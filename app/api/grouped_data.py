import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.db.models import MergedData
from fastapi import APIRouter, Depends, HTTPException
from app.db.database import get_db
from app.core.logging import logger

def process_and_group_data(df: pd.DataFrame) -> list:
    # Ensure columns are present
    required_columns = ['order_id', 'transaction_type', 'invoice_amount', 'net_amount']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise KeyError(f"Missing columns in MergedData DataFrame: {', '.join(missing_columns)}")
    
    # Replace NaN values in transaction_type with a string (e.g., 'Unknown')
    df['transaction_type'] = df['transaction_type'].fillna('Unknown')

    # Group by 'Order Id' and 'Transaction Type', then aggregate invoice and net amounts
    grouped = df.groupby(['order_id', 'transaction_type']).agg({
        'invoice_amount': 'sum',
        'net_amount': 'sum'
    }).reset_index()

    # Convert the grouped data into the desired nested format
    grouped_data = []
    
    for order_id, group in grouped.groupby('order_id'):
        transactions = {}
        for _, row in group.iterrows():
            transactions[row['transaction_type']] = {
                'invoice_amount': row['invoice_amount'],
                'net_amount': row['net_amount']
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
