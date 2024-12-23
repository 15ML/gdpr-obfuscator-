import json
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


def read_json_input(json_string):
    """
    Parse a JSON string to extract 'file_to_obfuscate' and 'pii_fields'.

    Args:
        json_string (str): A JSON string containing the keys 'file_to_obfuscate' and 'pii_fields'.

    Returns:
        tuple: A tuple containing the file path and a list of PII fields to be obfuscated.

    Raises:
        ValueError: If the input string is not a valid JSON, if required keys are missing,
                    or if the file type is not supported.
    """
    if not isinstance(json_string, str) or not json_string.strip():
        logging.error("Provided JSON string is empty or not valid.")
        raise ValueError(
            "Input must be a valid JSON string and cannot be empty."
        )

    try:
        input_data = json.loads(json_string)
    except json.JSONDecodeError:
        logging.error("JSON decoding has failed.")
        raise ValueError("Input is not a valid JSON format as expected")

    file_to_obfuscate = input_data.get("file_to_obfuscate")
    pii_fields = input_data.get("pii_fields")

    if not file_to_obfuscate or not pii_fields:
        logging.error("'file_to_obfuscate' or 'pii_fields' not provided.")
        raise ValueError(
            "Invalid input: 'file_to_obfuscate' and 'pii_fields' are required."
        )

    if not file_to_obfuscate.startswith("s3://"):
        logging.error("File path does not start with 's3://'.")
        raise ValueError("Invalid S3 path in 'file_to_obfuscate'.")

    _, file_type = file_to_obfuscate.rsplit(".", 1)
    file_type = file_type.lower()
    if file_type not in ["csv", "parquet", "json"]:
        logging.error(f"Unsupported file type: {file_type}")
        raise ValueError(
            f"Unsupported file type: {file_type}. Supported types are csv, parquet, and json."
        )

    return file_to_obfuscate, pii_fields


def obfuscate_pii_fields(df: pd.DataFrame, pii_fields):
    """
    Obfuscate specified fields in a DataFrame by replacing values with asterisks.

    Args:
        df (pd.DataFrame): The DataFrame to obfuscate.
        pii_fields (list): A list of columns in the DataFrame that contain personally identifiable information.

    Returns:
        pd.DataFrame: The obfuscated DataFrame.

    Raises:
        ValueError: If the DataFrame is empty or if specified columns are missing.
    """
    if df.empty:
        logging.error("Provided DataFrame is empty.")
        raise ValueError(
            "Input DataFrame is empty. Cannot proceed with processing."
        )

    missing_columns = [col for col in pii_fields if col not in df.columns]
    if missing_columns:
        logging.error(f"Missing columns: {', '.join(missing_columns)}")
        raise ValueError(
            f"The following columns to obfuscate are missing in the DataFrame provided. Missing columns: {', '.join(missing_columns)}"
        )

    df = df.copy()
    try:
        for column in pii_fields:
            df[column] = np.where(
                df[column].isnull(), "MISSING VALUE", "******"
            )
        return df
    except Exception as e:
        logging.error(f"Error obfuscating data: {e}")
        raise Exception(f"Error obfuscating data! Error: {e}")
