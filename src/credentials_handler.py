import os

def get_aws_credentials():
    """Retrieve AWS credentials from environment variables."""
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv("AWS_DEFAULT_REGION")


    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS credentials are missing. Please check your environment variables.")

    return aws_access_key_id, aws_secret_access_key, aws_region
