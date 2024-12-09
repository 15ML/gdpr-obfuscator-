# Initiate provider as AWS Terraform
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

# Create a S3 bucket for initial raw data
resource "aws_s3_bucket" "raw_bucket" {
  bucket = "gdpr-raw-data"

  tags = {
    Environment = "Dev"
    Project = "GDPR-Obfuscator"
  }
}

# Create a S3 bucket for processed data
resource "aws_s3_bucket" "processed_bucket" {
  bucket = "gdpr-processed-data"

  tags = {
    Environment = "Dev"
    Project = "GDPR-Obfuscator"
  }
}

# Create IAM role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    Environment = "dev"
    Project = "GDPR-Obfuscator"
  }
}

# Create Lambda IAM role policy for S3 and Cloudwatch 
resource "aws_iam_policy" "lambda_role_policy" {
  name        = "lambda-iam-policy"
  #path        = "/"
  description = "IAM role policy for Lambda to access S3 and Cloudwatch logging"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
    # Allows Lambda to read from raw bucket
        {
        "Effect": "Allow",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::gdpr-raw-data/*"
      },
    # Allows Lambda to read and write to/from processed bucket
        {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::gdpr-processed-data/*"
    },
    # Allows Lambda to keep logs in AWS Cloudwatch
        {
        "Effect": "Allow",
        "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*"
    }
    ]
  })
    tags = {
    Environment = "dev"
    Project = "GDPR-Obfuscator"
  }
}

# Attach the specified IAM policy to the Lambda IAM role
resource "aws_iam_role_policy_attachment" "iam-role-attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_role_policy.arn
}

# Create the actual Lambda function
resource "aws_lambda_function" "gdpr-lambda"{
  function_name = "gdpr-lambda-obfuscator"
  role = aws_iam_role.lambda_role.arn
  filename = "${path.module}/../src/lambda/lambda_function.zip"
  #filename = "${path.module}/../lambda_function.zip"
  #filename = "${path.module}/src/lambda/lambda_function.zip"
  handler = "lambda_function.lambda_handler"
  runtime = "python3.9"
}