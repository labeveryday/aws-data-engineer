# Lab 3.1: ETL with AWS Glue

## Overview
This lab focuses on building ETL (Extract, Transform, Load) pipelines using AWS Glue. You will learn how to create crawlers to discover data, develop ETL jobs using both visual interface and PySpark, and implement data quality checks, which are essential skills for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Set up AWS Glue crawlers to discover and catalog data
- Create ETL jobs using AWS Glue Studio visual interface
- Develop custom ETL scripts using PySpark
- Implement data transformation logic
- Configure job bookmarks for incremental processing
- Implement data quality checks
- Monitor and troubleshoot ETL jobs

**AWS Services Used:**
- AWS Glue (Crawlers, Data Catalog, ETL Jobs)
- Amazon S3
- AWS Glue DataBrew (optional)
- Amazon Athena
- AWS Identity and Access Management (IAM)

**Estimated Time:** 3 hours

**Estimated Cost:** $5-10 (AWS Glue charges per minute of processing)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for Glue, S3, and Athena
- Basic understanding of ETL concepts
- Familiarity with Python and SQL
- Basic knowledge of Spark (helpful but not required)

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │     │             │
│  Source     │────▶│  AWS Glue   │────▶│  AWS Glue   │────▶│  Target     │
│  Data (S3)  │     │  Crawler    │     │  ETL Job    │     │  Data (S3)  │
│             │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                   │                    │
                          ▼                   ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
                    │             │     │             │     │             │
                    │  AWS Glue   │     │ CloudWatch  │     │  Amazon     │
                    │  Catalog    │     │ Monitoring  │     │  Athena     │
                    │             │     │             │     │             │
                    └─────────────┘     └─────────────┘     └─────────────┘
```

## Implementation Steps

### Step 1: Create S3 Buckets for Source and Target Data
1. Sign in to the AWS Management Console and navigate to the S3 service
2. Create a bucket for source data (e.g., `your-name-glue-source-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-glue-source-YYYYMMDD
   ```
3. Create a bucket for target data (e.g., `your-name-glue-target-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-glue-target-YYYYMMDD
   ```
4. Create a bucket for Glue scripts and temporary files (e.g., `your-name-glue-scripts-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-glue-scripts-YYYYMMDD
   ```

### Step 2: Prepare Sample Data
1. Create a sample CSV file for customer data (`customers.csv`):
```
customer_id,first_name,last_name,email,registration_date,status,loyalty_points
1,John,Doe,john.doe@example.com,2022-01-15,active,120
2,Jane,Smith,jane.smith@example.com,2022-02-20,active,85
3,Robert,Johnson,robert.j@example.com,2022-03-10,inactive,50
4,Sarah,Williams,sarah.w@example.com,2022-04-05,active,200
5,Michael,Brown,michael.b@example.com,2022-05-12,active,150
6,Emily,Davis,emily.d@example.com,2022-06-18,pending,0
7,David,Miller,david.m@example.com,2022-07-22,active,95
8,Lisa,Wilson,lisa.w@example.com,2022-08-30,inactive,30
9,James,Taylor,james.t@example.com,2022-09-14,active,175
10,Jennifer,Anderson,jennifer.a@example.com,2022-10-05,active,110
```

2. Create a sample JSON file for order data (`orders.json`):
```json
{"order_id": 1001, "customer_id": 1, "order_date": "2023-01-10", "total_amount": 1299.99, "items": 1, "status": "delivered"}
{"order_id": 1002, "customer_id": 2, "order_date": "2023-01-15", "total_amount": 899.99, "items": 1, "status": "shipped"}
{"order_id": 1003, "customer_id": 3, "order_date": "2023-01-20", "total_amount": 159.98, "items": 2, "status": "processing"}
{"order_id": 1004, "customer_id": 4, "order_date": "2023-01-25", "total_amount": 129.99, "items": 1, "status": "delivered"}
{"order_id": 1005, "customer_id": 5, "order_date": "2023-01-30", "total_amount": 149.99, "items": 1, "status": "shipped"}
{"order_id": 1006, "customer_id": 1, "order_date": "2023-02-05", "total_amount": 89.99, "items": 1, "status": "delivered"}
{"order_id": 1007, "customer_id": 2, "order_date": "2023-02-10", "total_amount": 129.99, "items": 1, "status": "processing"}
{"order_id": 1008, "customer_id": 6, "order_date": "2023-02-15", "total_amount": 499.99, "items": 1, "status": "shipped"}
{"order_id": 1009, "customer_id": 7, "order_date": "2023-02-20", "total_amount": 79.98, "items": 2, "status": "delivered"}
{"order_id": 1010, "customer_id": 8, "order_date": "2023-02-25", "total_amount": 249.99, "items": 1, "status": "processing"}
```

3. Upload these files to your source S3 bucket:
   ```
   aws s3 cp customers.csv s3://your-name-glue-source-YYYYMMDD/raw/customers/
   aws s3 cp orders.json s3://your-name-glue-source-YYYYMMDD/raw/orders/
   ```

### Step 3: Create an IAM Role for AWS Glue
1. Navigate to the IAM console
2. Create a new role with the following permissions:
   - AWSGlueServiceRole
   - AmazonS3FullAccess (in production, use more restrictive policies)
   - AWSGlueConsoleFullAccess
   - AmazonAthenaFullAccess
3. Name the role `GlueETLLabRole`

### Step 4: Create a Glue Database and Crawlers
1. Navigate to the AWS Glue console
2. Go to "Databases" under "Data catalog" and click "Add database"
3. Name the database `retail_db` and create it
4. Go to "Crawlers" and click "Create crawler"
5. Name the crawler `retail_source_crawler`
6. For data source, choose S3 and specify your source bucket path: `s3://your-name-glue-source-YYYYMMDD/raw/`
7. Choose the IAM role you created
8. For output, select the `retail_db` database
9. Set the crawler schedule to run on demand
10. Review and create the crawler
11. Run the crawler and wait for it to complete

