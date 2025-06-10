# Lab 5.1: Pipeline Orchestration with AWS Step Functions

## Overview
This lab focuses on building and orchestrating data pipelines using AWS Step Functions. You will learn how to design, implement, and monitor complex data workflows with error handling and retry logic, which are essential skills for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Design state machines for data pipeline orchestration
- Implement error handling and retry mechanisms
- Coordinate multiple AWS services in a workflow
- Monitor and troubleshoot pipeline execution
- Implement dynamic branching based on data conditions
- Create reusable workflow components

**AWS Services Used:**
- AWS Step Functions
- AWS Lambda
- Amazon S3
- AWS Glue
- Amazon SNS
- AWS Identity and Access Management (IAM)
- Amazon CloudWatch

**Estimated Time:** 3 hours

**Estimated Cost:** $5-10 (Most resources fall under Free Tier if available)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for Step Functions, Lambda, S3, Glue, and SNS
- Basic understanding of state machines and workflow concepts
- Familiarity with JSON for state machine definitions
- Basic Python knowledge for Lambda functions

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│  S3 Event   │────▶│  Lambda     │────▶│  Step       │
│  Trigger    │     │  Function   │     │  Functions  │
│             │     │             │     │  Workflow   │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              │
                                              ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│  AWS Glue   │◀───▶│  Lambda     │◀───▶│  Amazon     │
│  Jobs       │     │  Functions  │     │  SNS        │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              │
                                              ▼
                                        ┌─────────────┐
                                        │             │
                                        │  CloudWatch │
                                        │  Monitoring │
                                        │             │
                                        └─────────────┘
```

## Implementation Steps

### Step 1: Create S3 Buckets for Data Pipeline
1. Sign in to the AWS Management Console and navigate to the S3 service
2. Create a bucket for source data (e.g., `your-name-pipeline-source-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-pipeline-source-YYYYMMDD
   ```
3. Create a bucket for processed data (e.g., `your-name-pipeline-processed-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-pipeline-processed-YYYYMMDD
   ```
4. Create a bucket for pipeline artifacts (e.g., `your-name-pipeline-artifacts-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-pipeline-artifacts-YYYYMMDD
   ```

### Step 2: Create an SNS Topic for Notifications
1. Navigate to the Amazon SNS console
2. Click "Create topic"
3. Select "Standard" type
4. Name the topic `pipeline-notifications`
5. Create the topic
6. Create a subscription for the topic:
   - Protocol: Email
   - Endpoint: Your email address
7. Confirm the subscription by clicking the link in the email you receive

### Step 3: Create Lambda Functions for the Pipeline
1. Navigate to the AWS Lambda console
2. Create the following Lambda functions:

#### a. File Validation Function
```python
import json
import boto3
import os
import csv
from io import StringIO

def lambda_handler(event, context):
    # Get bucket and key from the event
    bucket = event['bucket']
    key = event['key']
    
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    try:
        # Get the file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        
        # Check file type
        if key.endswith('.csv'):
            # Validate CSV structure
            csv_reader = csv.reader(StringIO(file_content))
            header = next(csv_reader)
            row_count = sum(1 for _ in csv_reader)
            
            # Check if file has content
            if row_count == 0:
                return {
                    'statusCode': 400,
                    'isValid': False,
                    'error': 'File is empty',
                    'bucket': bucket,
                    'key': key
                }
            
            return {
                'statusCode': 200,
                'isValid': True,
                'fileType': 'csv',
                'rowCount': row_count,
                'bucket': bucket,
                'key': key
            }
        elif key.endswith('.json'):
            # Validate JSON structure
            try:
                data = json.loads(file_content)
                record_count = len(data) if isinstance(data, list) else 1
                
                return {
                    'statusCode': 200,
                    'isValid': True,
                    'fileType': 'json',
                    'recordCount': record_count,
                    'bucket': bucket,
                    'key': key
                }
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'isValid': False,
                    'error': 'Invalid JSON format',
                    'bucket': bucket,
                    'key': key
                }
        else:
            return {
                'statusCode': 400,
                'isValid': False,
                'error': 'Unsupported file type',
                'bucket': bucket,
                'key': key
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'isValid': False,
            'error': str(e),
            'bucket': bucket,
            'key': key
        }
```

#### b. Start Glue Job Function
```python
import json
import boto3
import time

