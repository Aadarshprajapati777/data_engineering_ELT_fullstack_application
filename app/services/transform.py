# import pandas as pd

# def transform_data(df: pd.DataFrame) -> dict:
#     datasets = {}

#     # Dataset for 'Removal Order IDs'
#     datasets['Removal Order IDs'] = df[df['Order ID'].str.len() == 10]

#     # Dataset for 'Return'
#     datasets['Return'] = df[(df['Transaction Type'] == 'Return') & (df['Invoice Amount'].notna())]

#     # Dataset for 'Negative Payout'
#     datasets['Negative Payout'] = df[(df['Transaction Type'] == 'Payment') & (df['Net Amount'] < 0)]

#     # Dataset for 'Order & Payment Received'
#     datasets['Order & Payment Received'] = df[
#         (df['Order ID'].notna()) &
#         (df['Payment Net Amount'].notna()) &
#         (df['Shipment Invoice Amount'].notna())
#     ]

#     # Dataset for 'Order Not Applicable but Payment Received'
#     datasets['Order Not Applicable but Payment Received'] = df[
#         (df['Order ID'].notna()) &
#         (df['Payment Net Amount'].notna()) &
#         (df['Shipment Invoice Amount'].isna())
#     ]

#     # Dataset for 'Payment Pending'
#     datasets['Payment Pending'] = df[
#         (df['Order ID'].notna()) &
#         (df['Shipment Invoice Amount'].notna()) &
#         (df['Payment Net Amount'].isna())
#     ]

#     return datasets


# app/services/transform.py
import pandas as pd

def transform_data(mtr_df: pd.DataFrame, payment_df: pd.DataFrame) -> pd.DataFrame:
    # Processing the Merchant Tax Report (MTR)
    if 'Transaction Type' in mtr_df.columns:
        mtr_df = mtr_df[mtr_df['Transaction Type'] != 'Cancel']
        mtr_df['Transaction Type'] = mtr_df['Transaction Type'].replace({
            'Refund': 'Return',
            'FreeReplacement': 'Return'
        })

    # Processing the Payment Report
    if 'Type' in payment_df.columns:
        payment_df = payment_df[payment_df['Type'] != 'Transfer']
        payment_df = payment_df.rename(columns={'Type': 'Payment Type'})
        payment_df['Payment Type'] = payment_df['Payment Type'].replace({
            'Ajdustment': 'Order',
            'FBA Inventory Fee': 'Order',
            'Fulfilment Fee Refund': 'Order',
            'Service Fee': 'Order',
            'Refund': 'Return'
        })
        payment_df['Transaction Type'] = 'Payment'

    # Merge MTR and Payment DataFrames into a single dataset
    merged_df = pd.concat([mtr_df, payment_df], ignore_index=True)

    # Filtering out rows with an empty or blank 'Order ID'
    merged_df = merged_df[merged_df['Order ID'].notna() & (merged_df['Order ID'] != '')]

    # Grouping the dataset by 'Order ID' and creating summaries for each group
    grouped = merged_df.groupby('Order ID').agg({
        'Transaction Type': lambda x: list(x),
        'Invoice Amount': 'sum',
        'Net Amount': 'sum'
    }).reset_index()

    return grouped

# This will return the grouped DataFrame which can then be further processed into different categories
