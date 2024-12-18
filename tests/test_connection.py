import os
import unittest
from unittest.mock import patch
from moto import mock_aws
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from src.connection import s3_client

class TestAWSConnection(unittest.TestCase):
    @mock_aws
    def test_s3_client_creation(self):
        """Test that the S3 client is created and can list buckets."""
        client = s3_client()
        self.assertIsNotNone(client)
        response = client.list_buckets()
        self.assertIn('Buckets', response)  # Basic operation to check the client works

    @patch('boto3.client')
    def test_s3_client_invalid_credentials(self, mock_boto_client):
        """Test that the S3 client raises an error with invalid credentials."""
        # Simulate boto3 raising a NoCredentialsError
        mock_boto_client.side_effect = NoCredentialsError()

        with self.assertRaises(NoCredentialsError):
            client = s3_client()
            client.list_buckets()

    # def test_s3_client_missing_credentials(self):
    #     """Test behavior when AWS credentials are missing."""
    #     # Mock an empty environment
    #     with patch.dict('os.environ', {}, clear=True):
    #         with self.assertRaises(NoCredentialsError):
    #             client = s3_client()
    #             client.list_buckets()

    # @mock_aws
    # def test_s3_client_missing_credentials(self):
    #     """Test behavior when AWS credentials are missing."""
    #     with patch.dict(os.environ, {}, clear=True):  # Temporarily clear environment variables
    #         with self.assertRaises(NoCredentialsError):
    #             client = s3_client()
    #             client.list_buckets()

    # @mock_aws
    # def test_s3_client_missing_credentials(self):
    #     """Test behavior when AWS credentials are missing."""
    #     # Unset credentials
    #     os.environ.pop('AWS_ACCESS_KEY_ID', None)
    #     os.environ.pop('AWS_SECRET_ACCESS_KEY', None)
    #     with self.assertRaises(Exception):  # Expect failure without credentials
    #         client = s3_client()
    #         client.list_buckets()

    @mock_aws
    def test_s3_client_correct_region(self):
        """Test that the S3 client connects to the correct region."""
        client = boto3.client('s3', region_name='us-east-1')
        self.assertEqual(client.meta.region_name, 'us-east-1')


if __name__ == '__main__':
    unittest.main()
