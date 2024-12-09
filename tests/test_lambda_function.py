import pytest
import pandas as pd
from src.lambda_function import read_data

@pytest.fixture
def valid_csv_file_path():
    file_path = "tests/test_data/csv_dummy.csv"
    return file_path

class TestReadDataFunction:

    def test_read_data_function_when_passed_valid_csv(self, valid_csv_file_path):

        #file_path = "tests/test_data/csv_dummy.csv"
        func_results = read_data(valid_csv_file_path)

        assert isinstance(func_results, pd.DataFrame)
        #assert func_results


