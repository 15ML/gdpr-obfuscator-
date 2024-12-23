import pytest
import os
import json
import boto3
import pandas as pd
import io
from moto import mock_aws

# Fixtures for mocking AWS and credentials

@pytest.fixture(scope="function")
def aws_creds():
    """
    Set up temporary AWS credentials in the environment.
    These credentials are used for mocking AWS services during tests.
    """
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    yield
    # Clean up environment variables after the test
    os.environ.pop("AWS_ACCESS_KEY_ID", None)
    os.environ.pop("AWS_SECRET_ACCESS_KEY", None)
    os.environ.pop("AWS_DEFAULT_REGION", None)


@pytest.fixture(scope="function")
def s3_client_fixture(aws_creds):
    """
    Provide an S3 client for interacting with AWS services during tests.
    This client uses the mocked credentials from aws_creds.
    """
    return boto3.client("s3")


@pytest.fixture(scope="function")
def mock_s3_setup(aws_creds):
    """
    Mock an S3 environment, set up a bucket, and upload test files.
    """
    with mock_aws():
        s3 = boto3.client("s3", region_name="eu-west-2")
        s3.create_bucket(
            Bucket="mybucket",
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        # Upload test files
        _upload_test_files_to_s3(s3)

        # Yield the client for test use
        yield s3


def _upload_test_files_to_s3(s3):
    """
    Upload various test files to the mocked S3 bucket for testing.

    Args:
        s3 (boto3.client): The mocked S3 client.
    """
    # CSV files
    s3.put_object(
        Bucket="mybucket",
        Key="csv_data.csv",
        Body="student_id,name,course,cohort,graduation_date,email_address\n1234,Jane Walker,Data Science,2023-08-15,2025-06-30,jane.walker@example.com",
    )
    s3.put_object(Bucket="mybucket", Key="csv_empty.csv", Body="")
    s3.put_object(
        Bucket="mybucket",
        Key="csv_empty_values.csv",
        Body="student_id,name,course,cohort,graduation_date,email_address",
    )

    # JSON files
    s3.put_object(
        Bucket="mybucket",
        Key="json_data.json",
        Body=json.dumps(
            {
                "data": [
                    {
                        "student_id": 5678,
                        "name": "Alex Johnson",
                        "course": "Computer Science",
                        "cohort": "2024-01-10",
                        "graduation_date": "2026-05-15",
                        "email_address": "alex.johnson@example.com",
                    }
                ]
            }
        ),
    )
    s3.put_object(
        Bucket="mybucket", Key="json_empty.json", Body=json.dumps({})
    )
    s3.put_object(
        Bucket="mybucket",
        Key="json_empty_values.json",
        Body=json.dumps(
            {
                "data": [
                    {
                        "student_id": None,
                        "name": None,
                        "course": None,
                        "cohort": None,
                        "graduation_date": None,
                        "email_address": None,
                    }
                ]
            }
        ),
    )

    # Parquet file
    parquet_df = pd.DataFrame(
        {
            "student_id": [7890],
            "name": ["Emily Carter"],
            "course": ["Data Analytics"],
            "cohort": ["2023-09-01"],
            "graduation_date": ["2026-06-30"],
            "email_address": ["emily.carter@example.com"],
        }
    )
    parquet_buffer = io.BytesIO()
    parquet_df.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)
    s3.put_object(
        Bucket="mybucket",
        Key="parquet_data.parquet",
        Body=parquet_buffer.getvalue(),
    )
