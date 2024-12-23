import pytest
import boto3
from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    ClientError,
)


class TestConnectingToAWSServices:
    """
    Tests for verifying AWS S3 client connectivity and operations.
    """

    def test_s3_client_initialised_from_conftest_file(self, mock_s3_setup):
        """
        Test that the S3 client initializes properly using the mock_s3_setup fixture.
        """
        try:
            response = mock_s3_setup.list_buckets()
            assert "Buckets" in response, "Buckets key missing in response."
        except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
            pytest.fail(f"Error initializing S3 client: {e}")

    def test_isolated_s3_client_initialised(self, mock_s3_setup):
        """
        Test that an isolated S3 client initializes properly, independent of connection.py.
        """
        isolated_s3_client = boto3.client("s3", region_name="eu-west-2")

        try:
            response = isolated_s3_client.list_buckets()
            assert "Buckets" in response, "Buckets key missing in response."
        except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
            pytest.fail(f"Error initializing isolated S3 client: {e}")

    def test_list_buckets_after_connection_made(self, mock_s3_setup):
        """
        Test that the S3 client can list buckets successfully after establishing a connection.
        """
        try:
            response = mock_s3_setup.list_buckets()
            assert (
                "Buckets" in response
            ), "Response does not contain 'Buckets' key."
        except ClientError as e:
            pytest.fail(f"Error while listing buckets: {e}")
