# Lab 5.2: Monitoring and Alerting

## Overview
This lab focuses on implementing comprehensive monitoring and alerting for data pipelines. You will learn how to set up monitoring for various AWS data services, create dashboards, configure alerts, and respond to issues, which are essential skills for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Set up CloudWatch metrics and alarms for data services
- Create custom metrics for data pipeline monitoring
- Implement operational dashboards
- Configure alerting for critical issues
- Set up log analysis for troubleshooting
- Implement automated responses to common issues
- Monitor data quality and pipeline health

**AWS Services Used:**
- Amazon CloudWatch
- AWS Lambda
- Amazon SNS
- Amazon EventBridge
- AWS X-Ray (optional)
- AWS CloudTrail
- Various data services (Glue, Redshift, Kinesis, etc.)

**Estimated Time:** 3 hours

**Estimated Cost:** $5-10 (Most resources fall under Free Tier if available)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for CloudWatch, Lambda, SNS, and data services
- Basic understanding of monitoring concepts
- Familiarity with AWS data services
- Basic knowledge of Python for Lambda functions

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │     │             │
│  AWS Data   │────▶│  CloudWatch │────▶│  CloudWatch │────▶│  Amazon SNS │
│  Services   │     │  Metrics    │     │  Alarms     │     │  Topics     │
│             │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                    │                    │
                          │                    │                    │
                          ▼                    ▼                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │     │             │
│  CloudWatch │◀───▶│  CloudWatch │◀───▶│  Lambda     │◀───▶│  EventBridge│
│  Logs       │     │  Dashboard  │     │  Functions  │     │  Rules      │
│             │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## Implementation Steps

### Step 1: Set Up a Sample Data Pipeline
1. For this lab, we'll set up a simple data pipeline using AWS Glue to monitor
2. Navigate to the AWS Glue console
3. Create a new Glue database named `monitoring_lab_db`
4. Create a simple Glue ETL job:
   - Name: `sample-etl-job`
   - IAM role: Create or select a role with appropriate permissions
   - Type: Spark
   - Glue version: Glue 3.0
   - Script:

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import time
import random

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Simulate processing with random duration and occasional failures
processing_time = random.randint(30, 120)
print(f"Processing will take approximately {processing_time} seconds")

# Simulate data processing
records_processed = 0
for i in range(processing_time):
    # Process some records
    batch_size = random.randint(10, 100)
    records_processed += batch_size
    print(f"Processed {batch_size} records. Total: {records_processed}")
    
    # Simulate occasional errors
    if random.random() < 0.05:  # 5% chance of error
        print("WARNING: Encountered processing error, retrying...")
        time.sleep(5)
    
    time.sleep(1)

# Simulate occasional job failure
if random.random() < 0.1:  # 10% chance of failure
    print("ERROR: Critical failure in data processing")
    sys.exit(1)

