import unittest
import pytest
import boto3
import pandas as pd
from src.file_handling import download_s3_file_and_convert_to_pandas_dataframe, dataframe_to_bytes

class TestDownloadFromS3AndConvertToPandas():

    csv_path = '{"file_to_obfuscate": "s3://mybucket/csv_data.csv"}'
    json_path = '{"file_to_obfuscate": "s3://mybucket/json_data.json"}'
    parquet_path = '{"file_to_obfuscate": "s3://mybucket/parquet_data.parquet"}'
    invalid_path = 's3://mybucket/unsupported_file.txt'

    def test_file_download_with_s3_path_and_different_file_types(self, mock_s3_setup):

        # Test with CSV path
        result = download_s3_file_and_convert_to_pandas_dataframe(self.csv_path)
        assert result is not None, "Expected no exceptions for CSV path handling"

        # Test with JSON path
        result = download_s3_file_and_convert_to_pandas_dataframe(self.json_path)
        assert result is not None, "Expected no exceptions for JSON path handling"

        # Test with Parquet path
        result = download_s3_file_and_convert_to_pandas_dataframe(self.parquet_path)
        assert result is not None, "Expected no exceptions for Parquet path handling"

        # Test with invalid file type
        with pytest.raises(ValueError) as e:
            download_s3_file_and_convert_to_pandas_dataframe(self.invalid_path)
        assert "NoSuchKey" in str(e.value), "Expected NoSuchKey error for missing file"


    def test_function_converts_to_pandas_dataframe(self, mock_s3_setup):
        
        # CSV
        result = download_s3_file_and_convert_to_pandas_dataframe(self.csv_path)
        assert isinstance(result, pd.DataFrame)

        #JSON
        result = download_s3_file_and_convert_to_pandas_dataframe(self.json_path)
        assert isinstance(result, pd.DataFrame)

        # Parquet
        result = download_s3_file_and_convert_to_pandas_dataframe(self.parquet_path)
        assert isinstance(result, pd.DataFrame)




