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
def process_payment(payment_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Processing Payment data")

    # Remove newline characters from the 'type' and 'description' columns
    payment_df['type'] = payment_df['type'].str.replace('\n', ' ', regex=False).str.strip()
    payment_df['description'] = payment_df['description'].str.replace('\n', ' ', regex=False).str.strip()

    # Check if 'type' column exists and rename it
    if 'type' in payment_df.columns:
        payment_df.rename(columns={'type': 'Payment Type'}, inplace=True)
    elif 'Type' in payment_df.columns:
        payment_df.rename(columns={'Type': 'Payment Type'}, inplace=True)
    else:
        logger.error("The 'type' or 'Type' column is missing in the Payment file.")
        raise KeyError("'type' or 'Type' column is missing")

    # Remove rows with 'Transfer' in 'Payment Type'
    payment_df = payment_df[~payment_df['Payment Type'].str.contains('Transfer', case=False, na=False)]

    # Rename specific values in 'Payment Type' using .loc to avoid SettingWithCopyWarning
    payment_df.loc[:, 'Payment Type'] = payment_df['Payment Type'].replace({
        'Adjustment': 'Order',
        'FBA Inventory Fee': 'Order',
        'Fulfilment Fee Refund': 'Order',
        'Service Fee': 'Order',
        'Refund': 'Return'
    }, regex=True)

    # Add 'Transaction Type' column with all values set to 'Payment' using .loc
    payment_df.loc[:, 'Transaction Type'] = 'Payment'

    logger.info("Payment data processing successful")
    return payment_df