print(f"Job completed successfully. Processed {records_processed} records.")
job.commit()
```

5. Save and create the job

### Step 2: Set Up CloudWatch Metrics and Alarms

#### 2.1: Create CloudWatch Alarms for Glue Job
1. Navigate to the CloudWatch console
2. Go to "Alarms" > "All alarms" and click "Create alarm"
3. Click "Select metric"
4. Choose "Glue" > "Job Metrics"
5. Select the metric `glue.driver.aggregate.elapsedTime` for your job
6. Click "Select metric"
7. Configure the alarm:
   - Statistic: Maximum
   - Period: 5 minutes
   - Threshold type: Static
   - Condition: Greater than
   - Threshold value: 300 (seconds)
8. Click "Next"
9. For notification:
   - Select "Create new topic"
   - Topic name: `data-pipeline-alerts`
   - Email endpoint: Your email address
10. Click "Create topic"
11. Click "Next"
12. Name the alarm: `GlueJobDurationAlarm`
13. Click "Next" and then "Create alarm"
14. Confirm the SNS subscription in your email

#### 2.2: Create Additional Alarms
1. Create an alarm for Glue job failures:
   - Metric: `glue.driver.aggregate.numFailedTasks`
   - Statistic: Sum
   - Period: 5 minutes
   - Condition: Greater than
   - Threshold: 0
   - Notification: Use the same SNS topic
   - Name: `GlueJobFailureAlarm`

2. Create an alarm for Glue job memory usage:
   - Metric: `glue.driver.jvm.heap.usage`
   - Statistic: Maximum
   - Period: 5 minutes
   - Condition: Greater than
   - Threshold: 80 (percent)
   - Notification: Use the same SNS topic
   - Name: `GlueJobMemoryAlarm`

### Step 3: Create a CloudWatch Dashboard

1. Navigate to the CloudWatch console
2. Go to "Dashboards" and click "Create dashboard"
3. Name the dashboard: `DataPipelineMonitoring`
4. Add widgets to the dashboard:

   a. Add a metric graph for Glue job duration:
   - Widget type: Line
   - Metrics: Select `glue.driver.aggregate.elapsedTime` for your job
   - Title: "ETL Job Duration"

   b. Add a metric graph for Glue job records processed:
   - Widget type: Line
   - Metrics: Select `glue.ALL.s3.filesystem.read_bytes` and `glue.ALL.s3.filesystem.write_bytes`
   - Title: "Data Processed (Bytes)"

   c. Add a metric graph for Glue job memory usage:
   - Widget type: Line
   - Metrics: Select `glue.driver.jvm.heap.usage`
   - Title: "Memory Usage"

   d. Add a log widget:
   - Widget type: Logs
   - Log group: Select your Glue job's log group
   - Title: "ETL Job Logs"

   e. Add an alarm status widget:
   - Widget type: Alarm status
   - Alarms: Select all the alarms you created
   - Title: "Pipeline Alarms"

5. Arrange the widgets as desired and save the dashboard

### Step 4: Set Up Custom Metrics with Lambda

1. Navigate to the Lambda console
2. Click "Create function"
3. Choose "Author from scratch"
4. Configure the function:
   - Function name: `DataPipelineMetricsFunction`
   - Runtime: Python 3.9
   - Architecture: x86_64
   - Execution role: Create a new role with basic Lambda permissions
5. Click "Create function"
6. Replace the code with the following:

```python
import json
import boto3
import random
import time
from datetime import datetime

def lambda_handler(event, context):
    # Initialize CloudWatch client
    cloudwatch = boto3.client('cloudwatch')
    
    # Get current timestamp
    timestamp = datetime.utcnow()
    
    # Simulate data quality metrics
    data_quality_score = random.uniform(80.0, 100.0)
    error_rate = random.uniform(0.0, 5.0)
    processing_latency = random.uniform(10.0, 300.0)
    records_processed = random.randint(1000, 10000)
    
    # Publish custom metrics
    cloudwatch.put_metric_data(
        Namespace='DataPipelineMetrics',
        MetricData=[
            {
                'MetricName': 'DataQualityScore',
                'Value': data_quality_score,
                'Unit': 'Percent',
                'Timestamp': timestamp
            },
            {
                'MetricName': 'ErrorRate',
                'Value': error_rate,
                'Unit': 'Percent',
                'Timestamp': timestamp
            },
            {
                'MetricName': 'ProcessingLatency',
                'Value': processing_latency,
                'Unit': 'Seconds',
                'Timestamp': timestamp
            },
            {
                'MetricName': 'RecordsProcessed',
                'Value': records_processed,
                'Unit': 'Count',
                'Timestamp': timestamp
            }
        ]
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Custom metrics published successfully',
            'metrics': {
                'DataQualityScore': data_quality_score,
                'ErrorRate': error_rate,
                'ProcessingLatency': processing_latency,
                'RecordsProcessed': records_processed
            }
        })
    }