def lambda_handler(event, context):
    # Get parameters from the event
    bucket = event['bucket']
    key = event['key']
    file_type = event.get('fileType', 'unknown')
    
    # Initialize Glue client
    glue = boto3.client('glue')
    
    # Determine which Glue job to run based on file type
    if file_type == 'csv':
        job_name = 'process-csv-data'
    elif file_type == 'json':
        job_name = 'process-json-data'
    else:
        return {
            'statusCode': 400,
            'error': f'No Glue job defined for file type: {file_type}',
            'bucket': bucket,
            'key': key
        }
    
    try:
        # Start the Glue job
        response = glue.start_job_run(
            JobName=job_name,
            Arguments={
                '--source_bucket': bucket,
                '--source_key': key,
                '--target_bucket': 'your-name-pipeline-processed-YYYYMMDD'
            }
        )
        
        job_run_id = response['JobRunId']
        
        return {
            'statusCode': 200,
            'jobName': job_name,
            'jobRunId': job_run_id,
            'bucket': bucket,
            'key': key
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e),
            'bucket': bucket,
            'key': key
        }
```

#### c. Check Job Status Function
```python
import json
import boto3

def lambda_handler(event, context):
    # Get parameters from the event
    job_name = event['jobName']
    job_run_id = event['jobRunId']
    
    # Initialize Glue client
    glue = boto3.client('glue')
    
    try:
        # Get the job run status
        response = glue.get_job_run(
            JobName=job_name,
            RunId=job_run_id
        )
        
        job_status = response['JobRun']['JobRunState']
        
        return {
            'statusCode': 200,
            'jobName': job_name,
            'jobRunId': job_run_id,
            'jobStatus': job_status,
            'isComplete': job_status in ['SUCCEEDED', 'FAILED', 'STOPPED', 'TIMEOUT'],
            'isSuccessful': job_status == 'SUCCEEDED'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e),
            'jobName': job_name,
            'jobRunId': job_run_id
        }
```

#### d. Send Notification Function
```python
import json
import boto3

def lambda_handler(event, context):
    # Get parameters from the event
    status = event.get('status', 'Unknown')
    details = event.get('details', {})
    
    # Initialize SNS client
    sns = boto3.client('sns')
    
    # Prepare the message
    subject = f"Data Pipeline Notification: {status}"
    message = f"Pipeline Status: {status}\n\nDetails:\n{json.dumps(details, indent=2)}"
    
    try:
        # Send the notification
        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:pipeline-notifications',
            Subject=subject,
            Message=message
        )
        
        return {
            'statusCode': 200,
            'messageId': response['MessageId'],
            'status': status
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e),
            'status': status
        }
```

3. Configure each Lambda function:
   - Runtime: Python 3.9
   - Timeout: 30 seconds
   - Memory: 128 MB
   - Execution role: Create a new role with appropriate permissions

### Step 4: Create AWS Glue Jobs
1. Navigate to the AWS Glue console
2. Create the following Glue jobs:

#### a. Process CSV Data Job
```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as F

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'source_bucket', 'source_key', 'target_bucket'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Get parameters
source_bucket = args['source_bucket']
source_key = args['source_key']
target_bucket = args['target_bucket']

# Extract file name without extension
file_name = source_key.split('/')[-1].split('.')[0]

# Read CSV data
source_path = f"s3://{source_bucket}/{source_key}"
df = spark.read.option("header", "true").option("inferSchema", "true").csv(source_path)

# Apply transformations
transformed_df = df.withColumn("processing_date", F.current_date())

# Convert to Glue DynamicFrame
dynamic_frame = DynamicFrame.fromDF(transformed_df, glueContext, "dynamic_frame")

# Write to target in Parquet format
target_path = f"s3://{target_bucket}/processed/{file_name}"
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={"path": target_path},
    format="parquet"
)

job.commit()
```

#### b. Process JSON Data Job
```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as F

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'source_bucket', 'source_key', 'target_bucket'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Get parameters
source_bucket = args['source_bucket']
source_key = args['source_key']
target_bucket = args['target_bucket']

# Extract file name without extension
file_name = source_key.split('/')[-1].split('.')[0]

# Read JSON data
source_path = f"s3://{source_bucket}/{source_key}"
df = spark.read.json(source_path)

# Apply transformations
transformed_df = df.withColumn("processing_date", F.current_date())

# Convert to Glue DynamicFrame
dynamic_frame = DynamicFrame.fromDF(transformed_df, glueContext, "dynamic_frame")

