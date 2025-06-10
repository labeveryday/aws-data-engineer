# Lab 4.3: Cross-Account Data Sharing

## Overview
This lab focuses on implementing secure cross-account data sharing using various AWS services. You will learn how to share data across AWS accounts while maintaining security and governance controls, which is an essential skill for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Configure cross-account data sharing using AWS Lake Formation
- Implement Amazon Redshift datashares
- Set up cross-account access to S3 data
- Use AWS RAM (Resource Access Manager) for sharing resources
- Implement cross-account data catalog access
- Monitor and audit cross-account data access
- Apply appropriate security controls for shared data

**AWS Services Used:**
- AWS Lake Formation
- Amazon Redshift
- Amazon S3
- AWS Resource Access Manager (RAM)
- AWS Glue
- AWS Identity and Access Management (IAM)
- AWS CloudTrail
- AWS KMS (Key Management Service)

**Estimated Time:** 3-4 hours

**Estimated Cost:** $10-15 (Redshift charges apply)

## Prerequisites
- Two AWS accounts (producer and consumer)
- IAM permissions for Lake Formation, Redshift, S3, and RAM in both accounts
- Basic understanding of cross-account access patterns
- Familiarity with data sharing concepts

## Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Producer Account                                   │
│                                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐│
│  │             │     │             │     │             │     │             ││
│  │  S3 Data    │────▶│  AWS Lake   │────▶│  AWS Glue   │────▶│  Redshift   ││
│  │  Lake       │     │  Formation  │     │  Catalog    │     │  Cluster    ││
│  │             │     │             │     │             │     │             ││
│  └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘│
│                            │                    │                   │        │
└────────────────────────────│────────────────────│───────────────────│────────┘
                             │                    │                   │
                             ▼                    ▼                   ▼
┌────────────────────────────│────────────────────│───────────────────│────────┐
│                            │                    │                   │        │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐│
│  │             │     │             │     │             │     │             ││
│  │  IAM Roles  │◀───▶│  AWS Lake   │◀───▶│  AWS Glue   │◀───▶│  Redshift   ││
│  │             │     │  Formation  │     │  Catalog    │     │  Cluster    ││
│  └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘│
│                                                                             │
│                           Consumer Account                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Implementation Steps

### Step 1: Set Up Producer Account Resources

#### 1.1: Create S3 Bucket for Data Lake
1. Sign in to the producer AWS account
2. Navigate to the S3 service
3. Create a new S3 bucket with a unique name (e.g., `producer-data-sharing-YYYYMMDD`)
   ```
   aws s3 mb s3://producer-data-sharing-YYYYMMDD
   ```
4. Create the following folder structure:
   ```
   aws s3api put-object --bucket producer-data-sharing-YYYYMMDD --key data/
   ```

#### 1.2: Prepare Sample Data
1. Create a sample CSV file for sales data (`sales_data.csv`):
```
sale_id,product_id,product_name,category,sale_date,quantity,unit_price,total_amount,customer_id,region
1001,P100,Laptop Pro,Electronics,2023-01-10,1,1299.99,1299.99,C001,North
1002,P101,Smartphone X,Electronics,2023-01-15,1,899.99,899.99,C002,South
1003,P102,Coffee Maker,Home Appliances,2023-01-20,2,79.99,159.98,C003,East
1004,P103,Running Shoes,Sportswear,2023-01-25,1,129.99,129.99,C004,West
1005,P104,Wireless Headphones,Electronics,2023-01-30,1,149.99,149.99,C005,North
1006,P100,Laptop Pro,Electronics,2023-02-05,1,1299.99,1299.99,C006,South
1007,P101,Smartphone X,Electronics,2023-02-10,1,899.99,899.99,C007,East
1008,P105,Gaming Console,Electronics,2023-02-15,1,499.99,499.99,C008,West
1009,P106,Yoga Mat,Sportswear,2023-02-20,2,39.99,79.98,C009,North
1010,P107,Smart Watch,Electronics,2023-02-25,1,249.99,249.99,C010,South
```