### Step 5: Explore the Discovered Data
1. After the crawler completes, go to "Tables" under "Data catalog"
2. You should see tables for customers and orders
3. Click on each table to explore its schema
4. Use Athena to query the data:
   ```sql
   SELECT * FROM retail_db.customers LIMIT 10;
   ```
   ```sql
   SELECT * FROM retail_db.orders LIMIT 10;
   ```

### Step 6: Create a Visual ETL Job with Glue Studio
1. Navigate to AWS Glue Studio
2. Click "Create job" and select "Visual with a source and target"
3. For source, select "Data Catalog table" and choose the customers table
4. Add a "Change Schema" transform to:
   - Convert column names to lowercase
   - Rename `first_name` and `last_name` to `firstname` and `lastname`
   - Change data types if needed
5. Add a "Filter" transform to keep only active customers:
   - Filter condition: `status = 'active'`
6. For target, select "Amazon S3" with the following settings:
   - Format: Parquet
   - Compression: Snappy
   - Location: `s3://your-name-glue-target-YYYYMMDD/processed/customers/`
7. Configure job properties:
   - Name: `process_customers_job`
   - IAM Role: `GlueETLLabRole`
   - Glue version: Glue 3.0
   - Language: Python
   - Worker type: G.1X
   - Number of workers: 2
   - Job bookmark: Enable
8. Save and run the job

### Step 7: Create a Custom PySpark ETL Job
1. In the AWS Glue console, go to "Jobs" and click "Create job"
2. Choose "Spark script editor"
3. Select "Create a new script with boilerplate code"
4. Name the script `process_orders_script`
5. Replace the boilerplate code with the following PySpark script:

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
from awsglue.dynamicframe import DynamicFrame

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read orders data from Glue Data Catalog
orders_dyf = glueContext.create_dynamic_frame.from_catalog(
    database="retail_db",
    table_name="orders"
)

# Convert to Spark DataFrame for easier transformations
orders_df = orders_dyf.toDF()

# Perform transformations
transformed_df = orders_df.withColumn(
    "processing_date", F.current_date()
).withColumn(
    "order_year", F.year(F.to_date(F.col("order_date")))
).withColumn(
    "order_month", F.month(F.to_date(F.col("order_date")))
).withColumn(
    "order_day", F.dayofmonth(F.to_date(F.col("order_date")))
).withColumn(
    "amount_category", F.when(F.col("total_amount") < 100, "low")
                        .when(F.col("total_amount") < 500, "medium")
                        .otherwise("high")
)

# Data quality checks
total_records = transformed_df.count()
valid_records = transformed_df.filter(
    (F.col("order_id").isNotNull()) & 
    (F.col("customer_id").isNotNull()) & 
    (F.col("order_date").isNotNull()) &
    (F.col("total_amount") > 0)
).count()

print(f"Total records: {total_records}")
print(f"Valid records: {valid_records}")
print(f"Data quality score: {valid_records / total_records:.2%}")

# Convert back to DynamicFrame
transformed_dyf = DynamicFrame.fromDF(transformed_df, glueContext, "transformed_orders")

# Write to S3 in Parquet format, partitioned by year and month
output_path = "s3://your-name-glue-target-YYYYMMDD/processed/orders/"
glueContext.write_dynamic_frame.from_options(
    frame=transformed_dyf,
    connection_type="s3",
    connection_options={
        "path": output_path,
        "partitionKeys": ["order_year", "order_month"]
    },
    format="parquet",
    transformation_ctx="output_orders"
)

# Create a crawler to catalog the processed data
processed_crawler_name = "retail_processed_crawler"
processed_crawler_exists = False

try:
    glueContext.get_crawler(processed_crawler_name)
    processed_crawler_exists = True
except:
    pass

if not processed_crawler_exists:
    glueContext.create_crawler(
        name=processed_crawler_name,
        role="GlueETLLabRole",
        database_name="retail_db",
        targets={"s3Targets": [{"path": output_path}]},
        schedule="cron(0 0 * * ? *)",
        table_prefix="processed_"
    )