# Write to target in Parquet format
target_path = f"s3://{target_bucket}/processed/{file_name}"
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={"path": target_path},
    format="parquet"
)

job.commit()
```

3. Configure each Glue job:
   - Type: Spark
   - Glue version: Glue 3.0
   - Worker type: G.1X
   - Number of workers: 2
   - Job parameters: (leave empty, they will be passed from Step Functions)

### Step 5: Create the Step Functions State Machine
1. Navigate to the AWS Step Functions console
2. Click "Create state machine"
3. Choose "Write your workflow in code"
4. Use the following Amazon States Language (ASL) definition:

```json
{
  "Comment": "Data Processing Pipeline",
  "StartAt": "ValidateFile",
  "States": {
    "ValidateFile": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:file-validation-function",
      "Next": "FileValidationChoice",
      "Retry": [
        {
          "ErrorEquals": ["Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException"],
          "IntervalSeconds": 2,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "ResultPath": "$.error",
          "Next": "NotifyFailure"
        }
      ]
    },
    "FileValidationChoice": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.isValid",
          "BooleanEquals": true,
          "Next": "StartGlueJob"
        }
      ],
      "Default": "NotifyInvalidFile"
    },
    "NotifyInvalidFile": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:send-notification-function",
      "Parameters": {
        "status": "File Validation Failed",
        "details.$": "$"
      },
      "End": true
    },
    "StartGlueJob": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:start-glue-job-function",
      "Next": "WaitForJobCompletion",
      "Retry": [
        {
          "ErrorEquals": ["Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException"],
          "IntervalSeconds": 2,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "ResultPath": "$.error",
          "Next": "NotifyFailure"
        }
      ]
    },
    "WaitForJobCompletion": {
      "Type": "Wait",
      "Seconds": 30,
      "Next": "CheckJobStatus"
    },
    "CheckJobStatus": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:check-job-status-function",
      "Next": "JobCompletionChoice",
      "Retry": [
        {
          "ErrorEquals": ["Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException"],
          "IntervalSeconds": 2,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "ResultPath": "$.error",
          "Next": "NotifyFailure"
        }
      ]
    },
    "JobCompletionChoice": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.isComplete",
          "BooleanEquals": true,
          "Next": "JobSuccessChoice"
        }
      ],
      "Default": "WaitForJobCompletion"
    },
    "JobSuccessChoice": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.isSuccessful",
          "BooleanEquals": true,
          "Next": "NotifySuccess"
        }
      ],
      "Default": "NotifyFailure"
    },
    "NotifySuccess": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:send-notification-function",
      "Parameters": {
        "status": "Pipeline Completed Successfully",
        "details.$": "$"
      },
      "End": true
    },
    "NotifyFailure": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:send-notification-function",
      "Parameters": {
        "status": "Pipeline Failed",
        "details.$": "$"
      },
      "End": true
    }
  }
}
```

4. Replace `YOUR_ACCOUNT_ID` with your actual AWS account ID
5. Replace the Lambda function ARNs with the actual ARNs of your functions
6. Configure the state machine:
   - Type: Standard
   - Name: `data-processing-pipeline`
   - Permissions: Create new role
7. Create the state machine

### Step 6: Create a Lambda Function to Trigger the Pipeline
1. Create a new Lambda function named `trigger-pipeline-function`:

```python
import json
import boto3
import urllib.parse

def lambda_handler(event, context):
    # Get the S3 event details
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # Initialize Step Functions client
    sfn = boto3.client('stepfunctions')
    
    # Prepare input for the state machine
    input_data = {
        'bucket': bucket,
        'key': key
    }
    
    try:
        # Start the state machine execution
        response = sfn.start_execution(
            stateMachineArn='arn:aws:states:us-east-1:YOUR_ACCOUNT_ID:stateMachine:data-processing-pipeline',
            name=f"execution-{key.replace('/', '-')}",
            input=json.dumps(input_data)
        )
        
        return {
            'statusCode': 200,
            'executionArn': response['executionArn'],
            'bucket': bucket,
            'key': key
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'error': str(e),
            'bucket': bucket,
            'key': key
        }
