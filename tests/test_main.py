import pytest
from src.main import main


def test_overall_main_function_flow(mock_s3_setup):
    """Test the main function end-to-end.

    This test verifies the overall flow of the main function by providing a valid input JSON.
    It checks whether the obfuscation process works as expected by comparing the actual output
    with the expected obfuscated content.

    Args:
        mock_s3_setup: Pytest fixture to mock AWS S3 interactions.

    Raises:
        AssertionError: If the actual output content does not match the expected content.
    """
    input_json = '{"file_to_obfuscate": "s3://mybucket/csv_data.csv", "pii_fields": ["email_address", "name"]}'
    result_bytes = main(input_json)

    # Converted obfuscated content from bytes to string for testing
    result_content = result_bytes.decode("utf-8")
    expected_content = (
        "student_id,name,course,cohort,graduation_date,email_address\n"
        "1234,******,Data Science,2023-08-15,2025-06-30,******\n"
    )

    assert (
        result_content == expected_content
    ), "The obfuscated content does not match expected output."


def test_integration_partial_pii_fields(mock_s3_setup):
    """Test obfuscation when some PII fields are missing in the file.

    This test ensures that the function raises a ValueError with the appropriate error message
    when attempting to obfuscate columns that do not exist in the input file.

    Args:
        mock_s3_setup: Pytest fixture to mock AWS S3 interactions.

    Raises:
        ValueError: If the columns specified in the PII fields are missing.
    """
    input_json = '{"file_to_obfuscate": "s3://mybucket/csv_data.csv", "pii_fields": ["name", "non_existent_field"]}'
    expected_error_message = (
        "The following columns to obfuscate are missing in the DataFrame provided. "
        "Missing columns: non_existent_field"
    )
    with pytest.raises(ValueError, match=expected_error_message):
        main(input_json)


def test_integration_empty_csv(mock_s3_setup):
    """Test handling of an empty CSV file.

    This test verifies that the function raises a ValueError with an appropriate error message
    when provided with an empty CSV file.

    Args:
        mock_s3_setup: Pytest fixture to mock AWS S3 interactions.

    Raises:
        ValueError: If the CSV file contains no columns to parse.
    """
    input_json = '{"file_to_obfuscate": "s3://mybucket/csv_empty.csv", "pii_fields": ["name", "email_address"]}'
    with pytest.raises(ValueError, match="No columns to parse from file"):
        main(input_json)


def test_integration_csv_with_columns_but_no_values(mock_s3_setup):
    """Test handling of a CSV file with columns but no values.

    This test ensures that the function raises a ValueError with an appropriate error message
    when provided with a CSV file that has column headers but no data values.

    Args:
        mock_s3_setup: Pytest fixture to mock AWS S3 interactions.

    Raises:
        ValueError: If the input DataFrame is empty.
    """
    input_json = '{"file_to_obfuscate": "s3://mybucket/csv_empty_values.csv", "pii_fields": ["name", "email_address"]}'
    with pytest.raises(
        ValueError,
        match="Input DataFrame is empty. Cannot proceed with processing.",
    ):
        main(input_json)
