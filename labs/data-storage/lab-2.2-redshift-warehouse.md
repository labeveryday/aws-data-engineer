# Lab 2.2: Amazon Redshift Data Warehouse Setup

## Overview
This lab focuses on setting up and optimizing an Amazon Redshift data warehouse. You will learn how to design efficient tables with appropriate distribution and sort keys, load data from S3, and optimize query performance, which are essential skills for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Create and configure an Amazon Redshift cluster
- Design tables with appropriate distribution and sort keys
- Load data efficiently from S3 into Redshift
- Implement table optimization techniques
- Monitor and tune query performance
- Use Redshift Spectrum to query data in S3

**AWS Services Used:**
- Amazon Redshift
- Amazon S3
- AWS Glue (for Redshift Spectrum)
- Amazon CloudWatch
- AWS Identity and Access Management (IAM)

**Estimated Time:** 3 hours

**Estimated Cost:** $5-10 (Redshift has hourly charges)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for Redshift, S3, and Glue
- Basic understanding of SQL and data warehousing concepts
- Familiarity with database performance concepts

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│  S3 Bucket  │────▶│  Redshift   │────▶│  BI Tool    │
│  (Data)     │     │  Cluster    │     │  (Optional) │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          │
                          ▼
┌─────────────┐     ┌─────────────┐
│             │     │             │
│  S3 Bucket  │◀───▶│  Redshift   │
│  (External) │     │  Spectrum   │
│             │     │             │
└─────────────┘     └─────────────┘
```

## Implementation Steps

### Step 1: Create an S3 Bucket for Data
1. Sign in to the AWS Management Console and navigate to the S3 service
2. Create a new S3 bucket with a unique name (e.g., `your-name-redshift-data-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-redshift-data-YYYYMMDD
   ```
3. Create the following folder structure:
   ```
   aws s3api put-object --bucket your-name-redshift-data-YYYYMMDD --key load/
   aws s3api put-object --bucket your-name-redshift-data-YYYYMMDD --key spectrum/
   aws s3api put-object --bucket your-name-redshift-data-YYYYMMDD --key results/
   ```

### Step 2: Prepare Sample Data
1. Create sample CSV files for customers, products, and sales data
2. For this lab, we'll create three files:

**customers.csv**:
```
customer_id,first_name,last_name,email,city,state,created_date
1,John,Doe,john.doe@example.com,Seattle,WA,2022-01-15
2,Jane,Smith,jane.smith@example.com,Portland,OR,2022-02-20
3,Robert,Johnson,robert.j@example.com,San Francisco,CA,2022-03-10
4,Sarah,Williams,sarah.w@example.com,Los Angeles,CA,2022-04-05
5,Michael,Brown,michael.b@example.com,Denver,CO,2022-05-12
6,Emily,Davis,emily.d@example.com,Chicago,IL,2022-06-18
7,David,Miller,david.m@example.com,Boston,MA,2022-07-22
8,Lisa,Wilson,lisa.w@example.com,Miami,FL,2022-08-30
9,James,Taylor,james.t@example.com,Austin,TX,2022-09-14
10,Jennifer,Anderson,jennifer.a@example.com,Phoenix,AZ,2022-10-05
```

**products.csv**:
```
product_id,product_name,category,price,cost,launch_date
101,Laptop Pro,Electronics,1299.99,900.00,2022-01-10
102,Smartphone X,Electronics,899.99,600.00,2022-02-15
103,Coffee Maker,Home Appliances,79.99,45.00,2022-03-20
104,Running Shoes,Sportswear,129.99,70.00,2022-04-25
105,Wireless Headphones,Electronics,149.99,85.00,2022-05-30
106,Blender Pro,Home Appliances,89.99,50.00,2022-06-05
107,Fitness Tracker,Electronics,129.99,75.00,2022-07-10
108,Gaming Console,Electronics,499.99,350.00,2022-08-15
109,Yoga Mat,Sportswear,39.99,20.00,2022-09-20
110,Smart Watch,Electronics,249.99,150.00,2022-10-25
```

**sales.csv** (generate a larger file with ~1000 rows for better testing):
```
sale_id,customer_id,product_id,sale_date,quantity,total_amount
10001,1,101,2023-01-10,1,1299.99
10002,2,102,2023-01-15,1,899.99
10003,3,103,2023-01-20,2,159.98
10004,4,104,2023-01-25,1,129.99
10005,5,105,2023-01-30,1,149.99
10006,6,106,2023-02-05,1,89.99
10007,7,107,2023-02-10,1,129.99
10008,8,108,2023-02-15,1,499.99
10009,9,109,2023-02-20,2,79.98
10010,10,110,2023-02-25,1,249.99
...
```

3. Upload these files to your S3 bucket:
   ```
   aws s3 cp customers.csv s3://your-name-redshift-data-YYYYMMDD/load/
   aws s3 cp products.csv s3://your-name-redshift-data-YYYYMMDD/load/
   aws s3 cp sales.csv s3://your-name-redshift-data-YYYYMMDD/load/
   ```

### Step 3: Create an IAM Role for Redshift
1. Navigate to the IAM console
2. Create a new role with the following permissions:
   - AmazonS3ReadOnlyAccess
   - AWSGlueConsoleFullAccess (for Redshift Spectrum)
3. Name the role `RedshiftLabRole`

### Step 4: Create a Redshift Cluster
1. Navigate to the Amazon Redshift console
2. Click "Create cluster"
3. Configure the cluster:
   - Cluster identifier: `redshift-lab-cluster`
   - Node type: dc2.large (for lab purposes)
   - Number of nodes: 2
   - Database name: `retail`
   - Admin username: `admin`
   - Admin password: Create and save a secure password
4. For network and security:
   - Choose a VPC and subnet
   - Enable "Publicly accessible" (for lab purposes)
   - Create a new security group or use an existing one
5. Associate the IAM role you created
6. Create the cluster and wait for it to become available

### Step 5: Connect to the Redshift Cluster
1. Use a SQL client (like the Redshift Query Editor in the console) to connect to your cluster
2. Connect using the admin credentials you created

### Step 6: Create Tables with Appropriate Distribution and Sort Keys
1. Create a schema for your data warehouse:
   ```sql
   CREATE SCHEMA retail;
   SET search_path TO retail;
   ```

2. Create the customers table with EVEN distribution (small dimension table):
   ```sql
   CREATE TABLE retail.customers (
     customer_id INT PRIMARY KEY,
     first_name VARCHAR(50),
     last_name VARCHAR(50),
     email VARCHAR(100),
     city VARCHAR(50),
     state CHAR(2),
     created_date DATE
   )
   DISTSTYLE ALL;  -- Small dimension table, replicate to all nodes
   ```

3. Create the products table with EVEN distribution (small dimension table):
   ```sql
   CREATE TABLE retail.products (
     product_id INT PRIMARY KEY,
     product_name VARCHAR(100),
     category VARCHAR(50),
     price DECIMAL(10,2),
     cost DECIMAL(10,2),
     launch_date DATE
   )
   DISTSTYLE ALL;  -- Small dimension table, replicate to all nodes
   ```

4. Create the sales table with KEY distribution and compound sort key:
   ```sql
   CREATE TABLE retail.sales (
     sale_id INT,
     customer_id INT REFERENCES retail.customers(customer_id),
     product_id INT REFERENCES retail.products(product_id),
     sale_date DATE,
     quantity INT,
     total_amount DECIMAL(10,2),
     PRIMARY KEY (sale_id)
   )
   DISTSTYLE KEY DISTKEY(customer_id)  -- Distribute by customer_id for joins
   SORTKEY (sale_date, customer_id);   -- Sort by date for time-based queries
   ```

### Step 7: Load Data from S3 into Redshift
1. Load the customers data:
   ```sql
   COPY retail.customers
   FROM 's3://your-name-redshift-data-YYYYMMDD/load/customers.csv'
   IAM_ROLE 'arn:aws:iam::<your-account-id>:role/RedshiftLabRole'
   CSV IGNOREHEADER 1;
   ```

2. Load the products data:
   ```sql
   COPY retail.products
   FROM 's3://your-name-redshift-data-YYYYMMDD/load/products.csv'
   IAM_ROLE 'arn:aws:iam::<your-account-id>:role/RedshiftLabRole'
   CSV IGNOREHEADER 1;
   ```

3. Load the sales data:
   ```sql
   COPY retail.sales
   FROM 's3://your-name-redshift-data-YYYYMMDD/load/sales.csv'
   IAM_ROLE 'arn:aws:iam::<your-account-id>:role/RedshiftLabRole'
   CSV IGNOREHEADER 1;
   ```

### Step 8: Analyze Table Design and Query Performance
1. Run ANALYZE to update statistics:
   ```sql
   ANALYZE;
   ```

2. Run VACUUM to sort and reclaim space:
   ```sql
   VACUUM;
   ```

3. Run a simple query to test performance:
   ```sql
   SELECT 
     c.first_name,
     c.last_name,
     p.product_name,
     s.sale_date,
     s.quantity,
     s.total_amount
   FROM 
     retail.sales s
   JOIN 
     retail.customers c ON s.customer_id = c.customer_id
   JOIN 
     retail.products p ON s.product_id = p.product_id
   WHERE 
     s.sale_date BETWEEN '2023-01-01' AND '2023-01-31'
   ORDER BY 
     s.sale_date;
   ```

4. Examine the query plan:
   ```sql
   EXPLAIN
   SELECT 
     c.first_name,
     c.last_name,
     p.product_name,
     s.sale_date,
     s.quantity,
     s.total_amount
   FROM 
     retail.sales s
   JOIN 
     retail.customers c ON s.customer_id = c.customer_id
   JOIN 
     retail.products p ON s.product_id = p.product_id
   WHERE 
     s.sale_date BETWEEN '2023-01-01' AND '2023-01-31'
   ORDER BY 
     s.sale_date;
   ```

### Step 9: Create a View for Sales Analysis
1. Create a view that summarizes sales by category and month:
   ```sql
   CREATE VIEW retail.monthly_sales_by_category AS
   SELECT 
     p.category,
     DATE_TRUNC('month', s.sale_date) AS month,
     SUM(s.quantity) AS total_quantity,
     SUM(s.total_amount) AS total_sales,
     SUM(s.total_amount - (p.cost * s.quantity)) AS total_profit
   FROM 
     retail.sales s
   JOIN 
     retail.products p ON s.product_id = p.product_id
   GROUP BY 
     p.category, DATE_TRUNC('month', s.sale_date)
   ORDER BY 
     month, p.category;
   ```

2. Query the view:
   ```sql
   SELECT * FROM retail.monthly_sales_by_category;
   ```

### Step 10: Set Up Redshift Spectrum for External Tables
1. Create an external schema using AWS Glue Data Catalog:
   ```sql
   CREATE EXTERNAL SCHEMA spectrum
   FROM DATA CATALOG
   DATABASE 'spectrum_db'
   IAM_ROLE 'arn:aws:iam::<your-account-id>:role/RedshiftLabRole'
   CREATE EXTERNAL DATABASE IF NOT EXISTS;
   ```

2. Create an external table pointing to data in S3:
   ```sql
   CREATE EXTERNAL TABLE spectrum.sales_history (
     sale_id INT,
     customer_id INT,
     product_id INT,
     sale_date DATE,
     quantity INT,
     total_amount DECIMAL(10,2)
   )
   ROW FORMAT DELIMITED
   FIELDS TERMINATED BY ','
   STORED AS TEXTFILE
   LOCATION 's3://your-name-redshift-data-YYYYMMDD/spectrum/'
   TABLE PROPERTIES ('skip.header.line.count'='1');
   ```

3. Upload historical sales data to the spectrum folder:
   ```
   aws s3 cp sales_history.csv s3://your-name-redshift-data-YYYYMMDD/spectrum/
   ```

4. Query data across both Redshift tables and external S3 data:
   ```sql
   SELECT 
     'Current' AS data_source,
     DATE_TRUNC('month', sale_date) AS month,
     COUNT(*) AS sale_count,
     SUM(total_amount) AS total_sales
   FROM 
     retail.sales
   GROUP BY 
     DATE_TRUNC('month', sale_date)
   
   UNION ALL
   
   SELECT 
     'Historical' AS data_source,
     DATE_TRUNC('month', sale_date) AS month,
     COUNT(*) AS sale_count,
     SUM(total_amount) AS total_sales
   FROM 
     spectrum.sales_history
   GROUP BY 
     DATE_TRUNC('month', sale_date)
   
   ORDER BY 
     month, data_source;
   ```

### Step 11: Monitor Query Performance
1. Check system tables for query performance:
   ```sql
   -- Recent query performance
   SELECT 
     query,
     TRIM(querytxt) AS query_text,
     starttime,
     DATEDIFF(milliseconds, starttime, endtime) AS duration_ms,
     CASE WHEN aborted = 1 THEN 'Yes' ELSE 'No' END AS aborted
   FROM 
     STL_QUERY
   WHERE 
     starttime > DATEADD(hour, -1, GETDATE())
   ORDER BY 
     starttime DESC
   LIMIT 10;
   
   -- Table scan statistics
   SELECT 
     tbl,
     perm_table_name,
     SUM(rows) AS rows_scanned,
     SUM(blocks) AS blocks_scanned
   FROM 
     SVL_QUERY_SUMMARY s
   JOIN 
     SVV_TABLE_INFO t ON s.tbl = t.table_id
   WHERE 
     s.userid > 1
     AND s.query > 1000
   GROUP BY 
     tbl, perm_table_name
   ORDER BY 
     rows_scanned DESC
   LIMIT 10;
   ```

2. Check for table skew:
   ```sql
   SELECT 
     trim(name) AS table_name,
     slice,
     count(*) AS num_rows
   FROM 
     stv_tbl_perm
   JOIN 
     stv_slices
   USING 
     (slice)
   WHERE 
     name LIKE 'retail.%'
   GROUP BY 
     name, slice
   ORDER BY 
     name, slice;
   ```

## Validation Steps
1. Verify that all tables were created with the correct distribution and sort keys
2. Confirm that data was loaded correctly into all tables
3. Check that queries run efficiently and use the distribution and sort keys
4. Verify that Redshift Spectrum can query external data in S3
5. Review query performance metrics to identify any issues

## Cleanup Instructions
1. Delete the Redshift cluster
   ```
   aws redshift delete-cluster --cluster-identifier redshift-lab-cluster --skip-final-cluster-snapshot
   ```
2. Delete the S3 bucket and its contents
   ```
   aws s3 rb s3://your-name-redshift-data-YYYYMMDD --force
   ```
3. Delete the IAM role
   ```
   aws iam delete-role --role-name RedshiftLabRole
   ```

## Challenge Extensions (Optional)
1. Implement table compression encodings to reduce storage requirements
2. Create materialized views for frequently run complex queries
3. Set up workload management (WLM) queues for different query types
4. Implement column-level security using Redshift's security features
5. Set up cross-region snapshot copy for disaster recovery

## Additional Resources
- [Amazon Redshift Database Developer Guide](https://docs.aws.amazon.com/redshift/latest/dg/welcome.html)
- [Redshift Best Practices](https://docs.aws.amazon.com/redshift/latest/dg/best-practices.html)
- [Redshift Spectrum Documentation](https://docs.aws.amazon.com/redshift/latest/dg/c-using-spectrum.html)
- [Analyzing Table Design](https://docs.aws.amazon.com/redshift/latest/dg/c_analyzing-table-design.html)

## Notes and Tips
- Choose distribution keys based on join columns for large tables
- Use DISTKEY for columns frequently used in joins
- Use SORTKEY for columns frequently used in WHERE clauses and range filters
- ALL distribution is suitable only for small dimension tables
- Run ANALYZE after major data loads to update statistics
- Run VACUUM after deletes or updates to reclaim space and resort data
- Monitor for table skew to ensure even data distribution across nodes
