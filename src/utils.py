import json
import pandas as pd
import io

def read_json_input(json_string):
    """
    Check if the input is a JSON string, if not raise an error.
    Parse the input JSON string
    """
    if not isinstance(json_string, str) or not json_string.strip():
        raise ValueError("Input must be a JSON string and cannot be empty.")
    try:
        input_data = json.loads(json_string)
    except json.JSONDecodeError:
        raise ValueError("Input is not a valid JSON string as expected")
    
    file_to_obfuscate = input_data['file_to_obfuscate']
    pii_fields = input_data['pii_fields']
    _, file_type = file_to_obfuscate.rsplit(".", 1)
    file_type = file_type.lower()

    if not file_to_obfuscate or not pii_fields:
        raise ValueError("Invalid input: 'file_to_obfuscate' and 'pii_fields' are required.")
    if not file_to_obfuscate.startswith("s3://"):
        raise ValueError("Invalid S3 path in 'file_to_obfuscate'.")
    if file_type not in ["csv", "parquet", "json"]:
        raise ValueError(f"Unsupported file type: {file_type}. Supported types are csv, parquet, and json.")
    return file_to_obfuscate, pii_fields

def obfuscate_pii_fields(df: pd.DataFrame, pii_fields):

    df = df.copy()

    try:
        for column in pii_fields:
            if column in df.columns:
                if df[column].isnull().any():
                    df[column] = df[column].fillna("MISSING VALUE")
                df[column] = "******"
        return df
    except Exception as e:
        raise Exception(f"Error obfuscating data!" 
                        f"Error: {e}")
    
def dataframe_to_bytes(df: pd.DataFrame, file_type):

    buffer = io.BytesIO()

    match file_type:
        case "csv":
            df.to_csv(buffer, Index=False)
        case "parquet":
            df.to_parquet(buffer, Index=False)
        case "json":
            buffer.write(df.to_json(orient="records").encode('utf-8'))
        case _:
            raise ValueError(f"Unsupported file type: {file_type}")
        
    buffer.seek(0)
    return buffer.getvalue()