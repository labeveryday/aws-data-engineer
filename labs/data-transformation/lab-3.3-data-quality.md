# Lab 3.3: Data Quality and Validation

## Overview
This lab focuses on implementing data quality checks and validation in your data pipelines. You will learn how to use AWS Glue DataBrew, AWS Glue Data Quality, and custom validation techniques to ensure your data meets quality standards, which is an essential skill for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Implement data profiling to understand data characteristics
- Define and enforce data quality rules
- Create data quality metrics and scorecards
- Implement validation checks in ETL pipelines
- Handle data quality issues with appropriate actions
- Monitor data quality over time
- Implement data cleansing and standardization

**AWS Services Used:**
- AWS Glue DataBrew
- AWS Glue
- Amazon S3
- AWS Lambda
- Amazon CloudWatch
- Amazon SNS (for notifications)
- AWS Glue Data Quality (preview feature)

**Estimated Time:** 3 hours

**Estimated Cost:** $5-10 (AWS Glue and DataBrew have usage-based charges)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for Glue, DataBrew, S3, Lambda, and CloudWatch
- Basic understanding of data quality concepts
- Familiarity with Python and SQL
- Basic knowledge of ETL processes

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │     │             │
│  Source     │────▶│  AWS Glue   │────▶│  Data       │────▶│  Target     │
│  Data (S3)  │     │  DataBrew   │     │  Quality    │     │  Data (S3)  │
│             │     │             │     │  Checks     │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              │
                                              ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│  CloudWatch │◀───▶│  Quality    │◀───▶│  SNS        │
│  Metrics    │     │  Dashboard  │     │  Alerts     │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Implementation Steps

