import os
import pytest
import boto3
from moto import mock_aws
from src.main import main

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


def test_overall_main_function_flow(mock_s3_setup):
    """Test the main function end-to-end."""

    input_json = '{"file_to_obfuscate": "s3://mybucket/data.csv", "pii_fields": ["email_address", "name"]}'
    result_bytes = main(input_json)

    # Converted obfuscated content from bytes to string for testing)
    result_content = result_bytes.decode("utf-8")
    expected_content = "student_id,name,course,cohort,graduation_date,email_address\n1234,******,Data Science,2023-08-15,2025-06-30,******\n"

    # The below message will only display if this test fails
    assert result_content == expected_content, "The obfuscated content does not match expected output."


def test_integration_partial_pii_fields(mock_s3_setup):
    """Test obfuscation when some PII fields are missing in the file."""
    input_json = '{"file_to_obfuscate": "s3://mybucket/data.csv", "pii_fields": ["name", "non_existent_field"]}'
    
    expected_error_message = (
        "The following columns to obfuscate are missing in the DataFrame provided. "
        "Missing columns: non_existent_field"
    )
    with pytest.raises(ValueError, match=expected_error_message):
        main(input_json)


def test_integration_empty_csv(mock_s3_setup):
    """Test handling of an empty CSV file."""
    input_json = '{"file_to_obfuscate": "s3://mybucket/empty.csv", "pii_fields": ["name", "email_address"]}'
    with pytest.raises(ValueError, match="No columns to parse from file"):
        main(input_json)

def test_integration_csv_with_columns_but_no_values(mock_s3_setup):
    """Test handling of an empty CSV file."""
    input_json = '{"file_to_obfuscate": "s3://mybucket/empty_values.csv", "pii_fields": ["name", "email_address"]}'
    with pytest.raises(ValueError, match="Input DataFrame is empty. Cannot proceed with processing."):
        main(input_json)