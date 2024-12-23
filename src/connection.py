import boto3
import logging
from src.credentials_handler import get_aws_credentials

logging.basicConfig(level=logging.INFO)


def s3_client():
    """
    Create an authenticated S3 client using AWS credentials.
    This function retrieves a session with AWS credentials and uses it to create an S3 client.
    """
    session = get_aws_credentials()

    if session:
        logging.info(
            "AWS session successfully retrieved. Initializing S3 client."
        )
        return boto3.client(
            "s3",
            aws_access_key_id=session.get_credentials().access_key,
            aws_secret_access_key=session.get_credentials().secret_key,
            region_name=session.region_name,
        )
    else:
        logging.error(
            "Failed to retrieve AWS session. S3 client cannot be initialized."
        )
        return None
