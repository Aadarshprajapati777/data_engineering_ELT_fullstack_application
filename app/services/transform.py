import pandas as pd
from app.core.logging import logger

def process_mtr(mtr_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Processing MTR data")
    
    # Remove rows with 'Cancel' in 'Transaction Type'
    mtr_df = mtr_df[mtr_df['Transaction Type'] != 'Cancel']
    
    # Use .loc to avoid SettingWithCopyWarning
    mtr_df.loc[:, 'Transaction Type'] = mtr_df['Transaction Type'].replace({
        'Refund': 'Return',
        'FreeReplacement': 'Return'
    })
    
    logger.info("MTR data processing successful")
    return mtr_df
