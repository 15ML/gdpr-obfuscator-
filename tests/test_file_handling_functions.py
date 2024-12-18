import unittest
from moto import mock_aws
import boto3
import pandas as pd
from src.file_handling import download_s3_file_and_convert_to_pandas_dataframe, dataframe_to_bytes

class TestDownloadS3ConvertPandasFunction(unittest.TestCase):
    def set_up_mock_s3(self):
        """Set up the mock S3 environment before each test."""
        self.s3 = boto3.resource('s3', region_name='eu-west-2')
        self.bucket_name = 'mybucket'
        self.object_key = 'test.csv'
        # Create the bucket and upload the file
        self.bucket = self.s3.create_bucket(Bucket=self.bucket_name)
        self.bucket.Object(self.object_key).put(Body=b"name,email_address\nDavid Attenborough,david_a@email.com")


    @mock_aws
    def test_download_csv(self):
        """Test downloading a CSV file and converting to dataframe."""
        df = download_s3_file_and_convert_to_pandas_dataframe(f's3://{self.bucket_name}/{self.csv_object_key}')
        expected_df = pd.DataFrame({'name': ["David Attenborough"], 'email_address': ["david_a@email.com"]})
        pd.testing.assert_frame_equal(df, expected_df)

    def tearDown(self):
        """Clean up resources after tests."""
        # Clean up logic here, if necessary

if __name__ == '__main__':
    unittest.main()


    # @mock_aws
    # def test_download_invalid_csv_filepath_from_s3(self):
    #     self.bucket.

# @pytest.fixture(scope="function")
# def aws_mock_credentials():
#     """Mocked AWS Credentials for moto."""
#     import os
#     os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
#     os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
#     os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'
#     yield

# @pytest.fixture(scope="function")
# def setup_s3():
#     with mock_aws():
#         s3 = boto3.client('s3', region_name="eu-west-2")
#         s3.create_bucket(
#             Bucket="mybucket",
#             CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
#         )
#         s3.put_object(
#             Bucket="mybucket", 
#             Key="test.csv", 
#             Body="name,email_address\nDavid Attenborough,david_a@email.com"
#         )
#         yield s3

# @pytest.fixture(scope="function")
# def s3_client(aws_mock_credentials):
#     with mock_aws():
#         yield boto3.client("s3")


# @pytest.mark.usefixtures("setup_s3")
# def test_download_csv():
#     # Assuming the function is supposed to handle the CSV correctly
#     df = download_s3_file_and_convert_to_pandas_dataframe("s3://mybucket/test.csv")
#     assert not df.empty
#     assert df.iloc[0]['name'] == 'David Attenborough'





# @pytest.fixture(scope="function")
# def aws_mock_credentials():
#     """Mocked AWS Credentials for moto."""
#     import os
#     os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
#     os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
#     os.environ['AWS_SESSION_TOKEN'] = 'testing'
#     yield

# @pytest.fixture(scope="function")
# def s3_client():
#     with mock_aws():
#         client = boto3.client("s3", region_name="eu-west-2")
#         client.create_bucket(Bucket="mybucket")
#         yield client

# class TestDownloadS3ConvertPandasFunction:

#     def test_download_csv(self, s3_client):
#         # Assuming the function is supposed to handle the CSV correctly
#         df = download_s3_file_and_convert_to_pandas_dataframe("s3://mybucket/test.csv")
#         assert not df.empty
#         assert df.iloc[0]['name'] == 'David Attenborough'

#     def test_valid_and_invalid_s3_file_path(self, s3_client):

#         #bucket = "mybucket"
#         #s3.create_bucket(Bucket=bucket)
#         #key = "key/does/not/exist.csv"
#         #s3.put_object(Bucket=bucket, Key=key, Body="name, email_address\nDavid Attenborough, david_a@email.com")

#         with pytest.raises(ValueError) as e:
#             download_s3_file_and_convert_to_pandas_dataframe("invalid_file_path")
#         assert "Invalid file path: Expected an S3 URI starting with 's3://'." in str(e.value)
