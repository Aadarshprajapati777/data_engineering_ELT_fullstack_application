import numpy as np
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import MergedData
from app.services.extract import extract_data
from app.services.transform import process_mtr, process_payment, merge_datasets
from app.services.load import load_merged_data_to_db, load_processed_mtr_data_to_db, load_processed_payment_data_to_db
from app.core.logging import logger
import pandas as pd
from io import BytesIO
from fastapi import UploadFile

async def perform_elt(mtr_file: UploadFile, payment_file: UploadFile):
    logger.info("Starting ELT process")

#for debugging purpose
    payment_df = pd.read_csv(BytesIO(payment_file.file.read()))
    logger.info(f"Payment CSV Columns: {payment_df.columns.tolist()}")
    logger.info(f"First few rows of Payment DataFrame: {payment_df.head()}")    
    
    try:
        mtr_df, payment_df = extract_data(mtr_file, payment_file)
        logger.info("Data extraction successful")
    except Exception as e:
        logger.error(f"Error during data extraction: {str(e)}")
        raise e
    
    try:
        processed_mtr = process_mtr(mtr_df)
        logger.info("inside try block for loading processed mtr data")
        load_processed_mtr_data_to_db(process_mtr)

        processed_payment = process_payment(payment_df)
        logger.info("inside try block for loading processed payment data")
        load_processed_payment_data_to_db(processed_payment)

        logger.info("Data processing and loading of payment and mtr successful")
    except Exception as e:
        logger.error(f"Error during data processing: {str(e)}")
        raise e
    
    try:
        merged_df = merge_datasets(processed_mtr, processed_payment)
        logger.info("Data merging successful")
    except Exception as e:
        logger.error(f"Error during data merging: {str(e)}")
        raise e
    
    # Clean up the DataFrame before loading it into the database
    try:
        clean_merged_df(merged_df)

        load_merged_data_to_db(merged_df)

        logger.info("Data loading to DB successful")
    except Exception as e:
        logger.error(f"Error during data loading to DB: {str(e)}")
        raise e
    
    return {"status": "success", "merged_row_count": len(merged_df)}

def clean_merged_df(df: pd.DataFrame):
    logger.info("Cleaning up the merged DataFrame")

    # Ensure correct data types for numeric columns
    numeric_columns = ['invoice_amount', 'net_amount']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert non-numeric to NaN
            df[col] = df[col].replace({np.nan: None})  # Replace NaNs with None for DB compatibility

    # Ensure correct data types for string columns
    string_columns = ['order_id', 'payment_type', 'transaction_type', 'p_description']
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).replace('nan', None)  # Convert 'nan' strings to None

    # Handle datetime columns
    datetime_columns = ['order_date', 'payment_date']
    for col in datetime_columns:
        if col in df.columns:
            df[col] = df[col].replace({pd.NaT: None})  # Replace NaT with None for DB compatibility

    logger.info("DataFrame cleaned successfully")
