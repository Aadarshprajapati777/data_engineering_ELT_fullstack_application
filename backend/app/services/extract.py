import pandas as pd
from io import BytesIO
from fastapi import UploadFile
from app.core.logging import logger

def extract_data(mtr_file: UploadFile, payment_file: UploadFile):
    logger.info("Extracting data from files")
    
    try:
        mtr_df = pd.read_excel(BytesIO(mtr_file.file.read()), sheet_name=0)  
        logger.info("MTR data extraction successful")
    except Exception as e:
        logger.error(f"Error during MTR data extraction: {str(e)}")
        raise e
    
    try:
        # reset file pointer before reading
        payment_file.file.seek(0)
        
        # read Payment file with potential adjustments for delimiter and encoding
        payment_file_content = BytesIO(payment_file.file.read())
        payment_df = pd.read_csv(payment_file_content, encoding='utf-8')
        logger.info(f"Payment data extraction successful. Columns found: {payment_df.columns.tolist()}")
    except pd.errors.EmptyDataError:
        logger.error("Payment file appears to be empty.")
        raise ValueError("Payment file appears to be empty.")
    except pd.errors.ParserError as e:
        logger.error(f"Parser error during Payment data extraction: {str(e)}")
        raise ValueError(f"Parser error during Payment data extraction: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during Payment data extraction: {str(e)}")
        raise e
    
    return mtr_df, payment_df
