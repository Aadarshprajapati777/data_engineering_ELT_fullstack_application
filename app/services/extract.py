import pandas as pd

def extract_data(file):
    filename = file.filename
    if filename.endswith('.csv'):
        df = pd.read_csv(file.file)
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(file.file)
    else:
        raise ValueError("Unsupported file type")
    return df
