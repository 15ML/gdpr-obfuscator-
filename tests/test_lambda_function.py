import pytest
import pandas as pd
from src.lambda_function import read_data

@pytest.fixture
def valid_csv_file_path():
    file_path = "tests/test_data/csv_dummy.csv"
    return file_path
class TestReadDataFunction:

    def test_function_outputs_dataframe_when_passed_csv(self, valid_csv_file_path):

        func_results = read_data(valid_csv_file_path)
        assert isinstance(func_results, pd.DataFrame)


    def test_function_has_correct_columns(self, valid_csv_file_path):

        func_results = read_data(valid_csv_file_path)
        expected_columns = [
            "student_id", "name", "course", 
            "cohort", "graduation_date", "email_address"
        ]
        assert list(func_results.columns) == expected_columns
    

    def test_read_data_correct_shape(self, valid_csv_file_path):

        func_results = read_data(valid_csv_file_path)
        expected_results = (3, 6) # 3 rows of values, 6 columns
        assert func_results.shape == expected_results


    def test_function_correct_values(self, valid_csv_file_path):

        func_results = read_data(valid_csv_file_path)
        assert func_results.iloc[0]['student_id'] == 1234
        assert func_results.iloc[0]['email_address'] == "j.smith@email.com"
        assert func_results.iloc[1]['name'] == "Jane Doe"
        assert func_results.iloc[1]['course'] == "Data Science"
        assert func_results.iloc[2]['cohort'] == "2024-09-30"
        assert func_results.iloc[2]['student_id'] == 9101


