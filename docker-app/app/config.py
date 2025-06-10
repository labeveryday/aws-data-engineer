"""
Configuration settings for the AWS Data Engineer Course application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# AWS Configuration
AWS_PROFILE = os.getenv("AWS_PROFILE", "default")
BEDROCK_REGION = os.getenv("BEDROCK_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")

# Application Configuration
APP_TITLE = "AWS Data Engineer Course"
APP_ICON = "📊"

# Content Paths
STUDY_GUIDE_PATH = "content/study-guide"
LABS_PATH = "content/labs"

# Define domains and their weights
DOMAINS = {
    "domain1": {
        "title": "Data Ingestion and Transformation",
        "weight": "30-35%",
        "file": "01-data-ingestion-transformation.md"
    },
    "domain2": {
        "title": "Storage and Data Management",
        "weight": "30-35%",
        "file": "02-storage-data-management.md"
    },
    "domain3": {
        "title": "Data Security and Access Control",
        "weight": "15-20%",
        "file": "03-data-security-access-control.md"
    },
    "domain4": {
        "title": "Data Operations and Optimization",
        "weight": "15-20%",
        "file": "04-data-operations-optimization.md"
    }
}

# Define labs
LABS = {
    "lab1_1": {
        "title": "Batch Data Ingestion with AWS Glue",
        "file": "data-ingestion/lab-1.1-batch-ingestion-glue.md",
        "domain": "domain1"
    },
    "lab1_2": {
        "title": "Streaming Data with Amazon Kinesis",
        "file": "data-ingestion/lab-1.2-streaming-kinesis.md",
        "domain": "domain1"
    },
    "lab1_3": {
        "title": "Database Migration with AWS DMS",
        "file": "data-ingestion/lab-1.3-database-migration-dms.md",
        "domain": "domain1"
    },
    "lab2_1": {
        "title": "S3 Data Lake Organization",
        "file": "data-storage/lab-2.1-s3-data-lake.md",
        "domain": "domain2"
    },
    "lab2_2": {
        "title": "Amazon Redshift Data Warehouse Setup",
        "file": "data-storage/lab-2.2-redshift-warehouse.md",
        "domain": "domain2"
    },
    "lab2_3": {
        "title": "DynamoDB NoSQL Database Design",
        "file": "data-storage/lab-2.3-dynamodb-nosql.md",
        "domain": "domain2"
    },
    "lab3_1": {
        "title": "ETL with AWS Glue",
        "file": "data-transformation/lab-3.1-etl-glue.md",
        "domain": "domain1"
    },
    "lab3_2": {
        "title": "Stream Processing with Kinesis Analytics",
        "file": "data-transformation/lab-3.2-stream-processing.md",
        "domain": "domain1"
    },
    "lab3_3": {
        "title": "Data Quality and Validation",
        "file": "data-transformation/lab-3.3-data-quality.md",
        "domain": "domain1"
    },
    "lab4_1": {
        "title": "Data Governance with AWS Lake Formation",
        "file": "security-governance/lab-4.1-lake-formation.md",
        "domain": "domain3"
    },
    "lab4_2": {
        "title": "Column-Level Security",
        "file": "security-governance/lab-4.2-column-security.md",
        "domain": "domain3"
    },
    "lab4_3": {
        "title": "Cross-Account Data Sharing",
        "file": "security-governance/lab-4.3-cross-account.md",
        "domain": "domain3"
    },
    "lab5_1": {
        "title": "Pipeline Orchestration with AWS Step Functions",
        "file": "operations-optimization/lab-5.1-step-functions.md",
        "domain": "domain4"
    },
    "lab5_2": {
        "title": "Monitoring and Alerting",
        "file": "operations-optimization/lab-5.2-monitoring.md",
        "domain": "domain4"
    },
    "lab5_3": {
        "title": "Cost Optimization Strategies",
        "file": "operations-optimization/lab-5.3-cost-optimization.md",
        "domain": "domain4"
    }
}
