import boto3
import json
import pandas as pd
import io
import logging
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)

s3 = boto3.client('s3')

def download_s3_file_and_convert_to_pandas_dataframe(file_to_obfuscate):
    """
    Download a file from S3 and load it into a pandas DataFrame based on the file's type.
    
    Args:
        file_to_obfuscate (str): The path to the file in S3 or a JSON string containing the path.
    
    Returns:
        pd.DataFrame: The data from the S3 file loaded into a DataFrame.
    
    Raises:
        ValueError: If the input path is invalid or the file type is unsupported.
        ClientError: If there is an error fetching the file from S3.
    """
    if file_to_obfuscate.strip().startswith("{"):
        try:
            file_to_obfuscate = json.loads(file_to_obfuscate)["file_to_obfuscate"]
        except (json.JSONDecodeError, KeyError) as e:
            logging.error("Failed to parse the JSON string.")
            raise ValueError("Invalid file path: Expected a JSON string of S3 URI starting with 's3://'.") from e
        
    try:
        bucket_name, key = file_to_obfuscate[5:].split("/", 1)
        logging.info(f"Downloading file {key} from bucket {bucket_name}.")
        response = s3.get_object(Bucket=bucket_name, Key=key)
        file_content = response['Body'].read()
    except ClientError as e:
        logging.error(f"Failed to download from S3: {e}")
        raise

    _, file_type = file_to_obfuscate.rsplit(".", 1)
    file_type = file_type.lower()

    try:
        match file_type:
            case "csv":
                return pd.read_csv(io.StringIO(file_content.decode('utf-8')))
            case "json":
                return pd.read_json(io.StringIO(file_content.decode('utf-8')))
            case "parquet":
                return pd.read_parquet(io.BytesIO(file_content))
            case _:
                raise ValueError(f"Unsupported file type: {file_type}. Supported file types are csv, parquet, and JSON.")
    except ValueError as e:
        logging.error(f"File type error: {e}")
        raise

def dataframe_to_bytes(df: pd.DataFrame, file_type):
    """
    Convert a DataFrame to bytes, suitable for saving to a file.

    Args:
        df (pd.DataFrame): DataFrame to convert.
        file_type (str): Type of file to convert to ('csv', 'parquet', 'json').

    Returns:
        bytes: The DataFrame converted to bytes.
    
    Raises:
        ValueError: If the specified file type is unsupported.
    """
    buffer = io.BytesIO()

    try:
        match file_type:
            case "csv":
                df.to_csv(buffer, index=False)
            case "parquet":
                df.to_parquet(buffer, index=False)
            case "json":
                buffer.write(df.to_json(orient="records").encode('utf-8'))
            case _:
                raise ValueError(f"Unsupported file type: {file_type}.")
    except ValueError as e:
        logging.error(f"Conversion error: {e}")
        raise

    buffer.seek(0)
    return buffer.getvalue()
