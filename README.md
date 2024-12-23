
# GDPR Obfuscator

The GDPR Obfuscator is a Python-based application designed to easily obfuscate Personally Identifiable Information (PII) in various file formats (CSV, JSON, and Parquet) stored in Amazon S3. This tool ensures data privacy compliance with GDPR requirements.

## Features
- **Multi-format Support**: Processes files in CSV, JSON, and Parquet formats.
- **Data Immutability**: The process of data transformations in this application does not mutate the original datasets.
- **AWS Integration**: Reads files directly from S3 buckets and produces results compatible for S3 write operations.
- **Customizable**: Specify sensitive data fields to obfuscate using input parameters.
- **Robust Testing**: Comprehensive unit and integration tests using `pytest`.

---

## Setup and Installation

Follow these steps to set up and use the application:

### 1. Clone the Repository
First, clone the repository to your local machine using the following command:

```bash
git clone <replace-with-repository-url>
cd gdpr-obfuscator
```

### 2. Configure AWS Credentials
There are two ways to ensure your AWS credentials are configured properly in this application as it looks at two sources for credentials.
You can either configure the credentials using the AWS CLI or a local .env file. 

Entering credentials using the AWS CLI:

```bash
aws configure
```

Alternatively, you can create a `.env` file and define your AWS credentials:

```
AWS_ACCESS_KEY_ID=<replace-with-your-access-key-id>
AWS_SECRET_ACCESS_KEY=<replace-with-your-secret-access-key>
AWS_REGION=<replace-with-your-region>
```
Make sure the .env file is placed in the root of the repository to avoid possible errors.

### 3. Set Up the Application Using Make
Run the following command to automatically set up the application and virtual environment:

```bash
make all
```

This will:
1. Load environment variables from the `.env` file (if present).
2. Create a virtual environment.
3. Install all required dependencies listed in `requirements.txt`.
4. Export the `PYTHONPATH` for the application.
5. Run all tests to ensure the setup is successful.

---

## Usage

### Before Running the Application
Ensure that your dataset files are uploaded to an accessible S3 bucket before running the application. Double-check that policies are in place, such as the permissions to read files ([s3:GetObject](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetObject.html)) from your S3 bucket.

1. **Export the Python Path**  
   Ensure the `PYTHONPATH` is correctly set by running the following command:
   ```bash
   export PYTHONPATH=$(pwd)
   ```

2. **Activate the Virtual Environment**  
   Verify that you are in the virtual environment by checking for `(venv)` in your terminal prompt. If not, activate it using:
   ```bash
   source venv/bin/activate

### Running the Application
Once the setup is complete, you will be prompted to provide a JSON object string with the following keys and values:

- **"file_to_obfuscate"**: The S3 URI pointing to the file to be obfuscated (e.g., `"s3://mybucket/myfile.csv"`).
- **"pii_fields"**: A list of fields to obfuscate (e.g., `["name", "email_address"]`).

### Example Input

Suppose the input dataset is stored in `s3://mybucket/myfile.csv` and contains the following data:

| student_id | name        | course                | cohort   | graduation_date | email_address       |
|------------|-------------|-----------------------|----------|-----------------|---------------------|
| 101        | Alice Smith | Data Engineering      | Data     | 2023-06-15      | alice@example.com   |
| 102        | Bob Jones   | Software Development  | Software | 2023-12-01      | bob@example.com     |
| 103        | Charlie Tay | Data Engineering      | Data     | 2022-05-20      |                     |

The user specifies the following JSON object string for obfuscation:

```json
{
  "file_to_obfuscate": "s3://mybucket/myfile.csv",
  "pii_fields": ["name", "email_address"]
}
```

---

### Example Obfuscated Output

After running the application, the obfuscated dataset might look like this:

| student_id | name       | course                | cohort   | graduation_date | email_address       |
|------------|------------|-----------------------|----------|-----------------|---------------------|
| 101        | ******     | Data Engineering      | Data     | 2023-06-15      | ******              |
| 102        | ******     | Software Development  | Software | 2023-12-01      | ******              |
| 103        | ******     | Data Engineering      | Data     | 2022-05-20      | MISSING VALUES      |

The fields specified in `pii_fields` are obfuscated by replacing their values with `******` or `MISSING VALUES` for any missing data. The application purposely returns the processed data as a byte-stream object, which is compatible for uploading to an AWS S3 bucket. 

The byte-stream representation for the obfuscated dataset might look like this:

```plaintext
student_id,name,course,cohort,graduation_date,email_address
101,******,Data Engineering,Data,2023-06-15,******
102,******,Software Development,Software,2023-12-01,******
103,******,Data Engineering,Data,2022-05-20,MISSING VALUES
```

---

### Predefined Example

To see a pre-existing example, run:

   ```bash
   python src/main.py
   ```

The predefined example is located in src/main.py at lines 67 and 68. This demonstrates the application using a sample dummy dataset stored in an S3 bucket. To customize this example for your own data, update the S3 URI and pii_fields values accordingly to point to your dataset and specify the fields you wish to obfuscate.

---

## Testing

### Running Tests
All tests would have been run with the "make all" command on setup. However, if you'd like to run all tests again, you can do so by using the following command:

```bash
make run-tests
```

This will execute the test suite with `pytest` and display results in a readable format using Testdox.

### Test Suite
The test suite includes:
- **Unit Tests**: Validate individual functions and modules.
- **Integration Tests**: Verify the end-to-end functionality of the application.

---

## Python Version

This project is developed and tested using Python **3.12.7**. Ensure you have this version installed to avoid compatibility issues.

If you need to manage multiple Python versions on your system, consider using a version manager like [pyenv](https://github.com/pyenv/pyenv).

### Verify Your Python Version

To check your current Python version, run:

```bash
python --version
```

If you don’t have Python 3.12.7 installed, you can download it from the [official Python website](https://www.python.org/downloads/).

---

## Dependencies
The project requires the following Python libraries:
- `boto3==1.35.83`: AWS SDK for Python.
- `botocore==1.35.83`: Core library for AWS SDK.
- `moto==5.0.23`: AWS mocking library for testing.
- `pandas==2.2.3`: Data manipulation and analysis.
- `pytest==8.3.4`: Testing framework.
- `python-dotenv==0.19.0`: Load environment variables from a `.env` file.

---

## Future Improvements
As applications continue to develop and improve, some of the many few things that could be added are:
- **Expand Input Flexibility**: Currently, the application only accepts JSON strings of the S3 location and fields to obfuscate. Future updates could allow for non-JSON strings and local machine file path support.
- **Improve Obfuscation Ability**: Currently, the application only obfuscates string values. Enhancements could include obfuscating other data types, such as dates for DOBs or mixed data for postal codes.
- **Infrastructure as Code**: The application could be implemented with cloud technologies (e.g., AWS Terraform) for scalability, efficiency, and automation.
- **Output Visual Tools**: Automate visual tools for output, such as Tableau or Power BI.

## Final Thoughts

Thank you for checking out this application! If you found it useful or have any suggestions for improvement, feel free to reach out or contribute. Your feedback is always appreciated.

## Contact

- Email: mike.work.5881@gmail.com
- LinkedIn: [My LinkedIn Profile](https://www.linkedin.com/in/michael-lee-5358849a/)