2. Create a sample CSV file for customer data (`customer_data.csv`):
```
customer_id,first_name,last_name,email,phone,address,city,state,zip_code,registration_date
C001,John,Doe,john.doe@example.com,555-123-4567,123 Main St,Seattle,WA,98101,2022-01-15
C002,Jane,Smith,jane.smith@example.com,555-987-6543,456 Oak Ave,Portland,OR,97205,2022-02-20
C003,Robert,Johnson,robert.j@example.com,555-456-7890,789 Pine Rd,San Francisco,CA,94105,2022-03-10
C004,Sarah,Williams,sarah.w@example.com,555-789-0123,101 Cedar Ln,Los Angeles,CA,90001,2022-04-05
C005,Michael,Brown,michael.b@example.com,555-234-5678,202 Elm St,Denver,CO,80201,2022-05-12
C006,Emily,Davis,emily.d@example.com,555-345-6789,303 Maple Dr,Chicago,IL,60601,2022-06-18
C007,David,Miller,david.m@example.com,555-456-7890,404 Birch Blvd,Boston,MA,02108,2022-07-22
C008,Lisa,Wilson,lisa.w@example.com,555-567-8901,505 Walnut St,Miami,FL,33101,2022-08-30
C009,James,Taylor,james.t@example.com,555-678-9012,606 Cherry Ave,Austin,TX,78701,2022-09-14
C010,Jennifer,Anderson,jennifer.a@example.com,555-789-0123,707 Spruce Ct,Phoenix,AZ,85001,2022-10-05
```

3. Upload these files to your S3 bucket:
   ```
   aws s3 cp sales_data.csv s3://producer-data-sharing-YYYYMMDD/data/sales/
   aws s3 cp customer_data.csv s3://producer-data-sharing-YYYYMMDD/data/customers/
   ```

#### 1.3: Set Up AWS Lake Formation in Producer Account
1. Navigate to the AWS Lake Formation console
2. Complete the initial setup if this is your first time using Lake Formation
3. For "Administrators", add your current IAM user or role
4. For "Database creators", add your current IAM user or role
5. Uncheck "Use only IAM access control for new databases" to enable Lake Formation permissions

#### 1.4: Register Data Lake Location
1. In the Lake Formation console, go to "Register and ingest" > "Data lake locations"
2. Click "Register location"
3. Select your S3 bucket: `s3://producer-data-sharing-YYYYMMDD`
4. For IAM role, create or select a role with appropriate S3 permissions
5. Register the location

#### 1.5: Create a Database in the Glue Data Catalog
1. In the Lake Formation console, go to "Data catalog" > "Databases"
2. Click "Create database"
3. Name the database `shared_data`
4. Leave other settings as default
5. Create the database

#### 1.6: Create Crawlers to Catalog the Data
1. Navigate to the AWS Glue console
2. Go to "Crawlers" and click "Create crawler"
3. Name the crawler `sales_data_crawler`
4. For data source, choose S3 and specify your bucket path: `s3://producer-data-sharing-YYYYMMDD/data/sales/`
5. Create or select an IAM role with appropriate permissions
6. For output, select the `shared_data` database
7. Set the crawler schedule to run on demand
8. Create the crawler and run it
9. Create another crawler named `customer_data_crawler` for the customer data path
10. Run both crawlers and wait for them to complete

#### 1.7: Set Up Amazon Redshift in Producer Account
1. Navigate to the Amazon Redshift console
2. Click "Create cluster"
3. Configure the cluster:
   - Cluster identifier: `producer-redshift-cluster`
   - Node type: dc2.large (for lab purposes)
   - Number of nodes: 2
   - Database name: `shared_data`
   - Admin username: `admin`
   - Admin password: Create and save a secure password
4. For network and security:
   - Choose a VPC and subnet
   - Enable "Publicly accessible" (for lab purposes)
   - Create a new security group or use an existing one
5. Create the cluster and wait for it to become available