### Step 1: Create S3 Buckets for Data
1. Sign in to the AWS Management Console and navigate to the S3 service
2. Create a bucket for source data (e.g., `your-name-data-quality-source-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-data-quality-source-YYYYMMDD
   ```
3. Create a bucket for processed data (e.g., `your-name-data-quality-processed-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-data-quality-processed-YYYYMMDD
   ```

### Step 2: Prepare Sample Data with Quality Issues
1. Create a sample CSV file with intentional quality issues (`customer_data_with_issues.csv`):

```
customer_id,first_name,last_name,email,registration_date,age,loyalty_points,customer_status
1,John,Doe,john.doe@example.com,2022-01-15,35,120,active
2,Jane,Smith,jane.smith@example.com,2022-02-20,28,85,active
3,Robert,Johnson,robert.j@example.com,2022-03-10,-5,50,inactive
4,Sarah,Williams,not_an_email,2022-04-05,32,200,active
5,Michael,Brown,michael.b@example.com,2022-05-12,41,150,active
6,,Davis,emily.d@example.com,2022-06-18,29,0,pending
7,David,Miller,david.m@example.com,invalid_date,31,95,active
8,Lisa,Wilson,lisa.w@example.com,2022-08-30,150,30,inactive
9,James,Taylor,james.t@example.com,2022-09-14,37,175,active
10,Jennifer,Anderson,jennifer.a@example.com,2022-10-05,,110,active
11,Thomas,Jackson,thomas.j@example.com,2022-11-20,45,200,active
12,Patricia,White,patricia.w@example.com,2022-12-03,39,165,active
13,Christopher,Harris,christopher.h@example.com,2023-01-08,42,190,active
14,Elizabeth,Martin,elizabeth.m@example.com,2023-02-15,36,145,inactive
15,Daniel,Thompson,daniel.t@example.com,2023-03-22,33,210,active
16,Jessica,Garcia,jessica.g@example.com,2023-04-11,27,125,active
17,Matthew,Martinez,matthew.m@example.com,2023-05-19,44,180,active
18,Ashley,Robinson,ashley.r@example.com,2023-06-24,30,155,pending
19,Joshua,Clark,joshua.c@example.com,2023-07-07,38,225,active
20,Amanda,Rodriguez,amanda.r@example.com,2023-08-16,34,170,active
```

2. Create a sample JSON file with different quality issues (`order_data_with_issues.json`):

```json
[
  {"order_id": 1001, "customer_id": 1, "order_date": "2023-01-10", "total_amount": 1299.99, "items": 1, "status": "delivered"},
  {"order_id": 1002, "customer_id": 2, "order_date": "2023-01-15", "total_amount": 899.99, "items": 1, "status": "shipped"},
  {"order_id": 1003, "customer_id": 3, "order_date": "2023-01-20", "total_amount": -159.98, "items": 2, "status": "processing"},
  {"order_id": 1004, "customer_id": 4, "order_date": "2023-01-25", "total_amount": 129.99, "items": 1, "status": "delivered"},
  {"order_id": 1005, "customer_id": 5, "order_date": "2023-01-30", "total_amount": 149.99, "items": 1, "status": "shipped"},
  {"order_id": 1006, "customer_id": 1, "order_date": "2023-02-05", "total_amount": 89.99, "items": 1, "status": "delivered"},
  {"order_id": 1007, "customer_id": 2, "order_date": "2023-02-10", "total_amount": 129.99, "items": 1, "status": "processing"},
  {"order_id": 1008, "customer_id": 6, "order_date": "2023-02-15", "total_amount": 499.99, "items": 1, "status": "shipped"},
  {"order_id": 1009, "customer_id": 7, "order_date": "2023-02-20", "total_amount": 79.98, "items": 2, "status": "delivered"},
  {"order_id": 1010, "customer_id": 8, "order_date": "2023-02-25", "total_amount": 249.99, "items": 1, "status": "processing"},
  {"order_id": 1011, "customer_id": 9, "order_date": "2023-03-02", "total_amount": 349.99, "items": 3, "status": "shipped"},
  {"order_id": 1012, "customer_id": 10, "order_date": "2023-03-08", "total_amount": 199.99, "items": 2, "status": "delivered"},
  {"order_id": 1013, "customer_id": 11, "order_date": "2023-03-15", "total_amount": 599.99, "items": 1, "status": "processing"},
  {"order_id": 1014, "customer_id": 12, "order_date": "2023-03-22", "total_amount": 149.99, "items": 1, "status": "shipped"},
  {"order_id": 1015, "customer_id": 13, "order_date": "2023-03-30", "total_amount": 299.99, "items": 2, "status": "delivered"},
  {"order_id": 1001, "customer_id": 14, "order_date": "2023-04-05", "total_amount": 399.99, "items": 3, "status": "processing"},
  {"order_id": 1017, "customer_id": 15, "order_date": "2023-04-12", "total_amount": 249.99, "items": 1, "status": "shipped"},
  {"order_id": 1018, "customer_id": 16, "order_date": "2023-04-20", "total_amount": 179.99, "items": 2, "status": "delivered"},
  {"order_id": 1019, "customer_id": 17, "order_date": "2023-04-28", "total_amount": 499.99, "items": 1, "status": "processing"},
  {"order_id": 1020, "customer_id": 18, "order_date": "2023-05-05", "total_amount": null, "items": 2, "status": "pending"}
]
```

3. Upload these files to your source S3 bucket:
   ```
   aws s3 cp customer_data_with_issues.csv s3://your-name-data-quality-source-YYYYMMDD/raw/customers/
   aws s3 cp order_data_with_issues.json s3://your-name-data-quality-source-YYYYMMDD/raw/orders/
   ```

### Step 3: Create an IAM Role for Data Quality Services
1. Navigate to the IAM console
2. Create a new role with the following permissions:
   - AWSGlueServiceRole
   - AWSGlueDataBrewServiceRole
   - AmazonS3FullAccess (in production, use more restrictive policies)
   - AmazonSNSFullAccess
   - CloudWatchFullAccess
3. Name the role `DataQualityLabRole`

### Step 4: Profile Data Using AWS Glue DataBrew
1. Navigate to the AWS Glue DataBrew console
2. Click "Create project"
3. Configure the project:
   - Project name: `customer-data-profiling`
   - Dataset name: `customer-data`
   - Dataset source: S3
   - S3 location: `s3://your-name-data-quality-source-YYYYMMDD/raw/customers/customer_data_with_issues.csv`
   - File type: CSV
   - First row is header: Yes
   - IAM role: `DataQualityLabRole`
4. Create the project
5. Once the project opens, click "Profile" in the top menu
6. Click "Run data profile" to analyze the data
7. After the profile job completes, review the results to identify data quality issues:
   - Missing values in `first_name` and `age`
   - Invalid values in `age` (negative and too high)
   - Invalid email format
   - Invalid date format

8. Create another project for the order data:
   - Project name: `order-data-profiling`
   - Dataset name: `order-data`
   - Dataset source: S3
   - S3 location: `s3://your-name-data-quality-source-YYYYMMDD/raw/orders/order_data_with_issues.json`
   - File type: JSON
   - IAM role: `DataQualityLabRole`
9. Run a profile job for this dataset as well

### Step 5: Create Data Quality Rules with DataBrew
1. Go back to the `customer-data-profiling` project
2. Click "Create recipe" to start defining data transformations
3. Add the following steps to your recipe:

   a. Filter out rows with missing first names:
   - Click "Filter" in the transformation menu
   - Select "first_name"
   - Choose "Is not null"
   - Apply the transformation

   b. Validate and standardize email addresses:
   - Click "PATTERN" in the transformation menu
   - Select "email"
   - Choose "Email validation"
   - Apply the transformation
   - For invalid emails, choose "Replace with null"

   c. Fix age values:
   - Click "FILTER" in the transformation menu
   - Select "age"
   - Choose "Custom formula"
   - Enter `age >= 0 AND age <= 120`
   - Apply the transformation

   d. Validate date format:
   - Click "PATTERN" in the transformation menu
   - Select "registration_date"
   - Choose "Date validation"
   - Specify format "YYYY-MM-DD"
   - Apply the transformation
   - For invalid dates, choose "Replace with null"

4. Save the recipe
5. Create a job to apply the recipe:
   - Job name: `customer-data-quality-job`
   - Output location: `s3://your-name-data-quality-processed-YYYYMMDD/processed/customers/`
   - Output format: CSV
   - IAM role: `DataQualityLabRole`
6. Run the job and wait for it to complete

7. Repeat similar steps for the order data project:
   - Create a recipe to validate order amounts (must be positive)
   - Check for duplicate order IDs
   - Ensure all required fields have values
   - Create and run a job to process the data

### Step 6: Implement Custom Data Quality Checks with AWS Glue
1. Navigate to the AWS Glue console
2. Create a new Glue job with the following PySpark script:

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as F
from pyspark.sql.types import *
import boto3
from datetime import datetime

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'source_bucket', 'target_bucket', 'sns_topic'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Get parameters
source_bucket = args['source_bucket']
target_bucket = args['target_bucket']
sns_topic = args['sns_topic']

# Initialize SNS client for notifications
sns = boto3.client('sns')

# Define data quality rules
def check_data_quality(df, table_name):
    # Initialize quality metrics
    total_records = df.count()
    quality_issues = []
    quality_score = 100.0
    
    # Check for null values in critical columns
    critical_columns = ['customer_id', 'email', 'registration_date'] if table_name == 'customers' else ['order_id', 'customer_id', 'order_date', 'total_amount']
    
    for column in critical_columns:
        if column in df.columns:
            null_count = df.filter(F.col(column).isNull()).count()
            null_percentage = (null_count / total_records) * 100 if total_records > 0 else 0
            
            if null_count > 0:
                quality_issues.append(f"Column '{column}' has {null_count} null values ({null_percentage:.2f}%)")
                quality_score -= (null_percentage * 0.5)  # Reduce score based on percentage of nulls
    
    # Check for specific data quality rules
    if table_name == 'customers':
        # Check for invalid emails
        invalid_emails = df.filter(~F.col("email").rlike("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$")).count()
        if invalid_emails > 0:
            invalid_percentage = (invalid_emails / total_records) * 100 if total_records > 0 else 0
            quality_issues.append(f"Found {invalid_emails} invalid email addresses ({invalid_percentage:.2f}%)")
            quality_score -= (invalid_percentage * 0.5)
        
        # Check for invalid ages
        invalid_ages = df.filter((F.col("age") < 0) | (F.col("age") > 120) | F.col("age").isNull()).count()
        if invalid_ages > 0:
            invalid_percentage = (invalid_ages / total_records) * 100 if total_records > 0 else 0
            quality_issues.append(f"Found {invalid_ages} invalid age values ({invalid_percentage:.2f}%)")
            quality_score -= (invalid_percentage * 0.5)
    
    elif table_name == 'orders':
        # Check for negative order amounts
        negative_amounts = df.filter(F.col("total_amount") < 0).count()
        if negative_amounts > 0:
            negative_percentage = (negative_amounts / total_records) * 100 if total_records > 0 else 0
            quality_issues.append(f"Found {negative_amounts} negative order amounts ({negative_percentage:.2f}%)")
            quality_score -= (negative_percentage * 1.0)
        
        # Check for duplicate order IDs
        duplicate_orders = df.groupBy("order_id").count().filter("count > 1").count()
        if duplicate_orders > 0:
            quality_issues.append(f"Found {duplicate_orders} duplicate order IDs")
            quality_score -= (duplicate_orders * 5.0)  # Severe penalty for duplicates
    
    # Ensure score is between 0 and 100
    quality_score = max(0, min(100, quality_score))
    
    # Create quality report
    quality_report = {
        "table_name": table_name,
        "total_records": total_records,
        "quality_score": quality_score,
        "quality_issues": quality_issues,
        "timestamp": datetime.now().isoformat()
    }
    
    return quality_report

# Process customer data
customer_path = f"s3://{source_bucket}/raw/customers/customer_data_with_issues.csv"
customer_df = spark.read.option("header", "true").option("inferSchema", "true").csv(customer_path)

# Run data quality checks on customer data
customer_quality_report = check_data_quality(customer_df, "customers")
print(f"Customer Data Quality Report: {customer_quality_report}")

# Process order data
order_path = f"s3://{source_bucket}/raw/orders/order_data_with_issues.json"
order_df = spark.read.json(order_path)

# Run data quality checks on order data
order_quality_report = check_data_quality(order_df, "orders")
print(f"Order Data Quality Report: {order_quality_report}")

# Send notifications if quality score is below threshold
threshold = 80.0
if customer_quality_report["quality_score"] < threshold or order_quality_report["quality_score"] < threshold:
    message = f"Data Quality Alert!\n\n"
    
    if customer_quality_report["quality_score"] < threshold:
        message += f"Customer data quality score: {customer_quality_report['quality_score']:.2f}%\n"
        message += f"Issues found:\n"
        for issue in customer_quality_report["quality_issues"]:
            message += f"- {issue}\n"
        message += "\n"
    
    if order_quality_report["quality_score"] < threshold:
        message += f"Order data quality score: {order_quality_report['quality_score']:.2f}%\n"
        message += f"Issues found:\n"
        for issue in order_quality_report["quality_issues"]:
            message += f"- {issue}\n"
    
    # Send SNS notification
    sns.publish(
        TopicArn=sns_topic,
        Subject="Data Quality Alert",
        Message=message
    )

# Apply data quality fixes
# 1. Fix customer data
clean_customer_df = customer_df.filter(F.col("first_name").isNotNull()) \
    .filter((F.col("age") >= 0) & (F.col("age") <= 120)) \
    .withColumn("email", F.when(F.regexp_extract("email", "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$", 0) != "", F.col("email")).otherwise(None))

# 2. Fix order data
clean_order_df = order_df.filter(F.col("total_amount").isNotNull() & (F.col("total_amount") >= 0)) \
    .dropDuplicates(["order_id"])

# Save cleaned data
clean_customer_df.write.mode("overwrite").option("header", "true").csv(f"s3://{target_bucket}/processed/customers/")
clean_order_df.write.mode("overwrite").json(f"s3://{target_bucket}/processed/orders/")

# Save quality reports
quality_reports = spark.createDataFrame([
    (
        "customers",
        customer_quality_report["total_records"],
        customer_quality_report["quality_score"],
        str(customer_quality_report["quality_issues"]),
        customer_quality_report["timestamp"]
    ),
    (
        "orders",
        order_quality_report["total_records"],
        order_quality_report["quality_score"],
        str(order_quality_report["quality_issues"]),
        order_quality_report["timestamp"]
    )
], ["table_name", "total_records", "quality_score", "quality_issues", "timestamp"])

quality_reports.write.mode("overwrite").option("header", "true").csv(f"s3://{target_bucket}/quality_reports/")

job.commit()
```

3. Configure the job:
   - Name: `comprehensive-data-quality-job`
   - IAM role: `DataQualityLabRole`
   - Type: Spark
   - Glue version: Glue 3.0
   - Worker type: G.1X
   - Number of workers: 2
   - Job parameters:
     - `--source_bucket`: your-name-data-quality-source-YYYYMMDD
     - `--target_bucket`: your-name-data-quality-processed-YYYYMMDD
     - `--sns_topic`: arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:data-quality-alerts

### Step 7: Create an SNS Topic for Data Quality Alerts
1. Navigate to the Amazon SNS console
2. Click "Create topic"
3. Select "Standard" type
4. Name the topic `data-quality-alerts`
5. Create the topic
6. Create a subscription for the topic:
   - Protocol: Email
   - Endpoint: Your email address
7. Confirm the subscription by clicking the link in the email you receive

### Step 8: Run the Comprehensive Data Quality Job
1. Navigate back to the AWS Glue console
2. Find your `comprehensive-data-quality-job` and click "Run job"
3. Wait for the job to complete
4. Check your email for any data quality alerts

### Step 9: Create a CloudWatch Dashboard for Data Quality Monitoring
1. Navigate to the CloudWatch console
2. Click "Dashboards" and then "Create dashboard"
3. Name the dashboard `Data-Quality-Dashboard`
4. Add widgets to display:
   - Glue job success/failure metrics
   - Custom metrics for data quality scores
   - Alerts and notifications history

### Step 10: Implement AWS Glue Data Quality (Preview Feature)
1. Navigate to the AWS Glue console
2. Go to "Data quality" under "Data catalog"
3. Click "Create data quality rule set"
4. Configure the rule set:
   - Name: `customer-data-rules`
   - Database: Create or select a database
   - Table: Create or select a table for customer data
5. Add the following rules:
   - `Completeness "customer_id" > 0.99` (99% of records must have customer_id)
   - `Completeness "email" > 0.95` (95% of records must have email)
   - `Uniqueness "customer_id" = 1.0` (customer_id must be unique)
   - `ColumnValues "age" >= 0` (age must be non-negative)
   - `ColumnValues "age" <= 120` (age must be reasonable)
   - `ColumnValues "email" MATCHES_REGEX "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$"` (email must be valid format)
6. Save the rule set
7. Create a similar rule set for order data

### Step 11: Analyze and Compare Results
1. Download the quality reports from your processed S3 bucket:
   ```
   aws s3 cp s3://your-name-data-quality-processed-YYYYMMDD/quality_reports/ ./quality_reports/ --recursive
   ```
2. Compare the results from different approaches:
   - DataBrew profiling
   - Custom Glue job quality checks
   - AWS Glue Data Quality rules
3. Analyze which approach is most effective for different types of quality issues

## Validation Steps
1. Verify that data quality issues were correctly identified
2. Confirm that data quality metrics were calculated accurately
3. Check that notifications were sent for quality issues
4. Verify that the cleaned data has resolved the quality issues
5. Confirm that quality reports were generated and stored
6. Check that the CloudWatch dashboard displays relevant metrics

## Cleanup Instructions
1. Delete the DataBrew projects and jobs
   ```
   aws databrew delete-project --name customer-data-profiling
   aws databrew delete-project --name order-data-profiling
   ```
2. Delete the Glue job
   ```
   aws glue delete-job --job-name comprehensive-data-quality-job
   ```
3. Delete the SNS topic and subscription
   ```
   aws sns delete-topic --topic-arn arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:data-quality-alerts
   ```
4. Delete the S3 buckets and their contents
   ```
   aws s3 rb s3://your-name-data-quality-source-YYYYMMDD --force
   aws s3 rb s3://your-name-data-quality-processed-YYYYMMDD --force
   ```
5. Delete the CloudWatch dashboard
   ```
   aws cloudwatch delete-dashboards --dashboard-names Data-Quality-Dashboard
   ```
6. Delete the IAM role
   ```
   aws iam delete-role --role-name DataQualityLabRole
   ```

## Challenge Extensions (Optional)
1. Implement a data quality scoring system with multiple dimensions
2. Create a historical tracking system for data quality metrics
3. Implement automated remediation for common quality issues
4. Set up a data quality gateway that prevents low-quality data from entering your data lake
5. Create a custom data quality dashboard using Amazon QuickSight
6. Implement machine learning-based anomaly detection for data quality

## Additional Resources
- [AWS Glue DataBrew Documentation](https://docs.aws.amazon.com/databrew/latest/dg/what-is.html)
- [AWS Glue Data Quality Documentation](https://docs.aws.amazon.com/glue/latest/dg/data-quality.html)
- [Data Quality Best Practices](https://aws.amazon.com/blogs/big-data/build-a-data-quality-score-card-using-amazon-deequ/)
- [Implementing Data Quality Checks with AWS Glue](https://aws.amazon.com/blogs/big-data/implementing-data-quality-checks-using-aws-glue-databrew/)

## Notes and Tips
- Data quality should be measured at multiple points in your data pipeline
- Consider both technical quality (format, completeness) and business quality (accuracy, relevance)
- Implement automated monitoring for ongoing data quality assurance
- Balance the cost of quality checks against the value they provide
- Use appropriate thresholds based on your specific use case requirements
- Document your data quality rules and share them with stakeholders
- Consider implementing a data quality service level agreement (SLA)