```

7. Click "Deploy"
8. Add permissions to the Lambda function's role:
   - Navigate to the IAM console
   - Find the role created for your Lambda function
   - Attach the policy `CloudWatchFullAccess`

### Step 5: Schedule the Lambda Function with EventBridge

1. Navigate to the Amazon EventBridge console
2. Go to "Rules" and click "Create rule"
3. Configure the rule:
   - Name: `DataPipelineMetricsSchedule`
   - Description: "Schedule for publishing custom data pipeline metrics"
   - Rule type: Schedule
4. Define the schedule pattern:
   - Schedule type: Fixed rate
   - Rate expression: 5 minutes
5. Click "Next"
6. Select target:
   - Target type: AWS service
   - Target: Lambda function
   - Function: `DataPipelineMetricsFunction`
7. Click "Next", then "Next" again
8. Click "Create rule"

### Step 6: Create Alarms for Custom Metrics

1. Navigate back to the CloudWatch console
2. Go to "Alarms" > "All alarms" and click "Create alarm"
3. Click "Select metric"
4. Choose "Custom namespaces" > "DataPipelineMetrics"
5. Select the metric `DataQualityScore`
6. Click "Select metric"
7. Configure the alarm:
   - Statistic: Average
   - Period: 5 minutes
   - Threshold type: Static
   - Condition: Less than
   - Threshold value: 90
8. Click "Next"
9. For notification, select your existing SNS topic `data-pipeline-alerts`
10. Click "Next"
11. Name the alarm: `DataQualityAlarm`
12. Click "Next" and then "Create alarm"

13. Repeat the process to create alarms for:
    - ErrorRate (alarm when > 2%)
    - ProcessingLatency (alarm when > 180 seconds)

### Step 7: Add Custom Metrics to Dashboard

1. Navigate back to your CloudWatch dashboard
2. Click "Add widget"
3. Choose "Line" widget
4. Select "Custom namespaces" > "DataPipelineMetrics"
5. Add all your custom metrics to the graph
6. Title the widget "Data Pipeline Quality Metrics"
7. Add the widget to your dashboard
8. Save the dashboard

### Step 8: Set Up Automated Response with Lambda

1. Navigate to the Lambda console
2. Create a new function:
   - Function name: `AlarmResponseFunction`
   - Runtime: Python 3.9
   - Architecture: x86_64
   - Execution role: Create a new role with basic Lambda permissions
3. Replace the code with the following:

```python
import json
import boto3
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event))
    
    # Parse the SNS message
    message = json.loads(event['Records'][0]['Sns']['Message'])
    alarm_name = message['AlarmName']
    alarm_description = message.get('AlarmDescription', 'No description')
    new_state = message['NewStateValue']
    reason = message['NewStateReason']
    
    logger.info(f"Alarm {alarm_name} state changed to {new_state}: {reason}")
    
    # Take action based on the alarm
    if "GlueJob" in alarm_name and new_state == "ALARM":
        handle_glue_job_alarm(alarm_name, reason)
    elif "DataQuality" in alarm_name and new_state == "ALARM":
        handle_data_quality_alarm(alarm_name, reason)
    elif "ErrorRate" in alarm_name and new_state == "ALARM":
        handle_error_rate_alarm(alarm_name, reason)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Alarm processed successfully')
    }

def handle_glue_job_alarm(alarm_name, reason):
    """Handle Glue job alarms by restarting the job if needed"""
    logger.info(f"Handling Glue job alarm: {alarm_name}")
    
    # In a real scenario, you might want to restart the job or take other actions
    # glue_client = boto3.client('glue')
    # glue_client.start_job_run(JobName='sample-etl-job')
    
    # For this lab, we'll just log the action
    logger.info("Would restart Glue job in production environment")

def handle_data_quality_alarm(alarm_name, reason):
    """Handle data quality alarms"""
    logger.info(f"Handling data quality alarm: {alarm_name}")
    
    # In a real scenario, you might want to trigger a data quality check job
    logger.info("Would trigger data quality validation job in production environment")

def handle_error_rate_alarm(alarm_name, reason):
    """Handle high error rate alarms"""
    logger.info(f"Handling error rate alarm: {alarm_name}")
    
    # In a real scenario, you might want to pause the pipeline or trigger investigation
    logger.info("Would trigger investigation workflow in production environment")