#### 1.8: Load Data into Redshift
1. Use a SQL client (like the Redshift Query Editor in the console) to connect to your cluster
2. Create tables for the sales and customer data:

```sql
-- Create schema
CREATE SCHEMA shared_data;
SET search_path TO shared_data;

-- Create sales table
CREATE TABLE sales (
    sale_id INT,
    product_id VARCHAR(10),
    product_name VARCHAR(100),
    category VARCHAR(50),
    sale_date DATE,
    quantity INT,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    customer_id VARCHAR(10),
    region VARCHAR(20)
);

-- Create customers table
CREATE TABLE customers (
    customer_id VARCHAR(10),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(2),
    zip_code VARCHAR(10),
    registration_date DATE
);
```

3. Load data from S3 into Redshift:

```sql
-- Load sales data
COPY shared_data.sales
FROM 's3://producer-data-sharing-YYYYMMDD/data/sales/sales_data.csv'
IAM_ROLE 'arn:aws:iam::<producer-account-id>:role/RedshiftLoadRole'
CSV IGNOREHEADER 1;

-- Load customer data
COPY shared_data.customers
FROM 's3://producer-data-sharing-YYYYMMDD/data/customers/customer_data.csv'
IAM_ROLE 'arn:aws:iam::<producer-account-id>:role/RedshiftLoadRole'
CSV IGNOREHEADER 1;
```

### Step 2: Set Up Consumer Account Resources

#### 2.1: Create IAM Role for Cross-Account Access
1. Sign in to the consumer AWS account
2. Navigate to the IAM console
3. Create a new role with the following settings:
   - Trusted entity: Another AWS account
   - Account ID: Enter the producer account ID
   - Name the role `CrossAccountDataAccessRole`
   - Attach the following policies:
     - AmazonS3ReadOnlyAccess
     - AWSGlueConsoleFullAccess
     - AmazonAthenaFullAccess
     - AmazonRedshiftFullAccess

#### 2.2: Set Up AWS Lake Formation in Consumer Account
1. Navigate to the AWS Lake Formation console
2. Complete the initial setup if this is your first time using Lake Formation
3. For "Administrators", add your current IAM user or role
4. For "Database creators", add your current IAM user or role

#### 2.3: Set Up Amazon Redshift in Consumer Account
1. Navigate to the Amazon Redshift console
2. Click "Create cluster"
3. Configure the cluster:
   - Cluster identifier: `consumer-redshift-cluster`
   - Node type: dc2.large (for lab purposes)
   - Number of nodes: 2
   - Database name: `shared_data`
   - Admin username: `admin`
   - Admin password: Create and save a secure password
4. For network and security:
   - Choose a VPC and subnet
   - Enable "Publicly accessible" (for lab purposes)
   - Create a new security group or use an existing one
5. Create the cluster and wait for it to become available

### Step 3: Configure Cross-Account Data Sharing with Lake Formation

#### 3.1: Create a Resource Link in Producer Account
1. Sign in to the producer AWS account
2. Navigate to the Lake Formation console
3. Go to "Data catalog" > "Databases"
4. Select the `shared_data` database
5. Click "Actions" > "Create resource link"
6. Configure the resource link:
   - Resource link name: `shared_data_link`
   - Database: `shared_data`
7. Create the resource link

#### 3.2: Share the Database with Consumer Account
1. In the Lake Formation console, go to "Permissions" > "Data lake permissions"
2. Click "Grant"
3. Configure the permissions:
   - Principal: External accounts
   - AWS account ID: Enter the consumer account ID
   - Resources: Databases
   - Database: `shared_data`
   - Permissions: Describe, Select
4. Grant the permissions

#### 3.3: Share Tables with Consumer Account
1. In the Lake Formation console, go to "Permissions" > "Data lake permissions"
2. Click "Grant"
3. Configure the permissions:
   - Principal: External accounts
   - AWS account ID: Enter the consumer account ID
   - Resources: Tables
   - Database: `shared_data`
   - Tables: Select both `sales_data` and `customer_data`
   - Table permissions: Describe, Select
   - Grantable permissions: None
