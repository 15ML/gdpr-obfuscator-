import boto3
from src.credentials_handler import get_aws_credentials

def s3_client():
    """Create an authenticated S3 client using environment credentials."""
    aws_access_key_id, aws_secret_access_key = get_aws_credentials()
    return boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='eu-west-2'  # specify your region
    )
