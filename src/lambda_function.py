import logging
import os
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)

"""
def lambda_handler(event, context):
    logger.info("Lambda handler function is successful!")
    return {
        "StatusCode": 200,
        "body": "Hello world! From GDPR Lambda handler function!"
    }
"""

def read_data(file_path):
    """
    Determines the file format from the file extension and routes
    to the appropriate helper function to transform the data.

    Args:
        file_path (str): The path to the file.

    Returns:
        A Pandas DataFrame.
    """
    _, file_type = os.path.splitext(file_path)
    file_type = file_type.lower()

    try:
        match file_type:
            case ".csv":
                #data = pd.read_csv(file_path)
                return pd.read_csv(file_path)
            case ".json":
                #data = pd.read_json(file_path)
                return pd.read_json(file_path)
            case ".parquet":
                #data = pd.read_parquet(file_path)
                return pd.read_parquet(file_path)
    except:
        raise ValueError(f"Unsupported file type: {file_type}")
    
def transform_data(df: pd.DataFrame, pii_columns):
    """
    Transforms the DataFrame by obfuscating specified PII columns 
    and handling missing values whilst capturing any errors.

    Args:
        df (DataFrame): The input Pandas DataFrame to transform.
        pii_columns (list): List of column values to obfuscate.

    Returns:
        DataFrame: Transformed Pandas DataFrame.
    """
    try:
        for column in pii_columns:
            if column in df.columns:
                if df[column].isnull().any():
                    df[column] = df[column].fillna("MISSING")
                df[column] = "******"
        return df
    except Exception as e:
        raise Exception(f"Error transforming data: {e}")

#result = read_data("tests/test_data/csv_dummy.csv")
#print (result)