4. Grant the permissions

#### 3.4: Accept Resource Share in Consumer Account
1. Sign in to the consumer AWS account
2. Navigate to the Lake Formation console
3. Go to "Data catalog" > "Databases"
4. Click "Shared with me"
5. You should see the `shared_data` database from the producer account
6. Select the database and click "Accept"
7. The shared database and tables should now be available in your Data Catalog

### Step 4: Configure Cross-Account Data Sharing with Redshift

#### 4.1: Create a Datashare in Producer Account
1. Sign in to the producer AWS account
2. Connect to the Redshift cluster using the Query Editor
3. Create a datashare:

```sql
-- Create a datashare
CREATE DATASHARE sales_share;

-- Add schema and tables to the datashare
ALTER DATASHARE sales_share ADD SCHEMA shared_data;
ALTER DATASHARE sales_share ADD TABLE shared_data.sales;
ALTER DATASHARE sales_share ADD TABLE shared_data.customers;

-- Grant usage on datashare to consumer account
GRANT USAGE ON DATASHARE sales_share TO ACCOUNT '<consumer-account-id>';
```

#### 4.2: Create a Database from Datashare in Consumer Account
1. Sign in to the consumer AWS account
2. Connect to the Redshift cluster using the Query Editor
3. Create a database from the datashare:

```sql
-- Create a database from the datashare
CREATE DATABASE sales_from_producer FROM DATASHARE sales_share OF ACCOUNT '<producer-account-id>' NAMESPACE '<producer-namespace>';

-- Grant permissions to users
GRANT USAGE ON DATABASE sales_from_producer TO PUBLIC;
GRANT USAGE ON SCHEMA sales_from_producer.shared_data TO PUBLIC;
GRANT SELECT ON ALL TABLES IN SCHEMA sales_from_producer.shared_data TO PUBLIC;
```

### Step 5: Configure Cross-Account S3 Access

#### 5.1: Update S3 Bucket Policy in Producer Account
1. Sign in to the producer AWS account
2. Navigate to the S3 console
3. Select your bucket `producer-data-sharing-YYYYMMDD`
4. Go to "Permissions" > "Bucket policy"
5. Add the following policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<consumer-account-id>:role/CrossAccountDataAccessRole"
            },
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::producer-data-sharing-YYYYMMDD",
                "arn:aws:s3:::producer-data-sharing-YYYYMMDD/*"
            ]
        }
    ]
}
```

#### 5.2: Test Cross-Account S3 Access
1. Sign in to the consumer AWS account
2. Navigate to the IAM console
3. Go to "Roles" and select `CrossAccountDataAccessRole`
4. Click "Switch role" to assume this role
5. Navigate to the S3 console
6. Try to access the producer's bucket: `producer-data-sharing-YYYYMMDD`
7. You should be able to list and view objects in the bucket

### Step 6: Test Cross-Account Data Access

#### 6.1: Test Lake Formation Cross-Account Access
1. Sign in to the consumer AWS account
2. Navigate to the Athena console
3. Set up a query result location if not already configured
4. In the query editor, you should see the shared database from the producer account
5. Run a query to test access:

```sql
SELECT * FROM "shared_data"."sales_data" LIMIT 10;
SELECT * FROM "shared_data"."customer_data" LIMIT 10;
```

#### 6.2: Test Redshift Cross-Account Access
1. Sign in to the consumer AWS account
2. Connect to the Redshift cluster using the Query Editor
3. Run queries to test access to the shared data:

```sql
-- Query shared sales data
SELECT * FROM sales_from_producer.shared_data.sales LIMIT 10;

-- Query shared customer data
SELECT * FROM sales_from_producer.shared_data.customers LIMIT 10;

-- Join shared tables
SELECT 
    s.sale_id,
    s.product_name,
    s.sale_date,
    s.total_amount,
    c.first_name,
    c.last_name,
    c.city,
    c.state
FROM 
    sales_from_producer.shared_data.sales s
