# Lab 1.3: Database Migration with AWS DMS

## Overview
This lab focuses on migrating data from a relational database to AWS using the Database Migration Service (DMS). You will learn how to set up a migration task for both full load and change data capture (CDC), which is an essential skill for data engineers working with existing data sources.

**Learning Objectives:**
- Configure AWS DMS replication instances
- Set up source and target endpoints
- Create and run migration tasks
- Implement Change Data Capture (CDC)
- Monitor and troubleshoot migration tasks

**AWS Services Used:**
- AWS Database Migration Service (DMS)
- Amazon RDS (source database)
- Amazon S3 (target storage)
- AWS Schema Conversion Tool (optional)
- Amazon CloudWatch (for monitoring)

**Estimated Time:** 3 hours

**Estimated Cost:** $10-15 (RDS and DMS instances have hourly charges)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for DMS, RDS, and S3
- Basic understanding of relational databases and SQL
- Familiarity with database migration concepts

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│  Source     │────▶│  AWS DMS    │────▶│  Target     │
│  Database   │     │ Replication │     │  S3 Bucket  │
│  (RDS)      │     │  Instance   │     │             │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          │
                          ▼
                    ┌─────────────┐
                    │             │
                    │ CloudWatch  │
                    │ Monitoring  │
                    │             │
                    └─────────────┘
