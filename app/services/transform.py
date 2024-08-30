import pandas as pd
from app.core.logging import logger

def process_mtr(mtr_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Processing MTR data")
    
    # Remove rows with 'Cancel' in 'Transaction Type'
    mtr_df = mtr_df[mtr_df['Transaction Type'] != 'Cancel']
    
    # Replace specific values in 'Transaction Type'
    mtr_df['Transaction Type'] = mtr_df['Transaction Type'].replace({
        'Refund': 'Return',
        'FreeReplacement': 'Return'
    })
    
    # Ensure 'Shipment Item Id' remains as string
    mtr_df['Shipment Item Id'] = mtr_df['Shipment Item Id'].astype(str)
    
    # Convert 'Invoice Amount' to numeric, coerce errors to NaN and drop such rows
    mtr_df['Invoice Amount'] = pd.to_numeric(mtr_df['Invoice Amount'], errors='coerce')
    mtr_df = mtr_df.dropna(subset=['Invoice Amount'])
    
    # Rename columns to match model field names
    mtr_df = mtr_df.rename(columns={
        'Invoice Date': 'invoice_date',
        'Shipment Date': 'shipment_date',
        'Order Date': 'order_date',
        'Shipment Item Id': 'shipment_item_id',
        'Item Description': 'item_description',
        'Invoice Amount': 'invoice_amount',
        'Transaction Type': 'transaction_type',
        'Order Id': 'order_id'
    })

    logger.info(f"DataFrame columns: {mtr_df.columns}")
    logger.info(f"First few rows of the DataFrame: \n{mtr_df.head()}")

    logger.info("MTR data processing successful")
    return mtr_df


def process_payment(payment_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Processing Payment data")

    # Remove newline characters from the 'type' and 'description' columns
    payment_df['type'] = payment_df['type'].str.replace('\n', ' ', regex=False).str.strip()
    payment_df['description'] = payment_df['description'].str.replace('\n', ' ', regex=False).str.strip()

    # Rename columns to match the model fields
    if 'type' in payment_df.columns:
        payment_df.rename(columns={'type': 'payment_type'}, inplace=True)
    elif 'Type' in payment_df.columns:
        payment_df.rename(columns={'Type': 'payment_type'}, inplace=True)
    else:
        logger.error("The 'type' or 'Type' column is missing in the Payment file.")
        raise KeyError("'type' or 'Type' column is missing")
    
    if 'description' in payment_df.columns:
        payment_df.rename(columns={'description': 'p_description'}, inplace=True)
    
    if 'date/time' in payment_df.columns:
        payment_df.rename(columns={'date/time': 'date_time'}, inplace=True)

    if 'order id' in payment_df.columns:
        payment_df.rename(columns={'order id': 'order_id'}, inplace=True)

    # Remove rows with 'Transfer' in 'payment_type'
    payment_df = payment_df[~payment_df['payment_type'].str.contains('Transfer', case=False, na=False)]

    # Rename specific values in 'payment_type'
    payment_df['payment_type'] = payment_df['payment_type'].replace({
        'Adjustment': 'Order',
        'FBA Inventory Fee': 'Order',
        'Fulfilment Fee Refund': 'Order',
        'Service Fee': 'Order',
        'Refund': 'Return'
    }, regex=True)

    # Add 'transaction_type' column with all values set to 'Payment'
    payment_df['transaction_type'] = 'Payment'

    # Convert 'total' to numeric (float), stripping any commas and coercing errors
    payment_df['total'] = payment_df['total'].replace({',': ''}, regex=True).astype(float)

    # Convert 'date_time' to datetime format
    payment_df['date_time'] = pd.to_datetime(payment_df['date_time'], errors='coerce')

    # Ensure 'order_id' is treated as a string
    payment_df['order_id'] = payment_df['order_id'].astype(str)

    # Drop rows with NaT in 'date_time' column or NaN in 'total' column
    payment_df = payment_df.dropna(subset=['date_time', 'total'])

    logger.info("Payment data processing successful")
    return payment_df



def merge_datasets(mtr_df: pd.DataFrame, payment_df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Merging MTR and Payment data")
    
    # Standardize column names
    mtr_df.columns = mtr_df.columns.str.strip().str.lower().str.replace(' ', '_')
    payment_df.columns = payment_df.columns.str.strip().str.lower().str.replace(' ', '_')

    payment_df.rename(columns={'total': 'net_amount'}, inplace=True)

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