JOIN 
    sales_from_producer.shared_data.customers c ON s.customer_id = c.customer_id
LIMIT 10;
```

### Step 7: Monitor Cross-Account Data Access

#### 7.1: Set Up CloudTrail for Cross-Account Monitoring
1. Sign in to the producer AWS account
2. Navigate to the CloudTrail console
3. Create a trail if you don't have one already
4. Configure the trail to log data events for your S3 bucket and Glue Data Catalog
5. Enable the option to log events from other accounts

#### 7.2: Create CloudWatch Dashboard for Monitoring
1. Navigate to the CloudWatch console
2. Click "Dashboards" and then "Create dashboard"
3. Name the dashboard `Cross-Account-Data-Sharing-Dashboard`
4. Add widgets to monitor:
   - S3 access metrics
   - Lake Formation permission checks
   - Redshift datashare usage

## Validation Steps
1. Verify that the consumer account can access shared Lake Formation tables
2. Confirm that the consumer account can query shared Redshift data
3. Check that the consumer account can access shared S3 objects
4. Verify that CloudTrail logs show cross-account access
5. Confirm that only authorized resources are accessible

## Cleanup Instructions
1. In the consumer account:
   - Drop the database created from the datashare
   ```sql
   DROP DATABASE sales_from_producer;
   ```
   - Delete the Redshift cluster
   ```
   aws redshift delete-cluster --cluster-identifier consumer-redshift-cluster --skip-final-cluster-snapshot
   ```
   - Delete the IAM role
   ```
   aws iam delete-role --role-name CrossAccountDataAccessRole
   ```

2. In the producer account:
   - Delete the datashare
   ```sql
   DROP DATASHARE sales_share;
   ```
   - Delete the Redshift cluster
   ```
   aws redshift delete-cluster --cluster-identifier producer-redshift-cluster --skip-final-cluster-snapshot
   ```
   - Revoke Lake Formation permissions
   ```
   # Use Lake Formation console to revoke permissions
   ```
   - Delete the resource link
   ```
   # Use Lake Formation console to delete resource link
   ```
   - Delete the Glue crawlers
   ```
   aws glue delete-crawler --name sales_data_crawler
   aws glue delete-crawler --name customer_data_crawler
   ```
   - Delete the Glue database and tables
   ```
   aws glue delete-database --name shared_data
   ```
   - Deregister the data lake location
   ```
   # Use Lake Formation console to deregister location
   ```
   - Delete the S3 bucket and its contents
   ```
   aws s3 rb s3://producer-data-sharing-YYYYMMDD --force
   ```
   - Delete the CloudWatch dashboard
   ```
   aws cloudwatch delete-dashboards --dashboard-names Cross-Account-Data-Sharing-Dashboard
   ```

## Challenge Extensions (Optional)
1. Implement column-level security for cross-account data sharing
2. Set up cross-account data sharing with AWS KMS encryption
3. Create a cross-account ETL pipeline using the shared data
4. Implement cross-account data sharing with AWS RAM
5. Set up cross-account data sharing with AWS License Manager
6. Create a cross-account data catalog synchronization process

## Additional Resources
- [AWS Lake Formation Cross-Account Data Sharing](https://docs.aws.amazon.com/lake-formation/latest/dg/cross-account-permissions.html)
- [Amazon Redshift Data Sharing](https://docs.aws.amazon.com/redshift/latest/dg/datashare-overview.html)
- [Cross-Account Access in Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-walkthroughs-managing-access-example2.html)
- [AWS Resource Access Manager](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html)
- [Cross-Account CloudTrail Logging](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-receive-logs-from-multiple-accounts.html)

## Notes and Tips
- Always follow the principle of least privilege when granting cross-account access
- Use resource policies and IAM roles instead of IAM users for cross-account access
- Consider using AWS Organizations for managing multiple accounts
- Regularly audit cross-account permissions to ensure they remain appropriate
- Use AWS CloudTrail to monitor cross-account access patterns
- Consider implementing a tagging strategy for shared resources
- Document your cross-account sharing architecture and permissions
