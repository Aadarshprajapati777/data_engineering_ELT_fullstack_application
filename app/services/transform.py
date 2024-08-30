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
    
    if 'description' in payment_df.columns:
        payment_df.rename(columns={'description': 'p_description'}, inplace=True)
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


def merge_datasets(mtr_df: pd.DataFrame, payment_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Merging MTR and Payment data")
    
    # Standardize column names
    mtr_df.columns = mtr_df.columns.str.strip().str.lower().str.replace(' ', '_')
    payment_df.columns = payment_df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Merge datasets on 'order_id'
    if 'order_id' in mtr_df.columns and 'order_id' in payment_df.columns:
        merged_df = pd.merge(mtr_df, payment_df, on='order_id', how='outer')
        
        required_columns = [
            'order_id', 'transaction_type', 'payment_type', 
            'invoice_amount', 'net_amount', 'p_description',
            'order_date', 'payment_date'
        ]
        
        for column in required_columns:
            if column not in merged_df.columns:
                merged_df[column] = None
        
        # Select and reorder columns based on the exemplar
        merged_df = merged_df[required_columns]
        
        logger.info(f"Merged DataFrame columns: {merged_df.columns.tolist()}")
        logger.info("Data merging successful")
    else:
        logger.error("Column 'Order ID' not found in one of the datasets.")
        raise KeyError("'Order ID' column is missing")

    return merged_df

