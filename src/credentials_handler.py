# import os

# def get_aws_credentials():
#     """Retrieve AWS credentials from environment variables."""
#     aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
#     aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
#     aws_region = os.getenv("AWS_DEFAULT_REGION")


#     if not aws_access_key_id or not aws_secret_access_key:
#         raise ValueError("AWS credentials are missing. Please check your environment variables.")

#     return aws_access_key_id, aws_secret_access_key, aws_region

import boto3
import os

def get_aws_credentials():
    session = boto3.session.Session()
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    if aws_access_key_id and aws_secret_access_key:
        # set credentials using .env variables
        session.set_credentials(aws_access_key_id, aws_secret_access_key)
        print("using credentials from .env")
    else:
        # use the default credentials from the AWS credentials file
        print("using credentials from the AWS credentials file")
    
    return session

session = get_aws_credentials()
