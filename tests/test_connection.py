import unittest
from moto import mock_aws
import boto3
from connection import s3_client, s3_resource

class TestAWSConnection(unittest.TestCase):
    @mock_aws
    def test_s3_client_creation(self):
        """Test that the S3 client is created and can list buckets (basic operation)."""
        client = s3_client()
        self.assertIsNotNone(client)
        # Test the client can perform a simple operation
        self.assertIn('Buckets', client.list_buckets())  # Checking for key in the dict returned by list_buckets

    @mock_aws
    def test_s3_resource_creation(self):
        """Test that the S3 resource is created and can list bucket names."""
        resource = s3_resource()
        self.assertIsNotNone(resource)
        # Trying to list buckets to ensure the resource is correctly set up
        buckets = list(resource.buckets.all())  # This should not raise an error
        self.assertIsInstance(buckets, list)  # Further checking the type

if __name__ == '__main__':
    unittest.main()