job.commit()
```

6. Update the S3 path in the script to match your target bucket
7. Configure job properties:
   - Name: `process_orders_job`
   - IAM Role: `GlueETLLabRole`
   - Glue version: Glue 3.0
   - Language: Python
   - Worker type: G.1X
   - Number of workers: 2
   - Job bookmark: Enable
8. Save and run the job

### Step 8: Create a Crawler for Processed Data
1. In the AWS Glue console, go to "Crawlers" and click "Create crawler"
2. Name the crawler `retail_processed_crawler`
3. For data source, choose S3 and specify your target bucket path: `s3://your-name-glue-target-YYYYMMDD/processed/`
4. Choose the IAM role you created
5. For output, select the `retail_db` database and add the prefix `processed_`
6. Set the crawler schedule to run on demand
7. Review and create the crawler
8. Run the crawler and wait for it to complete

### Step 9: Query and Analyze the Processed Data
1. Navigate to the Amazon Athena console
2. Set up a query result location if not already configured: `s3://your-name-glue-scripts-YYYYMMDD/athena-results/`
3. Run queries to analyze the processed data:

```sql
-- Query processed customers
SELECT * FROM retail_db.processed_customers LIMIT 10;

-- Query processed orders with partitioning
SELECT * FROM retail_db.processed_orders
WHERE order_year = 2023 AND order_month = 1
LIMIT 10;

-- Join customers and orders
SELECT 
  c.firstname,
  c.lastname,
  o.order_id,
  o.order_date,
  o.total_amount,
  o.amount_category
FROM 
  retail_db.processed_customers c
JOIN 
  retail_db.processed_orders o ON c.customer_id = o.customer_id
ORDER BY 
  o.order_date DESC
LIMIT 10;

-- Analyze orders by amount category
SELECT 
  amount_category,
  COUNT(*) as order_count,
  ROUND(AVG(total_amount), 2) as avg_amount,
  ROUND(SUM(total_amount), 2) as total_amount
FROM 
  retail_db.processed_orders
GROUP BY 
  amount_category
ORDER BY 
  avg_amount DESC;
```

### Step 10: Set Up a Workflow to Orchestrate Jobs
1. In the AWS Glue console, go to "Workflows" and click "Add workflow"
2. Name the workflow `retail_etl_workflow`
3. Add a trigger for the first job:
   - Trigger type: On-demand
   - Target: `process_customers_job`
4. Add a trigger for the second job:
   - Trigger type: Job completion
   - Watching: `process_customers_job`
   - Target: `process_orders_job`
5. Add a trigger for the crawler:
   - Trigger type: Job completion
   - Watching: `process_orders_job`
   - Target: `retail_processed_crawler`
6. Save the workflow
7. Run the workflow and monitor its progress

## Validation Steps
1. Verify that both ETL jobs completed successfully
2. Confirm that the processed data is available in the target S3 bucket
3. Check that the crawler created tables for the processed data
4. Verify that Athena queries return the expected results
5. Confirm that data transformations were applied correctly
6. Check that the workflow executed all steps in the correct order

## Cleanup Instructions
1. Delete the Glue jobs
   ```
   aws glue delete-job --job-name process_customers_job
   aws glue delete-job --job-name process_orders_job
   ```
2. Delete the Glue crawlers
   ```
   aws glue delete-crawler --name retail_source_crawler
   aws glue delete-crawler --name retail_processed_crawler
   ```
3. Delete the Glue database and tables
   ```
   aws glue delete-database --name retail_db
   ```
4. Delete the workflow
   ```
   aws glue delete-workflow --name retail_etl_workflow
   ```
5. Delete the S3 buckets and their contents
   ```
   aws s3 rb s3://your-name-glue-source-YYYYMMDD --force
   aws s3 rb s3://your-name-glue-target-YYYYMMDD --force
   aws s3 rb s3://your-name-glue-scripts-YYYYMMDD --force
   ```
6. Delete the IAM role
   ```
   aws iam delete-role --role-name GlueETLLabRole
   ```

## Challenge Extensions (Optional)
1. Implement error handling and data quality validation in your ETL jobs
2. Add a job to detect and handle schema changes in source data
3. Implement incremental processing using job bookmarks
4. Create a more complex transformation that joins multiple data sources
5. Set up monitoring and alerting for job failures
6. Implement data masking for sensitive fields

## Additional Resources
- [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/index.html)
- [AWS Glue Best Practices](https://docs.aws.amazon.com/glue/latest/dg/best-practices.html)
- [Glue ETL Programming Guide](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming.html)

## Notes and Tips
- Use job bookmarks to process only new data in subsequent job runs
- Monitor job metrics to identify performance bottlenecks
- Use appropriate worker types and number of workers based on data volume
- Consider using Glue DataBrew for visual data preparation
- Implement error handling and logging in your ETL scripts
- Use dynamic frames for schema flexibility and handling nested data
- Optimize Parquet files with appropriate compression and partitioning
