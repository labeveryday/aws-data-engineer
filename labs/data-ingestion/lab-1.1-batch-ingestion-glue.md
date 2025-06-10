# Lab 1.1: Batch Data Ingestion with AWS Glue

## Overview
This lab focuses on implementing a batch data ingestion pipeline using AWS Glue. You will learn how to ingest structured and semi-structured data from various sources into an S3 data lake, catalog it using AWS Glue Crawler, and prepare it for analysis.

**Learning Objectives:**
- Set up an S3 data lake with appropriate bucket structure
- Configure and run AWS Glue crawlers to discover and catalog data
- Create and run AWS Glue ETL jobs for data ingestion
- Implement Glue bookmarks for incremental data processing
- Query the ingested data using Amazon Athena

**AWS Services Used:**
- Amazon S3
- AWS Glue (Crawlers, Data Catalog, ETL Jobs)
- Amazon Athena
- AWS IAM

**Estimated Time:** 2 hours

**Estimated Cost:** $5-10 (Most resources fall under Free Tier if available)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for S3, Glue, and Athena
- Sample dataset downloaded (NYC Taxi Data subset provided in resources)
- Basic understanding of ETL concepts and SQL

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │     │             │
│  Source     │────▶│  AWS Glue   │────▶│  S3 Data    │────▶│  AWS Glue   │
│  Data       │     │  ETL Job    │     │  Lake       │     │  Crawler    │
│             │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   ▼
                                                           ┌─────────────┐     ┌─────────────┐
                                                           │             │     │             │
                                                           │  AWS Glue   │────▶│  Amazon     │
                                                           │  Catalog    │     │  Athena     │
                                                           │             │     │             │
                                                           └─────────────┘     └─────────────┘
```

## Implementation Steps

### Step 1: Set Up S3 Data Lake Structure
1. Sign in to the AWS Management Console and navigate to the S3 service
2. Create a new S3 bucket with a unique name (e.g., `your-name-data-lake-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-data-lake-YYYYMMDD
   ```
3. Create the following folder structure in your bucket:
   - `raw/` - For incoming raw data
   - `processed/` - For transformed data
   - `analytics/` - For data ready for analysis
   ```
   aws s3api put-object --bucket your-name-data-lake-YYYYMMDD --key raw/
   aws s3api put-object --bucket your-name-data-lake-YYYYMMDD --key processed/
   aws s3api put-object --bucket your-name-data-lake-YYYYMMDD --key analytics/
   ```

### Step 2: Upload Sample Data to S3
1. Download the sample NYC Taxi Data CSV files from the provided resource link
2. Upload the sample data to the `raw/nyc-taxi/` prefix in your S3 bucket
   ```
   aws s3 cp ./sample-data/ s3://your-name-data-lake-YYYYMMDD/raw/nyc-taxi/ --recursive
   ```

### Step 3: Create an IAM Role for Glue
1. Navigate to the IAM console
2. Create a new role with the following permissions:
   - AWSGlueServiceRole
   - AmazonS3FullAccess (in production, use more restrictive policies)
   - AmazonAthenaFullAccess
3. Name the role `GlueLabRole`

### Step 4: Create and Run a Glue Crawler
1. Navigate to the AWS Glue console
2. Select "Crawlers" from the left navigation and click "Create crawler"
3. Name the crawler `nyc-taxi-raw-crawler`
4. Select the S3 data source and specify your bucket path: `s3://your-name-data-lake-YYYYMMDD/raw/nyc-taxi/`
5. Choose the IAM role created in Step 3
6. Create a new database called `taxi_db`
7. Set the crawler schedule to run on demand
8. Review and create the crawler
9. Run the crawler and wait for it to complete

### Step 5: Create a Glue ETL Job
1. In the AWS Glue console, select "Jobs" from the left navigation
2. Click "Create job"
3. Choose "Visual with a source and target"
4. Select the source as the table created by your crawler
5. Add a transformation to convert data types and clean the data
6. Select the target as S3 with the path: `s3://your-name-data-lake-YYYYMMDD/processed/nyc-taxi/`
7. Choose Parquet as the output format
8. Configure job properties:
   - Name: `nyc-taxi-processing`
   - IAM Role: `GlueLabRole`
   - Enable job bookmarks: Yes
9. Save and run the job

### Step 6: Create a Crawler for Processed Data
1. Create another crawler named `nyc-taxi-processed-crawler`
2. Configure it to crawl the processed data path: `s3://your-name-data-lake-YYYYMMDD/processed/nyc-taxi/`
3. Use the same IAM role and database
4. Run the crawler and wait for it to complete

### Step 7: Query Data with Athena
1. Navigate to the Amazon Athena console
2. Set up a query result location if not already configured: `s3://your-name-data-lake-YYYYMMDD/athena-results/`
3. Run a sample query to analyze the taxi data:
   ```sql
   SELECT 
     passenger_count, 
     AVG(trip_distance) as avg_distance,
     COUNT(*) as trip_count
   FROM 
     taxi_db.nyc_taxi_processed
   GROUP BY 
     passenger_count
   ORDER BY 
     passenger_count;
   ```

## Validation Steps
1. Verify that the Glue crawlers have successfully created tables in the Glue Data Catalog
2. Confirm that the Glue ETL job ran successfully and data is available in the processed folder
3. Check that Athena queries return expected results from the processed data
4. Verify that the data is stored in Parquet format in the processed folder

## Cleanup Instructions
1. Delete the Athena query results
   ```
   aws s3 rm s3://your-name-data-lake-YYYYMMDD/athena-results/ --recursive
   ```
2. Delete the Glue jobs and crawlers
   ```
   aws glue delete-job --job-name nyc-taxi-processing
   aws glue delete-crawler --name nyc-taxi-raw-crawler
   aws glue delete-crawler --name nyc-taxi-processed-crawler
   ```
3. Delete the Glue database and tables
   ```
   aws glue delete-database --name taxi_db
   ```
4. Delete the S3 bucket and its contents
   ```
   aws s3 rb s3://your-name-data-lake-YYYYMMDD --force
   ```
5. Delete the IAM role
   ```
   aws iam delete-role --role-name GlueLabRole
   ```

## Challenge Extensions (Optional)
1. Modify the Glue job to partition the data by year and month
2. Implement data quality checks in your Glue job using FindMatches or custom transformations
3. Create a Glue workflow to orchestrate the crawlers and ETL job in sequence
4. Add error handling and notification using SNS when the ETL job fails

## Additional Resources
- [AWS Glue Developer Guide](https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html)
- [Best Practices for S3 Data Lakes](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/build-a-data-lake-using-amazon-s3.html)
- [NYC TLC Trip Record Data](https://registry.opendata.aws/nyc-tlc-trip-records-pds/)

## Notes and Tips
- When working with large datasets, consider using Glue bookmarks to process only new data
- Partitioning data by date can significantly improve query performance in Athena
- In production environments, use more restrictive IAM policies following the principle of least privilege
- Monitor Glue job metrics to optimize performance and cost
