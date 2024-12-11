import boto3
import json
import io
import pandas as pd

"""
The target CSV file might look like this:
student_id,name,course,cohort,graduation_date,email_address
...
1234,'John Smith','Software','2024-03-31','j.smith@email.com'
"""

s3 = boto3.client('s3')

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

def download_s3_file_and_convert_to_pandas_dataframe(file_to_obfuscate):

    if not file_to_obfuscate.startswith("s3://"):
        raise ValueError("Invalid file path: Expected an S3 URI starting with 's3://'.")

    bucket_name, key = file_to_obfuscate[5:].split("/", 1)
    response = s3.get_object(Bucket=bucket_name, Key=key)
    file_content = response['body'].read()

    _, file_type = file_to_obfuscate.rsplit(".", 1)
    file_type = file_type.lower()

    match file_type:
        case "csv":
            return pd.read_csv(io.StringIO(file_content.decode('utf-8')))
        case "json":
            return pd.read_json(io.StringIO(file_content.decode('utf-8')))
        case "parquet":
            return pd.read_parquet(io.BytesIO(file_content))
        case _:
            raise ValueError(f"Unsupported file type: {file_type}. Supported types are csv, parquet, and json.")
        
