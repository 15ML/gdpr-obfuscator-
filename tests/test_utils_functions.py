import pytest
import pandas as pd
from src.utils import read_json_input, obfuscate_pii_fields


class TestReadJsonInputFunction:
    """
    Tests for the `read_json_input` function.
    """

    def test_no_errors_with_valid_json_input_no_dependency(self):
        """
        Test that valid JSON input without dependency injection is processed correctly.
        """
        dummy_input = """
        {
            "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
            "pii_fields": ["name", "email_address"]
        }
        """
        actual_results = read_json_input(dummy_input)
        expected_results = (
            "s3://my_ingestion_bucket/new_data/file1.csv",
            ["name", "email_address"],
        )
        assert actual_results == expected_results

    def test_no_errors_with_valid_json_input_with_dependency(self):
        """
        Test that valid JSON input with dependency injection is processed correctly.
        """

        def valid_json_string_input():
            return """{
                "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
                "pii_fields": ["name", "email_address"]
            }"""

        actual_results = read_json_input(valid_json_string_input())
        expected_results = (
            "s3://my_ingestion_bucket/new_data/file1.csv",
            ["name", "email_address"],
        )
        assert actual_results == expected_results

    def test_errors_with_invalid_inputs(self):
        """
        Test that invalid inputs raise appropriate errors.
        """
        invalid_inputs = [
            {
                "file_to_obfuscate": "s3://my_bucket/data/file.csv",
                "pii_fields": ["name", "email_address"],
            },
            '{"file_to_obfuscate": \'\', "pii_fields": []}',
            123456,
            "Hello World!",
            None,
        ]
        expected_error_messages = [
            "Input must be a valid JSON string and cannot be empty.",
            "Input is not a valid JSON format as expected",
            "Input must be a valid JSON string and cannot be empty.",
            "Input is not a valid JSON format as expected",
            "Input must be a valid JSON string and cannot be empty.",
        ]

        for input_data, expected_message in zip(
            invalid_inputs, expected_error_messages
        ):
            with pytest.raises(ValueError, match=expected_message):
                read_json_input(input_data)


class TestObfuscatePiiFields:
    """
    Tests for the `obfuscate_pii_fields` function.
    """

    def test_handles_missing_values(self):
        """
        Test that missing PII fields are handled with 'MISSING VALUE'.
        """
        file_path = "tests/dummy_test_data/parquet_dummy.parquet"
        parquet_df = pd.read_parquet(file_path)
        pii_fields = ["email_address"]
        results = obfuscate_pii_fields(parquet_df, pii_fields)

        assert results["email_address"][1] == "MISSING VALUE"

    def test_empty_dataframe_returns_error(self):
        """
        Test that an empty DataFrame raises a ValueError and returns an empty DataFrame.
        """
        empty_df = pd.DataFrame()
        pii_fields = ["email_address"]

        with pytest.raises(
            ValueError,
            match="Input DataFrame is empty. Cannot proceed with processing.",
        ):
            obfuscate_pii_fields(empty_df, pii_fields)

    def test_successful_obfuscation_csv(self):
        """
        Test that PII fields are successfully obfuscated in a CSV file with no missing values.
        """
        file_path = "tests/dummy_test_data/csv_dummy.csv"
        csv_data = pd.read_csv(file_path)

        pii_fields = ["name", "email_address"]
        results = obfuscate_pii_fields(csv_data, pii_fields)

        expected_name = ["******", "******", "******"]
        expected_email = ["******", "******", "******"]

        assert list(results["name"]) == expected_name
        assert list(results["email_address"]) == expected_email

    def test_successful_obfuscation_parquet_and_json(self):
        """
        Test that PII fields are successfully obfuscated in Parquet and JSON files with missing values.
        """
        parquet_file_path = "tests/dummy_test_data/parquet_dummy.parquet"
        json_file_path = "tests/dummy_test_data/json_dummy.json"

        parquet_file = pd.read_parquet(parquet_file_path)
        json_file = pd.read_json(json_file_path)

        pii_fields = ["name", "email_address"]

        parquet_results = obfuscate_pii_fields(parquet_file, pii_fields)
        json_results = obfuscate_pii_fields(json_file, pii_fields)

        expected_parquet_name = [
            "MISSING VALUE",
            "******",
            "******",
            "MISSING VALUE",
            "******",
        ]
        expected_parquet_email = [
            "******",
            "MISSING VALUE",
            "******",
            "******",
            "MISSING VALUE",
        ]
        expected_json_name = [
            "MISSING VALUE",
            "******",
            "******",
            "MISSING VALUE",
            "******",
        ]
        expected_json_email = [
            "******",
            "MISSING VALUE",
            "******",
            "******",
            "MISSING VALUE",
        ]

        assert list(parquet_results["name"]) == expected_parquet_name
        assert list(parquet_results["email_address"]) == expected_parquet_email
        assert list(json_results["name"]) == expected_json_name
        assert list(json_results["email_address"]) == expected_json_email
