import pytest
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from conftest import s3_client_fixture


class TestTestConnectingToAWSServices():

    s3_client_fixture = s3_client_fixture
    
    def test_s3_client_initialised_from_connection_file(self, s3_client_fixture):
        """Test that the S3 client initializes properly."""

        try:
            s3_client_fixture.list_buckets()
            print("S3 client initialized successfully.")
        except NoCredentialsError:
            pytest.fail("AWS credentials not found. Ensure they are properly set.")
        except PartialCredentialsError:
            pytest.fail("AWS credentials are partially configured. Check your setup.")
        except ClientError as e:
            pytest.fail(f"Unexpected error while initializing S3 client: {e}")

    def test_isolated_s3_client_initialised(self):
        """Test that the S3 client initializes properly not dependent on connection.py."""

        isolated_s3_client = boto3.client('s3', region_name='eu-west-2')

        try:
            isolated_s3_client.list_buckets() 
            print("S3 client initialized successfully.")
        except NoCredentialsError:
            pytest.fail("AWS credentials not found. Ensure they are properly set.")
        except PartialCredentialsError:
            pytest.fail("AWS credentials are partially configured. Check your setup.")
        except ClientError as e:
            pytest.fail(f"Unexpected error while initializing S3 client: {e}")


    def test_list_buckets_after_connection_made(self, s3_client_fixture):
        """Test that the S3 client can list buckets."""
        try:
            response = s3_client_fixture.list_buckets()
            assert 'Buckets' in response, "Response does not contain 'Buckets' key."
        except ClientError as e:
            pytest.fail(f"Error while listing buckets: {e}")



