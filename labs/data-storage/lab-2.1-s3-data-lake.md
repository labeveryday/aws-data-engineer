# Lab 2.1: S3 Data Lake Organization

## Overview
This lab focuses on designing and implementing an efficient S3 data lake structure following best practices. You will learn how to organize data using appropriate partitioning strategies, implement data lifecycle policies, and optimize for both cost and performance.

**Learning Objectives:**
- Design an effective S3 data lake folder structure
- Implement partitioning strategies for efficient querying
- Configure S3 storage classes and lifecycle policies
- Set up data lake security controls
- Enable cross-region replication for disaster recovery

**AWS Services Used:**
- Amazon S3
- AWS Glue Data Catalog
- Amazon Athena
- AWS IAM

**Estimated Time:** 2 hours

**Estimated Cost:** $2-5 (Most resources fall under Free Tier if available)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for S3, Glue, and Athena
- Sample dataset (e-commerce data provided in resources)
- Basic understanding of data organization concepts

## Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────────┐
│                           S3 Data Lake                              │
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐             │
│  │             │    │             │    │             │             │
│  │  Raw Zone   │    │ Curated Zone│    │Analytics Zone│             │
│  │             │    │             │    │             │             │
│  └─────────────┘    └─────────────┘    └─────────────┘             │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    Partitioning Strategy                        ││
│  │                                                                 ││
│  │  /domain/entity/year=YYYY/month=MM/day=DD/data_files           ││
│  └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────┐          ┌─────────────┐          ┌─────────────┐
│             │          │             │          │             │
│  AWS Glue   │◄────────▶│   Athena    │◄────────▶│ QuickSight  │
│  Catalog    │          │             │          │ (Optional)  │
│             │          │             │          │             │
└─────────────┘          └─────────────┘          └─────────────┘
```

## Implementation Steps

### Step 1: Create S3 Bucket with Multi-Zone Structure
1. Sign in to the AWS Management Console and navigate to the S3 service
2. Create a new S3 bucket with a unique name (e.g., `your-name-datalake-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-datalake-YYYYMMDD
   ```
3. Create the following folder structure in your bucket:
   - `raw/` - For raw, unmodified data
   - `curated/` - For cleaned, transformed data
   - `analytics/` - For aggregated, analysis-ready data
   - `tmp/` - For temporary processing files
   - `archive/` - For historical data moved to cheaper storage
   ```
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key raw/
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key curated/
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key analytics/
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key tmp/
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key archive/
   ```

### Step 2: Implement Partitioning Strategy
1. Within each zone, create a domain-based structure for the e-commerce dataset:
   ```
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key raw/ecommerce/
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key raw/ecommerce/orders/
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key raw/ecommerce/customers/
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key raw/ecommerce/products/
   ```

2. Create a partitioned structure for time-based data:
   ```
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key raw/ecommerce/orders/year=2023/
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key raw/ecommerce/orders/year=2023/month=01/
   aws s3api put-object --bucket your-name-datalake-YYYYMMDD --key raw/ecommerce/orders/year=2023/month=01/day=01/
   ```

### Step 3: Upload Sample Data with Partitioning
1. Download the sample e-commerce dataset from the provided resource link
2. Upload the sample data to the appropriate partitioned folders:
   ```
   aws s3 cp ./sample-data/orders_20230101.csv s3://your-name-datalake-YYYYMMDD/raw/ecommerce/orders/year=2023/month=01/day=01/
   aws s3 cp ./sample-data/customers.csv s3://your-name-datalake-YYYYMMDD/raw/ecommerce/customers/
   aws s3 cp ./sample-data/products.csv s3://your-name-datalake-YYYYMMDD/raw/ecommerce/products/
   ```

### Step 4: Configure S3 Storage Classes and Lifecycle Policies
1. Navigate to the S3 console and select your bucket
2. Go to the "Management" tab and click "Create lifecycle rule"
3. Create a rule named "Archive-Old-Data" with the following configuration:
   - Filter: Prefix = "raw/ecommerce/orders/"
   - Transition actions:
     - Transition to Standard-IA after 90 days
     - Transition to Glacier after 180 days
   - Expiration actions:
     - Delete objects after 730 days (optional)
4. Create another rule named "Clean-Temp-Files" with the following configuration:
   - Filter: Prefix = "tmp/"
   - Expiration actions:
     - Delete objects after 7 days

### Step 5: Set Up Data Lake Security
1. Enable default encryption for your S3 bucket using SSE-S3
   ```
   aws s3api put-bucket-encryption \
     --bucket your-name-datalake-YYYYMMDD \
     --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'
   ```

2. Create a bucket policy that restricts access to specific IAM roles:
   ```
   aws s3api put-bucket-policy \
     --bucket your-name-datalake-YYYYMMDD \
     --policy '{
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Principal": {
             "AWS": "arn:aws:iam::<your-account-id>:role/DataLakeAccessRole"
           },
           "Action": [
             "s3:GetObject",
             "s3:ListBucket"
           ],
           "Resource": [
             "arn:aws:s3:::your-name-datalake-YYYYMMDD",
             "arn:aws:s3:::your-name-datalake-YYYYMMDD/*"
           ]
         }
       ]
     }'
   ```

### Step 6: Create AWS Glue Crawler for the Data Lake
1. Navigate to the AWS Glue console
2. Create a new crawler named "DataLakeCrawler"
3. Configure the crawler to scan the following paths:
   - s3://your-name-datalake-YYYYMMDD/raw/ecommerce/orders/
   - s3://your-name-datalake-YYYYMMDD/raw/ecommerce/customers/
   - s3://your-name-datalake-YYYYMMDD/raw/ecommerce/products/
4. Create a new database called "ecommerce_db"
5. Run the crawler to catalog the data

### Step 7: Query Data with Athena
1. Navigate to the Amazon Athena console
2. Set up a query result location: `s3://your-name-datalake-YYYYMMDD/tmp/athena-results/`
3. Run a sample query that demonstrates partition pruning:
   ```sql
   SELECT 
     o.order_id, 
     o.order_date, 
     c.customer_name,
     p.product_name
   FROM 
     ecommerce_db.orders o
   JOIN 
     ecommerce_db.customers c ON o.customer_id = c.customer_id
   JOIN 
     ecommerce_db.products p ON o.product_id = p.product_id
   WHERE 
     year = '2023' AND month = '01'
   LIMIT 10;
   ```

