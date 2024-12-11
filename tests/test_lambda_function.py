import pytest
import pprint
import pandas as pd
from src.lambda_function import read_json_input

@pytest.fixture
def valid_csv_file_path():
    file_path = "tests/test_data/csv_dummy.csv"
    return file_path
class TestReadJsonInputFunction:

    def test_no_errors_raised_when_given_valid_json_input(self):

        dummy_input = """
        {
            "file_to_obfuscate": "s3://my_bucket/data/file.csv",
            "pii_fields": ["name", "email_address"]
        }
        """
        actual_results = read_json_input(dummy_input)
        expected_results = ("s3://my_bucket/data/file.csv",
                                 ["name", "email_address"])
        assert actual_results == expected_results

    def test_function_raises_errors_when_passed_different_invalid_inputs(self):

        invalid_json_dict = {
            "file_to_obfuscate": "s3://my_bucket/data/file.csv",
            "pii_fields": ["name", "email_address"]
        }
        with pytest.raises(ValueError) as invalid_dict_response:
            read_json_input(invalid_json_dict)

        invalid_json_integer = 123456
        with pytest.raises(ValueError) as invalid_integer_response:
            read_json_input(invalid_json_integer)

        invalid_json_string = "Hello World!"
        with pytest.raises(ValueError) as invalid_string_response:
            read_json_input(invalid_json_string)

        invalid_json_none = None
        with pytest.raises(ValueError) as invalid_none_response:
            read_json_input(invalid_json_none)

        assert str(invalid_dict_response.value) == "Input must be a JSON string and cannot be empty."
        assert str(invalid_integer_response.value) == "Input must be a JSON string and cannot be empty."
        assert str(invalid_string_response.value) == "Input is not a valid JSON string as expected"
        assert str(invalid_none_response.value) == "Input must be a JSON string and cannot be empty."
        




