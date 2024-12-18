import boto3
import pandas as pd
import io

s3 = boto3.client('s3')

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
            raise ValueError(f"Unsupported file type: {file_type}." 
                             f"Supported file types are csv, parquet, and JSON."
                             f"File path: {file_to_obfuscate}")
        

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