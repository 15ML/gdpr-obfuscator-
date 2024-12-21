import pytest
import pandas as pd
from src.utils import read_json_input, obfuscate_pii_fields

class TestReadJsonInputFunction:

    def test_no_errors_raised_when_given_valid_json_input_no_dependency(self):

        dummy_input = """
        {
            "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
            "pii_fields": ["name", "email_address"]
        }
        """
        actual_results = read_json_input(dummy_input)
        expected_results = ("s3://my_ingestion_bucket/new_data/file1.csv",
                                 ["name", "email_address"])
        assert actual_results == expected_results
    
    
    def test_no_errors_raised_when_given_valid_json_input_with_dependency_injection(self):

        def valid_json_string_input():
            file_path = "{\"file_to_obfuscate\": \"s3://my_ingestion_bucket/new_data/file1.csv\", \"pii_fields\": [\"name\", \"email_address\"]}"
            return file_path
        
        actual_results = read_json_input(valid_json_string_input())
        expected_results = ("s3://my_ingestion_bucket/new_data/file1.csv",
                                 ["name", "email_address"])
        assert actual_results == expected_results


    def test_function_raises_errors_when_passed_different_invalid_inputs(self):

        invalid_json_dict = {
            "file_to_obfuscate": "s3://my_bucket/data/file.csv",
            "pii_fields": ["name", "email_address"]
        }
        with pytest.raises(ValueError) as invalid_dict_response:
            read_json_input(invalid_json_dict)

        invalid_empty_json = "{\"file_to_obfuscate\": '', \"pii_fields\": []}"
        with pytest.raises(ValueError) as invalid_empty_json_response:
            read_json_input(invalid_empty_json)

        invalid_json_integer = 123456
        with pytest.raises(ValueError) as invalid_integer_response:
            read_json_input(invalid_json_integer)

        invalid_json_string = "Hello World!"
        with pytest.raises(ValueError) as invalid_string_response:
            read_json_input(invalid_json_string)

        invalid_json_none = None
        with pytest.raises(ValueError) as invalid_none_response:
            read_json_input(invalid_json_none)

        assert str(invalid_dict_response.value) == "Input must be a valid JSON string and cannot be empty."
        assert str(invalid_empty_json_response.value) == "Input is not a valid JSON format as expected"
        assert str(invalid_integer_response.value) == "Input must be a valid JSON string and cannot be empty."
        assert str(invalid_string_response.value) == "Input is not a valid JSON format as expected"
        assert str(invalid_none_response.value) == "Input must be a valid JSON string and cannot be empty."
        

class TestObfuscatePiiFields:

    def test_function_handles_missing_values_with_fillna(self):
        
        file_path = "tests/dummy_test_data/parquet_dummy.parquet"
        parquet_df = pd.read_parquet(file_path)
        pii_fields = ['email_address']
        results = obfuscate_pii_fields(parquet_df, pii_fields)

        assert results['email_address'][1] == "MISSING VALUE"

    def test_empty_dataframe_input_returns_empty_dataframe_output_and_valueerror_message(self):

        empty_df = pd.DataFrame()
        pii_fields = ['email_address']
        result = None

        try:
            result = obfuscate_pii_fields(empty_df, pii_fields)
        except ValueError as e:
            # Testing for ValueError message
            assert str(e) == "Input DataFrame is empty. Cannot proceed with processing."

        # Testing empty df output
        if result is not None:
            assert result.empty

    def test_successful_obfuscation_with_dummy_csv_no_missing_values(self):

        file_path = "tests/dummy_test_data/csv_dummy.csv"
        with open (file_path, "r") as file:
            csv_data = pd.read_csv(file)

        pii_fields = ['name', 'email_address']
        results = obfuscate_pii_fields(csv_data, pii_fields)

        expected_name = ["******", "******", "******"]
        expected_email = ["******", "******", "******"]

        assert list(results['name']) == expected_name
        assert list(results['email_address']) == expected_email
    

    def test_successful_obfuscation_with_dummy_parquet_and_json_with_missing_values(self):

        parquet_file_path = "tests/dummy_test_data/parquet_dummy.parquet"
        json_file_path = "tests/dummy_test_data/json_dummy.json"

        parquet_file = pd.read_parquet(parquet_file_path)
        json_file = pd.read_json(json_file_path)

        pii_fields = ["name", "email_address"]

        parquet_results = obfuscate_pii_fields(parquet_file, pii_fields)
        json_results = obfuscate_pii_fields(json_file, pii_fields)

        expected_parquet_name_results = ["MISSING VALUE", "******", "******", "MISSING VALUE", "******"]
        expected_parquet_email_results = ["******", "MISSING VALUE",  "******", "******", "MISSING VALUE"]
        expected_json_name_results = ["MISSING VALUE", "******", "******", "MISSING VALUE", "******"]
        expected_json_email_results = ["******", "MISSING VALUE",  "******", "******", "MISSING VALUE"]

        assert list(parquet_results['name']) == expected_parquet_name_results
        assert list(parquet_results['email_address']) == expected_parquet_email_results
        assert list(json_results['name']) == expected_json_name_results
        assert list(json_results['email_address']) == expected_json_email_results






