import boto3
import os
import logging
from dotenv import load_dotenv


def get_aws_credentials():
    """
    Initialize a session to retrieve AWS credentials. If credentials are successfully retrieved
    from either AWS configuration files or environment variables, return the session.
    If not, return None indicating failure to retrieve valid credentials.
    """
    load_dotenv()  # Load .env file if available

    session = boto3.Session()  # Attempt to create a session

    if session.get_credentials() is not None:
        logging.info("Using AWS credentials from the configuration.")
        return session
    else:
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv(
            "AWS_REGION", "eu-west-2"
        )  # Default to 'eu-west-2' if not specified

        if aws_access_key_id and aws_secret_access_key:
            session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=aws_region,
            )
            logging.info("Using AWS credentials from environment variables.")
            return session

        logging.error("AWS credentials could not be retrieved.")
        return None
