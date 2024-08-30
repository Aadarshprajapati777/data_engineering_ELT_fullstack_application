import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.db.models import MergedData
from fastapi import APIRouter, Depends, HTTPException
from app.db.database import get_db
from app.core.logging import logger

def classify_rows(df: pd.DataFrame) -> pd.DataFrame:
    # Add a new column for classification based on the conditions provided
    df['classification'] = np.nan
    
    # Condition 1: If length of 'Order ID' is exactly 10, mark as 'Removal Order IDs'
    df.loc[df['order_id'].str.len() == 10, 'classification'] = 'Removal Order IDs'
    
    # Condition 2: If 'Transaction Type' is 'Return' and 'Invoice Amount' is not blank, mark as 'Return'
    df.loc[(df['transaction_type'] == 'Return') & (df['invoice_amount'].notna()), 'classification'] = 'Return'
    
    # Condition 3: If 'Transaction Type' is 'Payment' and 'Net Amount' is less than 0, mark as 'Negative Payout'
    df.loc[(df['transaction_type'] == 'Payment') & (df['net_amount'] < 0), 'classification'] = 'Negative Payout'
    
    # Condition 4: If 'Order ID' is not blank, 'Payment Net Amount' is not blank, and 'Shipment Invoice Amount' is not blank, mark as 'Order & Payment Received'
    df.loc[
        (df['order_id'].notna()) & 
        (df['net_amount'].notna()) & 
        (df['transaction_type'] == 'Shipment') & 
        (df['invoice_amount'].notna()), 
        'classification'
    ] = 'Order & Payment Received'
    
    # Condition 5: If 'Order ID' is not blank, 'Payment Net Amount' is not blank, but 'Shipment Invoice Amount' is blank, mark as 'Order Not Applicable but Payment Received'
    df.loc[
        (df['order_id'].notna()) & 
        (df['net_amount'].notna()) & 
        (df['transaction_type'] != 'Shipment'), 
        'classification'
    ] = 'Order Not Applicable but Payment Received'
    
    # Condition 6: If 'Order ID' is not blank, 'Shipment Invoice Amount' is not blank, but 'Payment Net Amount' is blank, mark as 'Payment Pending'
    df.loc[
        (df['order_id'].notna()) & 
        (df['transaction_type'] == 'Shipment') & 
        (df['invoice_amount'].notna()) & 
        (df['net_amount'].isna()), 
        'classification'
    ] = 'Payment Pending'
    
    return df

def process_and_group_data(df: pd.DataFrame) -> list:
    # Ensure columns are present
    required_columns = ['order_id', 'transaction_type', 'invoice_amount', 'net_amount']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise KeyError(f"Missing columns in MergedData DataFrame: {', '.join(missing_columns)}")
    
    # Classify the rows according to the provided conditions
    df = classify_rows(df)
    
    # Replace NaN values in transaction_type with a string (e.g., 'Unknown')
    df['transaction_type'] = df['transaction_type'].fillna('Unknown')

    # Group by 'Order Id' and 'Transaction Type', then aggregate invoice and net amounts
    grouped = df.groupby(['order_id', 'transaction_type']).agg({
        'invoice_amount': 'sum',
        'net_amount': 'sum',
        'classification': lambda x: ', '.join(x.dropna().unique())
    }).reset_index()

    # Convert the grouped data into the desired nested format
    grouped_data = []
    
    for order_id, group in grouped.groupby('order_id'):
        transactions = {}
        for _, row in group.iterrows():
            transactions[row['transaction_type']] = {
                'invoice_amount': row['invoice_amount'],
                'net_amount': row['net_amount'],
                'classification': row['classification']
            }
        grouped_data.append({
            'order_id': order_id,
            'transactions': transactions
        })

    return grouped_data

router = APIRouter()

@router.get("/grouped_data")
async def get_grouped_data(db: Session = Depends(get_db)):
    try:
        # Fetch the data from the database
        query = db.query(MergedData).all()
        df = pd.DataFrame([item.__dict__ for item in query])
        
        # Drop SQLAlchemy metadata fields (if present)
        df = df.drop(columns=['_sa_instance_state'], errors='ignore')
        
        # Process and group the data
        grouped_data = process_and_group_data(df)
        
        logger.info("Data grouping completed successfully")
        return {"grouped_data": grouped_data}
    except Exception as e:
        logger.error(f"Error during data grouping: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during data grouping: {str(e)}")
