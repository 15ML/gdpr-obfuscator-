import logging
from src.file_handling import (
    download_s3_file_and_convert_to_pandas_dataframe,
    dataframe_to_bytes,
)
from src.utils import read_json_input, obfuscate_pii_fields

# Configure logging
logging.basicConfig(level=logging.INFO)


def main(input_json):
    """
    Main function to process an input JSON, download the specified file,
    obfuscate PII fields, and return the obfuscated file as bytes.

    Args:
        input_json (str): A JSON string specifying the file path and PII fields to obfuscate.

    Returns:
        bytes: The obfuscated file content in its original format.

    Raises:
        Exception: If any error occurs during the process.
    """
    try:
        logging.info("Starting the obfuscation process.")

        # Parse the input JSON
        logging.info("Parsing input JSON.")
        file_path, pii_fields = read_json_input(input_json)

        # Download the file and convert to a DataFrame
        logging.info(
            f"Downloading and converting file from S3 path: {file_path}."
        )
        df = download_s3_file_and_convert_to_pandas_dataframe(file_path)

        # Obfuscate specified fields
        logging.info(f"Obfuscating PII fields: {pii_fields}.")
        obfuscated_df = obfuscate_pii_fields(df, pii_fields)

        # Convert the obfuscated DataFrame back to bytes
        file_type = file_path.split(".")[
            -1
        ].lower()  # Assumes the format is the file extension
        logging.info(
            f"Converting obfuscated DataFrame to bytes for file type: {file_type}."
        )
        result_bytes = dataframe_to_bytes(obfuscated_df, file_type)

        logging.info("Obfuscation process completed successfully.")
        return result_bytes

    except Exception as e:
        logging.error(
            f"An error occurred during the obfuscation process: {e}",
            exc_info=True,
        )
        # Optionally re-raise the exception if you want the error to propagate
        raise
