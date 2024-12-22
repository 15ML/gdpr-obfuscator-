import botocore
import botocore.exceptions
import pytest
import io
import pandas as pd
from src.file_handling import (
    download_s3_file_and_convert_to_pandas_dataframe,
    dataframe_to_bytes,
)


class TestDownloadFromS3AndConvertToPandas:
    """
    Tests for the function download_s3_file_and_convert_to_pandas_dataframe,
    which handles downloading files from S3 and converting them to pandas DataFrames.
    """

    # Sample test input paths
    csv_path = '{"file_to_obfuscate": "s3://mybucket/csv_data.csv"}'
    json_path = '{"file_to_obfuscate": "s3://mybucket/json_data.json"}'
    parquet_path = (
        '{"file_to_obfuscate": "s3://mybucket/parquet_data.parquet"}'
    )
    invalid_path = (
        '{"file_to_obfuscate": "s3://mybucket/unsupported_file.txt"}'
    )

    def test_file_download_with_s3_path_and_different_file_types(
        self, mock_s3_setup
    ):
        """
        Test downloading and converting valid S3 file paths and handling invalid paths.

        Args:
            mock_s3_setup (pytest fixture): Fixture to mock S3 setup.
        """
        # Test with CSV path
        result = download_s3_file_and_convert_to_pandas_dataframe(
            self.csv_path
        )
        assert (
            result is not None
        ), "Expected no exceptions for CSV path handling"

        # Test with JSON path
        result = download_s3_file_and_convert_to_pandas_dataframe(
            self.json_path
        )
        assert (
            result is not None
        ), "Expected no exceptions for JSON path handling"

        # Test with Parquet path
        result = download_s3_file_and_convert_to_pandas_dataframe(
            self.parquet_path
        )
        assert (
            result is not None
        ), "Expected no exceptions for Parquet path handling"

        # Test with invalid file type (NoSuchKey error expected)
        with pytest.raises(botocore.exceptions.ClientError, match="NoSuchKey"):
            download_s3_file_and_convert_to_pandas_dataframe(self.invalid_path)

    def test_function_converts_to_pandas_dataframe(self, mock_s3_setup):
        """
        Verify that the function converts S3 files to pandas DataFrames for various file formats.

        Args:
            mock_s3_setup (pytest fixture): Fixture to mock S3 setup.
        """
        # Test CSV file conversion
        result = download_s3_file_and_convert_to_pandas_dataframe(
            self.csv_path
        )
        assert isinstance(
            result, pd.DataFrame
        ), "Expected a DataFrame for CSV input"

        # Test JSON file conversion
        result = download_s3_file_and_convert_to_pandas_dataframe(
            self.json_path
        )
        assert isinstance(
            result, pd.DataFrame
        ), "Expected a DataFrame for JSON input"

        # Test Parquet file conversion
        result = download_s3_file_and_convert_to_pandas_dataframe(
            self.parquet_path
        )
        assert isinstance(
            result, pd.DataFrame
        ), "Expected a DataFrame for Parquet input"


class TestFinalUserOutputIsConvertedFromDataframeToByteStreamObject:
    """
    Tests for the function dataframe_to_bytes, which converts pandas DataFrames
    to byte stream objects for supported file formats (CSV, JSON, Parquet).
    """

    def test_dataframe_to_bytes_csv(self):
        """
        Test DataFrame to CSV byte stream conversion.
        """
        df = pd.DataFrame(
            {
                "student_id": [1234, 5678],
                "name": ["John Smith", "Jane Doe"],
                "course": ["Software", "Data Science"],
                "cohort": ["2024-03-31", "2023-12-15"],
                "graduation_date": ["2025-06-30", "2024-08-20"],
                "email_address": ["j.smith@email.com", "j.doe@email.com"],
            }
        )
        result = dataframe_to_bytes(df, "csv")
        expected = (
            b"student_id,name,course,cohort,graduation_date,email_address\n"
            b"1234,John Smith,Software,2024-03-31,2025-06-30,j.smith@email.com\n"
            b"5678,Jane Doe,Data Science,2023-12-15,2024-08-20,j.doe@email.com\n"
        )
        assert result == expected, "CSV conversion failed"

        # Confirm output using pandas read_csv
        csv_df = pd.read_csv(io.BytesIO(result))
        pd.testing.assert_frame_equal(csv_df, df, check_dtype=False)

    def test_dataframe_to_bytes_json(self):
        """
        Test DataFrame to JSON byte stream conversion.
        """
        df = pd.DataFrame(
            {
                "student_id": [1234, 5678],
                "name": ["John Smith", "Jane Doe"],
                "course": ["Software", "Data Science"],
                "cohort": ["2024-03-31", "2023-12-15"],
                "graduation_date": ["2025-06-30", "2024-08-20"],
                "email_address": ["j.smith@email.com", "j.doe@email.com"],
            }
        )
        result = dataframe_to_bytes(df, "json")
        expected = (
            b'[{"student_id":1234,"name":"John Smith","course":"Software","cohort":"2024-03-31",'
            b'"graduation_date":"2025-06-30","email_address":"j.smith@email.com"},'
            b'{"student_id":5678,"name":"Jane Doe","course":"Data Science","cohort":"2023-12-15",'
            b'"graduation_date":"2024-08-20","email_address":"j.doe@email.com"}]'
        )
        assert result == expected, "JSON conversion failed"

        # Confirm output using pandas read_json
        json_df = pd.read_json(io.BytesIO(result))
        pd.testing.assert_frame_equal(json_df, df, check_dtype=False)

    def test_dataframe_to_bytes_parquet(self):
        """
        Test DataFrame to Parquet byte stream conversion.
        """
        df = pd.DataFrame(
            {
                "student_id": [1234, 5678],
                "name": ["John Smith", "Jane Doe"],
                "course": ["Software", "Data Science"],
                "cohort": ["2024-03-31", "2023-12-15"],
                "graduation_date": ["2025-06-30", "2024-08-20"],
                "email_address": ["j.smith@email.com", "j.doe@email.com"],
            }
        )
        result = dataframe_to_bytes(df, "parquet")
        buffer = io.BytesIO(result)
        df_parquet = pd.read_parquet(buffer)
        pd.testing.assert_frame_equal(df, df_parquet)

    def test_dataframe_to_bytes_empty(self):
        """
        Test conversion of an empty DataFrame to a byte stream.
        """
        df = pd.DataFrame(
            columns=[
                "student_id",
                "name",
                "course",
                "cohort",
                "graduation_date",
                "email_address",
            ]
        )
        result = dataframe_to_bytes(df, "csv")
        expected = (
            b"student_id,name,course,cohort,graduation_date,email_address\n"
        )
        assert result == expected, "Empty DataFrame CSV conversion failed"
