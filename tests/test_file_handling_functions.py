import unittest
import pytest
import boto3
import io
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

class TestFinalUserOutputIsConvertedFromDataframeToByteStreamObject():

    def test_dataframe_to_bytes_csv(self):
        df = pd.DataFrame({
            "student_id": [1234, 5678],
            "name": ["John Smith", "Jane Doe"],
            "course": ["Software", "Data Science"],
            "cohort": ["2024-03-31", "2023-12-15"],
            "graduation_date": ["2025-06-30", "2024-08-20"],
            "email_address": ["j.smith@email.com", "j.doe@email.com"]
        })
        result = dataframe_to_bytes(df, "csv")
        expected = (
            b"student_id,name,course,cohort,graduation_date,email_address\n"
            b"1234,John Smith,Software,2024-03-31,2025-06-30,j.smith@email.com\n"
            b"5678,Jane Doe,Data Science,2023-12-15,2024-08-20,j.doe@email.com\n"
        )  # Expected CSV byte representation
        assert result == expected, "CSV conversion failed"
        
        # Use Pandas methods to read csv to confirm output file type
        csv_df = pd.read_csv(io.BytesIO(result))
        pd.testing.assert_frame_equal(csv_df, df, check_dtype=False, 
                                      obj="CSV content mismatch after reading back")


    def test_dataframe_to_bytes_json(self):
        df = pd.DataFrame({
            "student_id": [1234, 5678],
            "name": ["John Smith", "Jane Doe"],
            "course": ["Software", "Data Science"],
            "cohort": ["2024-03-31", "2023-12-15"],
            "graduation_date": ["2025-06-30", "2024-08-20"],
            "email_address": ["j.smith@email.com", "j.doe@email.com"]
        })
        result = dataframe_to_bytes(df, "json")
        expected = (
            b'[{"student_id":1234,"name":"John Smith","course":"Software","cohort":"2024-03-31",'
            b'"graduation_date":"2025-06-30","email_address":"j.smith@email.com"},'
            b'{"student_id":5678,"name":"Jane Doe","course":"Data Science","cohort":"2023-12-15",'
            b'"graduation_date":"2024-08-20","email_address":"j.doe@email.com"}]'
        )  # Expected JSON byte representation
        assert result == expected, "JSON conversion failed"

        # Use Pandas methods to read json to confirm output file type
        json_df = pd.read_json(io.BytesIO(result))
        pd.testing.assert_frame_equal(json_df, df, check_dtype=False, 
                                      obj="JSON content mismatch after reading back")


    def test_dataframe_to_bytes_parquet(self):
        
        df = pd.DataFrame({
            "student_id": [1234, 5678],
            "name": ["John Smith", "Jane Doe"],
            "course": ["Software", "Data Science"],
            "cohort": ["2024-03-31", "2023-12-15"],
            "graduation_date": ["2025-06-30", "2024-08-20"],
            "email_address": ["j.smith@email.com", "j.doe@email.com"]
        })
        result = dataframe_to_bytes(df, "parquet")
        # Verify that the result is a valid Parquet file by reading it back
        buffer = io.BytesIO(result)
        df_parquet = pd.read_parquet(buffer)
        pd.testing.assert_frame_equal(df, df_parquet)

        # Use Pandas methods to read json to confirm output file type
        parquet_df = pd.read_parquet(io.BytesIO(result))
        pd.testing.assert_frame_equal(parquet_df, df, check_dtype=False, 
                                      obj="PARQUET content mismatch after reading back")
        
    def test_dataframe_to_bytes_empty(self):

        df = pd.DataFrame(columns=["student_id", "name", "course", "cohort", "graduation_date", "email_address"])
        result = dataframe_to_bytes(df, "csv")
        expected = b"student_id,name,course,cohort,graduation_date,email_address\n"  # Expected CSV for an empty DataFrame
        assert result == expected, "Empty DataFrame CSV conversion failed"

