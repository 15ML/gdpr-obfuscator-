import boto3
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

def get_aws_credentials():
    """
    Retrieve AWS credentials from AWS configuration or environment variables and initialize a boto3 session.
    
    The function first tries to fetch AWS credentials from the AWS configuration.
    If this fails, it looks for credentials in environment variables set from a .env file.
    
    Returns:
        session (boto3.Session): An AWS session object initialized with credentials,
        or None if credentials could not be retrieved.
    """
    # Load environment variables from .env file if available
    load_dotenv()

    # Initialize a session to see if it can retrieve credentials from the AWS config
    session = boto3.Session()

    # Try to use credentials from AWS config
    if session.get_credentials().access_key:
        logging.info("Using AWS credentials from the AWS configuration.")
    else:
        # If no valid credentials from AWS config, check if they are set as environment variables from .env file
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_REGION')
        if aws_access_key_id and aws_secret_access_key:
            session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region
            )
            logging.info("Using AWS credentials from environment variables.")
        else:
            logging.error("AWS credentials could not be retrieved from AWS configuration or environment variables.")
            return None
    
    return session

session = get_aws_credentials()
if session is None:
    logging.error("AWS session could not be established.")
else:
    logging.info("AWS session established successfully.")
