import boto3
import json
import pandas as pd
import io
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def download_s3_file_and_convert_to_pandas_dataframe(file_to_obfuscate):

    if file_to_obfuscate.strip().startswith("{"):
        try:
            file_to_obfuscate = json.loads(file_to_obfuscate)["file_to_obfuscate"]
        except (json.JSONDecodeError, KeyError):
            raise ValueError("Invalid file path: Expected a json string of S3 URI starting with 's3://'.")
        
    # if not file_to_obfuscate.startswith("s3://"):
    #     raise ValueError("Invalid file path: Expected a json string of S3 URI starting with 's3://'.")

    # bucket_name, key = file_to_obfuscate[5:].split("/", 1)
    # response = s3.get_object(Bucket=bucket_name, Key=key)
    # file_content = response['Body'].read()

    try:
        bucket_name, key = file_to_obfuscate[5:].split("/", 1)
        response = s3.get_object(Bucket=bucket_name, Key=key)
        file_content = response['Body'].read()
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise ValueError(f"NoSuchKey: The specified key {key} does not exist in the S3 bucket.") from e
        raise

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
            raise ValueError(f"Unsupported file type: {file_type}." 
                             f"Supported file types are csv, parquet, and JSON."
                             f"File path: {file_to_obfuscate}")
        

def dataframe_to_bytes(df: pd.DataFrame, file_type):

    buffer = io.BytesIO()

    match file_type:
        case "csv":
            df.to_csv(buffer, index=False)
        case "parquet":
            df.to_parquet(buffer, index=False)
        case "json":
            buffer.write(df.to_json(orient="records").encode('utf-8'))
        case _:
            raise ValueError(f"Unsupported file type: {file_type}")
        
    buffer.seek(0)
    return buffer.getvalue()