import pytest
import os
import json
import boto3
import pandas as pd
import io
from moto import mock_aws
from src.connection import s3_client

# Fixtures for mocking AWS and credentials

@pytest.fixture(scope="function")
def aws_creds():
    """Set up AWS credentials in the environment."""
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@pytest.fixture(scope="function")
def s3_client_fixture(aws_creds):
    """Initialize an S3 client."""
    return boto3.client("s3")

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
        # ----------------------------------------------------------------
        # Upload an valid CSV file
        csv_content = "student_id,name,course,cohort,graduation_date,email_address\n1234,Jane Walker,Data Science,2023-08-15,2025-06-30,jane.walker@example.com"
        s3.put_object(Bucket="mybucket", Key="csv_data.csv", Body=csv_content)

        # Upload an empty CSV file
        empty_csv_content = ""
        s3.put_object(Bucket="mybucket", Key="csv_empty.csv", Body=empty_csv_content)

        # Upload a CSV file with columns but no values
        empty_csv_values_content = "student_id,name,course,cohort,graduation_date,email_address"
        s3.put_object(Bucket="mybucket", Key="csv_empty_values.csv", Body=empty_csv_values_content)

        # ----------------------------------------------------------------
        # Upload a valid JSON file with different data
        json_content = json.dumps({
            "data": [
                {"student_id": 5678, "name": "Alex Johnson", "course": "Computer Science", "cohort": "2024-01-10", "graduation_date": "2026-05-15", "email_address": "alex.johnson@example.com"}
            ]
        })
        s3.put_object(Bucket="mybucket", Key="json_data.json", Body=json_content)

        # Upload an empty JSON file
        empty_json_content = json.dumps({})
        s3.put_object(Bucket="mybucket", Key="json_empty.json", Body=empty_json_content)

        # Upload a JSON file with structure but no data entries
        empty_json_values_content = json.dumps({
            "data": [
                {"student_id": None, "name": None, "course": None, "cohort": None, "graduation_date": None, "email_address": None}
            ]
        })
        s3.put_object(Bucket="mybucket", Key="json_empty_values.json", Body=empty_json_values_content)

        # ----------------------------------------------------------------
        # Create a sample DataFrame for Parquet
        parquet_df = pd.DataFrame({
            "student_id": [7890],
            "name": ["Emily Carter"],
            "course": ["Data Analytics"],
            "cohort": ["2023-09-01"],
            "graduation_date": ["2026-06-30"],
            "email_address": ["emily.carter@example.com"]
        })

        # Convert the DataFrame to Parquet format in memory
        parquet_buffer = io.BytesIO()
        parquet_df.to_parquet(parquet_buffer, index=False)
        parquet_buffer.seek(0)

        # Upload the mocked Parquet file to the mock S3 bucket
        s3.put_object(Bucket="mybucket", Key="parquet_data.parquet", Body=parquet_buffer.getvalue())

        yield