```

2. Replace `YOUR_ACCOUNT_ID` with your actual AWS account ID
3. Configure the function with appropriate permissions

### Step 7: Set Up S3 Event Trigger
1. Navigate to the S3 console
2. Select your source bucket
3. Go to "Properties" > "Event notifications"
4. Create a new event notification:
   - Name: `trigger-pipeline`
   - Event types: Select "All object create events"
   - Destination: Lambda function
   - Lambda function: `trigger-pipeline-function`
5. Save the event notification

### Step 8: Test the Pipeline
1. Create sample CSV and JSON files for testing:

**sample_data.csv**:
```
id,name,age,city
1,John Doe,30,New York
2,Jane Smith,25,San Francisco
3,Robert Johnson,35,Chicago
4,Sarah Williams,28,Seattle
5,Michael Brown,40,Boston
```

**sample_data.json**:
```json
[
  {"id": 1, "name": "John Doe", "age": 30, "city": "New York"},
  {"id": 2, "name": "Jane Smith", "age": 25, "city": "San Francisco"},
  {"id": 3, "name": "Robert Johnson", "age": 35, "city": "Chicago"},
  {"id": 4, "name": "Sarah Williams", "age": 28, "city": "Seattle"},
  {"id": 5, "name": "Michael Brown", "age": 40, "city": "Boston"}
]
```

2. Upload these files to your source S3 bucket:
   ```
   aws s3 cp sample_data.csv s3://your-name-pipeline-source-YYYYMMDD/incoming/
   aws s3 cp sample_data.json s3://your-name-pipeline-source-YYYYMMDD/incoming/
   ```

3. Monitor the Step Functions execution in the console
4. Check your email for notifications
5. Verify that the processed data is available in the target S3 bucket

### Step 9: Monitor and Analyze the Pipeline
1. Navigate to the CloudWatch console
2. Create a dashboard for your pipeline:
   - Add widgets for Lambda function metrics
   - Add widgets for Glue job metrics
   - Add widgets for Step Functions execution metrics
3. Set up CloudWatch alarms for critical metrics:
   - Lambda function errors
   - Glue job failures
   - Step Functions execution failures

## Validation Steps
1. Verify that the pipeline is triggered when files are uploaded to S3
2. Confirm that file validation correctly identifies valid and invalid files
3. Check that Glue jobs process the data as expected
4. Verify that notifications are sent for success and failure cases
5. Confirm that the processed data is correctly stored in the target bucket
6. Check that error handling and retry mechanisms work as expected

## Cleanup Instructions
1. Delete the S3 event notification
2. Delete the Lambda functions
   ```
   aws lambda delete-function --function-name file-validation-function
   aws lambda delete-function --function-name start-glue-job-function
   aws lambda delete-function --function-name check-job-status-function
   aws lambda delete-function --function-name send-notification-function
   aws lambda delete-function --function-name trigger-pipeline-function
   ```
3. Delete the Glue jobs
   ```
   aws glue delete-job --job-name process-csv-data
   aws glue delete-job --job-name process-json-data
   ```
4. Delete the Step Functions state machine
   ```
   aws stepfunctions delete-state-machine --state-machine-arn arn:aws:states:us-east-1:YOUR_ACCOUNT_ID:stateMachine:data-processing-pipeline
   ```
5. Delete the SNS topic and subscription
   ```
   aws sns delete-topic --topic-arn arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:pipeline-notifications
   ```
6. Delete the S3 buckets and their contents
   ```
   aws s3 rb s3://your-name-pipeline-source-YYYYMMDD --force
   aws s3 rb s3://your-name-pipeline-processed-YYYYMMDD --force
   aws s3 rb s3://your-name-pipeline-artifacts-YYYYMMDD --force
   ```
7. Delete the CloudWatch dashboard and alarms

## Challenge Extensions (Optional)
1. Add parallel processing for multiple files
2. Implement dynamic branching based on file content
3. Add data quality checks and validation steps
4. Create a custom dashboard for pipeline monitoring
5. Implement cross-account data processing
6. Add human approval steps for certain conditions

## Additional Resources
- [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [AWS Step Functions Workshop](https://catalog.workshops.aws/step-functions/en-US)
- [Designing Serverless Data Processing Pipelines](https://aws.amazon.com/blogs/compute/designing-serverless-data-processing-pipelines/)
- [Error Handling in Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)

## Notes and Tips
- Use Map states for parallel processing of multiple items
- Implement appropriate error handling at each step
- Use CloudWatch Logs for debugging and troubleshooting
- Consider using Step Functions Express Workflows for high-volume, short-duration workflows
- Use Parameters and ResultSelector to shape the data between states
- Implement appropriate timeouts for long-running processes
- Use CloudWatch Events to trigger workflows on a schedule
