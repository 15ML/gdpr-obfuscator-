import pandas as pd
# import os
import pg8000
from credentials_handler import get_credentials

def connect_to_db():
    """
    Connects to the database and returns the connection object.
    Uncomment for real database
    
    credentials = get_credentials()
    conn = pg8000.connect(user=credentials['username'], password=credentials['password'], host=credentials['host'],
                          port=credentials['port'], database=credentials['dbname'])
    
    return conn
    """
    
    """
    Fetches the file path from credentials.py and loads the CSV file into a Pandas DataFrame.
    """
    credentials = get_credentials()  # Get the placeholder credentials
    file_path = credentials["file_path"]  # Extract the file path

    return file_path