```

## Implementation Steps

### Step 1: Create a Source RDS Database
1. Navigate to the Amazon RDS console
2. Click "Create database"
3. Choose MySQL as the engine type
4. Select "Free tier" for Template (or the smallest available instance for testing)
5. Configure basic settings:
   - DB instance identifier: `source-mysql-db`
   - Master username: `admin`
   - Master password: Create and save a secure password
6. For connectivity, choose "Yes" for public access (for lab purposes only)
7. Configure advanced settings:
   - Initial database name: `retail`
   - Enable automated backups
   - Enable binary logging for CDC (set binlog retention to 24 hours)
8. Create the database and wait for it to become available

### Step 2: Populate the Source Database
1. Connect to your RDS instance using a MySQL client:
   ```
   mysql -h <your-rds-endpoint> -u admin -p
   ```

2. Create tables and insert sample data:
   ```sql
   USE retail;

   -- Create customers table
   CREATE TABLE customers (
     customer_id INT PRIMARY KEY,
     first_name VARCHAR(50),
     last_name VARCHAR(50),
     email VARCHAR(100),
     phone VARCHAR(20),
     address VARCHAR(200),
     city VARCHAR(50),
     state VARCHAR(2),
     zip_code VARCHAR(10),
     registration_date DATETIME
   );

   -- Create products table
   CREATE TABLE products (
     product_id INT PRIMARY KEY,
     product_name VARCHAR(100),
     category VARCHAR(50),
     price DECIMAL(10,2),
     stock_quantity INT,
     description TEXT
   );

   -- Create orders table
   CREATE TABLE orders (
     order_id INT PRIMARY KEY,
     customer_id INT,
     order_date DATETIME,
     total_amount DECIMAL(10,2),
     status VARCHAR(20),
     FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
   );

   -- Create order_items table
   CREATE TABLE order_items (
     item_id INT PRIMARY KEY,
     order_id INT,
     product_id INT,
     quantity INT,
     price DECIMAL(10,2),
     FOREIGN KEY (order_id) REFERENCES orders(order_id),
     FOREIGN KEY (product_id) REFERENCES products(product_id)
   );

   -- Insert sample data into customers
   INSERT INTO customers VALUES
   (1, 'John', 'Doe', 'john.doe@example.com', '555-123-4567', '123 Main St', 'Seattle', 'WA', '98101', '2022-01-15 10:30:00'),
   (2, 'Jane', 'Smith', 'jane.smith@example.com', '555-987-6543', '456 Oak Ave', 'Portland', 'OR', '97205', '2022-02-20 14:45:00'),
   (3, 'Robert', 'Johnson', 'robert.j@example.com', '555-456-7890', '789 Pine Rd', 'San Francisco', 'CA', '94105', '2022-03-10 09:15:00'),
   (4, 'Sarah', 'Williams', 'sarah.w@example.com', '555-789-0123', '101 Cedar Ln', 'Los Angeles', 'CA', '90001', '2022-04-05 16:20:00'),
   (5, 'Michael', 'Brown', 'michael.b@example.com', '555-234-5678', '202 Elm St', 'Denver', 'CO', '80201', '2022-05-12 11:10:00');

   -- Insert sample data into products
   INSERT INTO products VALUES
   (101, 'Laptop Pro', 'Electronics', 1299.99, 50, 'High-performance laptop with 16GB RAM'),
   (102, 'Smartphone X', 'Electronics', 899.99, 100, 'Latest smartphone with advanced camera'),
   (103, 'Coffee Maker', 'Home Appliances', 79.99, 30, 'Programmable coffee maker with timer'),
   (104, 'Running Shoes', 'Sportswear', 129.99, 75, 'Lightweight running shoes with cushioning'),
   (105, 'Wireless Headphones', 'Electronics', 149.99, 60, 'Noise-cancelling wireless headphones');

   -- Insert sample data into orders
   INSERT INTO orders VALUES
   (1001, 1, '2023-01-10 13:25:00', 1299.99, 'Delivered'),
   (1002, 2, '2023-01-15 10:30:00', 899.99, 'Shipped'),
   (1003, 3, '2023-01-20 16:45:00', 229.98, 'Processing'),
   (1004, 4, '2023-01-25 09:15:00', 129.99, 'Delivered'),
   (1005, 5, '2023-01-30 14:20:00', 149.99, 'Shipped');

   -- Insert sample data into order_items
   INSERT INTO order_items VALUES
   (10001, 1001, 101, 1, 1299.99),
   (10002, 1002, 102, 1, 899.99),
   (10003, 1003, 103, 1, 79.99),
   (10004, 1003, 104, 1, 149.99),
   (10005, 1004, 104, 1, 129.99),
   (10006, 1005, 105, 1, 149.99);
   ```

### Step 3: Create a Target S3 Bucket
1. Navigate to the Amazon S3 console
2. Create a new S3 bucket with a unique name (e.g., `your-name-dms-target-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-dms-target-YYYYMMDD
   ```
3. Create a folder structure for the migrated data:
   ```
   aws s3api put-object --bucket your-name-dms-target-YYYYMMDD --key dms-data/
   ```

### Step 4: Create IAM Roles for DMS
1. Navigate to the IAM console
2. Create a role named `dms-s3-role` with the following policies:
   - AmazonS3FullAccess (in production, use more restrictive policies)
   - AmazonDMSRedshiftS3Role
3. Create a role named `dms-vpc-role` with the following policy:
   - AmazonDMSVPCManagementRole

### Step 5: Create a DMS Replication Instance
1. Navigate to the AWS DMS console
2. Select "Replication instances" and click "Create replication instance"
3. Configure the instance:
   - Name: `dms-replication-instance`
   - Description: `DMS instance for database migration lab`
   - Instance class: `dms.t3.micro` (smallest for testing)
   - Engine version: Choose the latest available
   - VPC: Select the same VPC as your RDS instance
   - Multi-AZ: No (for lab purposes)
   - Publicly accessible: Yes (for lab purposes)
4. Create the instance and wait for it to become available

### Step 6: Create Source and Target Endpoints
1. In the DMS console, select "Endpoints" and click "Create endpoint"
2. Create the source endpoint:
   - Endpoint type: Source endpoint
   - Endpoint identifier: `mysql-source`
   - Source engine: MySQL
   - Server name: Your RDS instance endpoint
   - Port: 3306
   - SSL mode: none (for lab purposes)
   - Username: admin
   - Password: Your RDS password
   - Database name: retail
3. Test the connection to ensure it works
4. Create the target endpoint:
   - Endpoint type: Target endpoint
   - Endpoint identifier: `s3-target`
   - Target engine: Amazon S3
   - Service access role ARN: ARN of the `dms-s3-role` you created
   - Bucket name: your-name-dms-target-YYYYMMDD
   - Bucket folder: dms-data
   - File format: CSV (or choose another format)
5. Test the connection to ensure it works

### Step 7: Create and Run a Migration Task
1. In the DMS console, select "Database migration tasks" and click "Create task"
2. Configure the task:
   - Task identifier: `mysql-to-s3-migration`
   - Replication instance: Select your replication instance
   - Source database endpoint: Select your MySQL source endpoint
   - Target database endpoint: Select your S3 target endpoint
   - Migration type: Migrate existing data and replicate ongoing changes
   - CDC start mode: Enable after full load completes
3. Configure table mappings:
   - Schema: retail
   - Table: % (all tables)
4. Configure transformation rules if needed (e.g., rename schemas or tables)
5. Start the task and monitor its progress

### Step 8: Monitor the Migration
1. In the DMS console, select your migration task
2. Monitor the task status and statistics
3. Check CloudWatch metrics for detailed performance information
4. Review any task logs for errors or warnings

### Step 9: Test Change Data Capture (CDC)
1. Connect to your source MySQL database
2. Insert, update, or delete some records:
   ```sql
   -- Insert a new customer
   INSERT INTO customers VALUES
   (6, 'Emily', 'Davis', 'emily.d@example.com', '555-345-6789', '303 Maple Dr', 'Chicago', 'IL', '60601', '2023-02-15 13:40:00');

   -- Update a product
   UPDATE products SET price = 1199.99, stock_quantity = 45 WHERE product_id = 101;

   -- Delete an order
   DELETE FROM order_items WHERE order_id = 1005;
   DELETE FROM orders WHERE order_id = 1005;
   ```
2. Monitor the DMS task to see if these changes are captured
3. Check the S3 bucket for the CDC files

### Step 10: Verify the Migrated Data
1. Navigate to the S3 console and browse to your target bucket
2. Download some of the migrated files
3. Verify that the data matches what's in the source database
4. Check that CDC changes were properly captured

## Validation Steps
1. Verify that the full load migration completed successfully
2. Confirm that all tables and data were migrated to S3
3. Check that CDC changes were captured and written to S3
4. Review the task statistics and logs for any issues
5. Verify the data format and structure in the S3 files

## Cleanup Instructions
1. Stop and delete the DMS migration task
   ```
   aws dms stop-replication-task --replication-task-arn <task-arn>
   aws dms delete-replication-task --replication-task-arn <task-arn>
   ```
2. Delete the DMS endpoints
   ```
   aws dms delete-endpoint --endpoint-arn <source-endpoint-arn>
   aws dms delete-endpoint --endpoint-arn <target-endpoint-arn>
   ```
3. Delete the DMS replication instance
   ```
   aws dms delete-replication-instance --replication-instance-arn <instance-arn>
   ```
4. Delete the RDS database
   ```
   aws rds delete-db-instance --db-instance-identifier source-mysql-db --skip-final-snapshot
   ```
5. Delete the S3 bucket and its contents
   ```
   aws s3 rb s3://your-name-dms-target-YYYYMMDD --force
   ```
6. Delete the IAM roles
   ```
   aws iam delete-role --role-name dms-s3-role
   aws iam delete-role --role-name dms-vpc-role
   ```

## Challenge Extensions (Optional)
1. Implement table filtering to migrate only specific tables
2. Add column transformations (e.g., masking sensitive data)
3. Set up a DMS task to migrate to Amazon Redshift instead of S3
4. Configure data validation to compare source and target data
5. Implement a more complex CDC scenario with multiple updates

## Additional Resources
- [AWS DMS Documentation](https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html)
- [DMS Best Practices](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- [Working with CDC in DMS](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html)
- [Troubleshooting DMS Tasks](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Troubleshooting.html)

## Notes and Tips
- Binary logging must be enabled on the source MySQL database for CDC to work
- For large migrations, consider using a larger DMS instance type
- Monitor task statistics to identify performance bottlenecks
- Use task logs to troubleshoot any migration issues
- In production environments, use more restrictive IAM policies
- Consider using AWS SCT for complex schema conversions
