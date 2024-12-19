import pytest
import boto3
from moto import mock_aws

# Fixtures for mocking AWS and credentials

@pytest.fixture(scope="function")
def aws_creds():
    """Set up AWS credentials in the environment."""
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@pytest.fixture(scope="function")
def mock_s3_setup(aws_creds):
    """Mock AWS S3 and upload a test file."""
    with mock_aws():
        s3 = boto3.client("s3", region_name="eu-west-2")
        # Explicitly provide the region configuration for the bucket
        s3.create_bucket(
            Bucket="mybucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )

        # Upload an valid CSV file
        csv_content = "student_id,name,course,cohort,graduation_date,email_address\n1234,Jane Walker,Data Science,2023-08-15,2025-06-30,jane.walker@example.com"
        s3.put_object(Bucket="mybucket", Key="data.csv", Body=csv_content)

        # Upload an empty CSV file
        empty_csv_content = ""
        s3.put_object(Bucket="mybucket", Key="empty.csv", Body=empty_csv_content)

        # Upload a CSV file with columns but no values
        empty_csv_values_content = "student_id,name,course,cohort,graduation_date,email_address"
        s3.put_object(Bucket="mybucket", Key="empty_values.csv", Body=empty_csv_values_content)
        yield