## Validation Steps
1. Verify that the S3 bucket structure is correctly set up with all zones and partitions
2. Confirm that the lifecycle policies are properly configured
3. Check that the Glue crawler has successfully created tables with partition recognition
4. Verify that Athena queries can efficiently filter by partitions
5. Confirm that the bucket policy is correctly restricting access

## Cleanup Instructions
1. Delete the Athena query results
   ```
   aws s3 rm s3://your-name-datalake-YYYYMMDD/tmp/athena-results/ --recursive
   ```
2. Delete the Glue crawler and database
   ```
   aws glue delete-crawler --name DataLakeCrawler
   aws glue delete-database --name ecommerce_db
   ```
3. Delete the S3 bucket and its contents
   ```
   aws s3 rb s3://your-name-datalake-YYYYMMDD --force
   ```

## Challenge Extensions (Optional)
1. Implement cross-region replication for disaster recovery
2. Set up S3 event notifications to trigger Lambda functions when new data arrives
3. Create a data catalog using AWS Lake Formation with fine-grained access controls
4. Implement S3 Access Points for different user groups
5. Set up S3 Inventory to track objects and their metadata

## Additional Resources
- [AWS S3 Data Lake Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/build-a-data-lake-using-amazon-s3.html)
- [Optimizing Amazon S3 Performance](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html)
- [S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/)
- [Partitioning Data on Amazon S3](https://docs.aws.amazon.com/athena/latest/ug/partitions.html)

## Notes and Tips
- Choose partition keys based on common query patterns to maximize query efficiency
- Consider using a prefix strategy that places frequently accessed data first
- For large datasets, consider using S3 Inventory to track objects and their metadata
- Use appropriate file formats (Parquet, ORC) for analytical data to improve query performance
- Monitor S3 access patterns using S3 Analytics to optimize storage class decisions
