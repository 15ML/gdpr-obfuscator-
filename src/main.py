from src.file_handling import download_s3_file_and_convert_to_pandas_dataframe, dataframe_to_bytes
from src.utils import read_json_input, obfuscate_pii_fields

def main(input_json):
    try:
        # Parse the input JSON
        file_path, pii_fields = read_json_input(input_json)
        
        # Download the file and convert to a DataFrame
        df = download_s3_file_and_convert_to_pandas_dataframe(file_path)
        
        # Obfuscate specified fields
        obfuscated_df = obfuscate_pii_fields(df, pii_fields)
        
        # Convert the obfuscated DataFrame back to bytes
        file_type = file_path.split('.')[-1]  # Assumes the format is the file extension
        result_bytes = dataframe_to_bytes(obfuscated_df, file_type)
        
        return result_bytes
    except Exception as e:
        print(f"An error occurred: {e}")
        # Optionally re-raise the exception if you want the error to propagate
        raise
