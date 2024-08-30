import pandas as pd
from sqlalchemy.orm import Session
from app.db.models import MergedData
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.logging import logger 
import numpy as np 

def fetch_and_summarize_merged_data(db: Session) -> pd.DataFrame:
    # Fetch data from the database
    query = db.query(MergedData).all()
    df = pd.DataFrame([item.__dict__ for item in query])

    # Drop SQLAlchemy metadata fields (if present)
    df = df.drop(columns=['_sa_instance_state'], errors='ignore')

    # Ensure columns are present
    required_columns = ['order_id', 'p_description', 'net_amount']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise KeyError(f"Missing columns in MergedData DataFrame: {', '.join(missing_columns)}")
    
    # Convert net_amount to numeric, forcing errors to NaN and fill NaN with 0
    df['net_amount'] = pd.to_numeric(df['net_amount'], errors='coerce').fillna(0)
    
    # Filter out rows with empty or blank Order ID
    filtered_df = df[df['order_id'].str.strip() != '']

    # Create summary based on p_description and sum of net_amount
    summary = filtered_df.groupby('p_description').agg({'net_amount': 'sum'}).reset_index()
    summary.rename(columns={'net_amount': 'Sum of Net Amount'}, inplace=True)
    
    return summary


router = APIRouter()

@router.get("/summary")
async def get_summary(db: Session = Depends(get_db)):
    try:
        summary = fetch_and_summarize_merged_data(db)
        logger.info("Summary fetched successfully")
        return {"summary": summary.to_dict(orient='records')}
    except Exception as e:
        logger.error(f"Error fetching summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching summary: {str(e)}")