```

4. Click "Deploy"
5. Add permissions to the Lambda function's role:
   - Navigate to the IAM console
   - Find the role created for your Lambda function
   - Attach the policy `AWSGlueConsoleFullAccess`

### Step 9: Configure SNS to Trigger Lambda

1. Navigate to the SNS console
2. Select your topic `data-pipeline-alerts`
3. Click "Create subscription"
4. Configure the subscription:
   - Protocol: AWS Lambda
   - Endpoint: Select your `AlarmResponseFunction`
5. Click "Create subscription"

### Step 10: Test the Monitoring System

1. Navigate to the AWS Glue console
2. Run your `sample-etl-job` job
3. While the job is running, navigate to your CloudWatch dashboard
4. Monitor the job's progress and metrics
5. After the job completes (or fails), check if any alarms were triggered
6. Check your email for any alarm notifications
7. Check the CloudWatch Logs for your Lambda functions to see if they were triggered

### Step 11: Set Up Log Insights for Analysis

1. Navigate to the CloudWatch console
2. Go to "Logs" > "Logs Insights"
3. Select the log group for your Glue job
4. Enter the following query to analyze errors:

```
fields @timestamp, @message
| filter @message like "ERROR"
| sort @timestamp desc
| limit 20
```

5. Click "Run query"
6. Save this query for future use by clicking "Save"
7. Name it "Glue Job Error Analysis"

8. Create another query for performance analysis:

```
fields @timestamp, @message
| filter @message like "Processed"
| parse @message "Processed * records" as records_count
| stats sum(records_count) as total_records, avg(records_count) as avg_batch_size
```

9. Run and save this query as "Glue Job Performance Analysis"

## Validation Steps
1. Verify that CloudWatch alarms are correctly configured and trigger when thresholds are exceeded
2. Confirm that the dashboard displays all relevant metrics and logs
3. Check that custom metrics are being published by the Lambda function
4. Verify that the automated response Lambda function is triggered by alarms
5. Confirm that you receive email notifications for alarm state changes
6. Check that Log Insights queries provide useful information for troubleshooting

## Cleanup Instructions
1. Delete the CloudWatch alarms
   ```
   aws cloudwatch delete-alarms --alarm-names GlueJobDurationAlarm GlueJobFailureAlarm GlueJobMemoryAlarm DataQualityAlarm
   ```
2. Delete the CloudWatch dashboard
   ```
   aws cloudwatch delete-dashboards --dashboard-names DataPipelineMonitoring
   ```
3. Delete the Lambda functions
   ```
   aws lambda delete-function --function-name DataPipelineMetricsFunction
   aws lambda delete-function --function-name AlarmResponseFunction
   ```
4. Delete the EventBridge rule
   ```
   aws events delete-rule --name DataPipelineMetricsSchedule
   ```
5. Delete the SNS topic and subscriptions
   ```
   aws sns delete-topic --topic-arn <your-sns-topic-arn>
   ```
6. Delete the Glue job
   ```
   aws glue delete-job --job-name sample-etl-job
   ```
7. Delete the Glue database
   ```
   aws glue delete-database --name monitoring_lab_db
   ```

## Challenge Extensions (Optional)
1. Implement X-Ray tracing for your data pipeline components
2. Create a multi-account monitoring solution using CloudWatch cross-account observability
3. Set up anomaly detection for your custom metrics
4. Implement a custom CloudWatch dashboard using the AWS SDK
5. Create a chatbot integration for Slack or Microsoft Teams notifications
6. Implement automated remediation for common pipeline issues

## Additional Resources
- [CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [CloudWatch Logs Insights Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Amazon SNS Developer Guide](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [AWS Glue Monitoring Documentation](https://docs.aws.amazon.com/glue/latest/dg/monitoring-awsglue-with-cloudwatch-metrics.html)

## Notes and Tips
- Set appropriate thresholds for alarms based on your specific workload patterns
- Use composite alarms for complex conditions that involve multiple metrics
- Consider implementing different notification channels for different severity levels
- Use metric math to create derived metrics that provide better insights
- Implement a consistent tagging strategy for all resources to simplify monitoring
- Consider using CloudWatch Contributor Insights for identifying top contributors to metrics
- Regularly review and refine your monitoring strategy as your data pipelines evolve
