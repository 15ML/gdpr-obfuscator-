
# GDPR Obfuscator Project

## Overview
This project is a GDPR-compliant data processing tool designed to handle sensitive data stored in files (CSV, JSON, and Parquet) located in AWS S3. The tool obfuscates Personally Identifiable Information (PII) fields while maintaining the structure and usability of the data.

## Key Features
- Supports multiple file formats: CSV, JSON, and Parquet.
- Obfuscates sensitive data to comply with GDPR requirements.
- Designed for integration with AWS S3 for secure file handling.
- Modular design with well-structured functions and tests.
- Extensively tested with pytest, including unit and integration tests.

## Requirements
- Python 3.9 or later
- AWS account with S3 access
- Libraries listed in `requirements.txt`

## Setup and Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd gdpr-obfuscator
   ```
2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure AWS credentials using environment variables or AWS CLI:
   ```bash
   aws configure
   ```

## Usage
1. Place the input files in an accessible S3 bucket.
2. Run the main script to process the data:
   ```bash
   python src/main.py --input-json <path-to-json-config>
   ```
3. The obfuscated output will be saved back to the specified S3 bucket.

## Testing
To run tests, use pytest:
```bash
pytest tests/
```

## Performance Testing
The tool is designed to handle files of up to 1MB with a runtime of less than 1 minute. For performance testing:
1. Create 1MB test files in the supported formats.
2. Use the following script to measure runtime:
   ```python
   import time

   start_time = time.time()
   # Call the main function
   elapsed_time = time.time() - start_time
   print(f"Processing completed in {elapsed_time:.2f} seconds.")
   ```

## Contributing
Contributions are welcome! Please submit pull requests with clear descriptions and ensure all tests pass before submission.

## License
This project is licensed under the MIT License.
