# Lab 4.1: Data Governance with AWS Lake Formation

## Overview
This lab focuses on implementing data governance using AWS Lake Formation. You will learn how to set up a data lake with fine-grained access controls, manage permissions at different levels, and implement column-level security, which are essential skills for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Set up AWS Lake Formation for data lake governance
- Register data locations with Lake Formation
- Create and manage data lake permissions
- Implement column-level security
- Configure row-level filtering
- Set up cross-account access
- Monitor data access patterns

**AWS Services Used:**
- AWS Lake Formation
- AWS Glue
- Amazon S3
- Amazon Athena
- AWS Identity and Access Management (IAM)
- AWS CloudTrail

**Estimated Time:** 3 hours

**Estimated Cost:** $5-10 (Most resources fall under Free Tier if available)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for Lake Formation, Glue, S3, and Athena
- Basic understanding of data governance concepts
- Familiarity with IAM roles and policies

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│  S3 Data    │────▶│  AWS Lake   │────▶│  AWS Glue   │
│  Lake       │     │  Formation  │     │  Catalog    │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                          │                    │
                          │                    │
                          ▼                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │
│  IAM Users  │◀───▶│  Permission │◀───▶│  Amazon     │
│  and Roles  │     │  Management │     │  Athena     │
│             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Implementation Steps

### Step 1: Create S3 Bucket for Data Lake
1. Sign in to the AWS Management Console and navigate to the S3 service
2. Create a new S3 bucket with a unique name (e.g., `your-name-lakeformation-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-lakeformation-YYYYMMDD
   ```
3. Create the following folder structure:
   ```
   aws s3api put-object --bucket your-name-lakeformation-YYYYMMDD --key raw/
   aws s3api put-object --bucket your-name-lakeformation-YYYYMMDD --key curated/
   ```

### Step 2: Prepare Sample Data with Sensitive Information
1. Create a sample CSV file for employee data (`employees.csv`) with some sensitive columns:
```
employee_id,first_name,last_name,email,phone_number,hire_date,job_title,department,salary,ssn
101,John,Doe,john.doe@example.com,555-123-4567,2022-01-15,Software Engineer,Engineering,120000,123-45-6789
102,Jane,Smith,jane.smith@example.com,555-987-6543,2022-02-20,Data Scientist,Data Science,130000,234-56-7890
103,Robert,Johnson,robert.j@example.com,555-456-7890,2022-03-10,Product Manager,Product,140000,345-67-8901
104,Sarah,Williams,sarah.w@example.com,555-789-0123,2022-04-05,UX Designer,Design,110000,456-78-9012
105,Michael,Brown,michael.b@example.com,555-234-5678,2022-05-12,DevOps Engineer,Engineering,125000,567-89-0123
106,Emily,Davis,emily.d@example.com,555-345-6789,2022-06-18,Marketing Specialist,Marketing,95000,678-90-1234
107,David,Miller,david.m@example.com,555-456-7890,2022-07-22,Sales Representative,Sales,105000,789-01-2345
108,Lisa,Wilson,lisa.w@example.com,555-567-8901,2022-08-30,HR Manager,Human Resources,115000,890-12-3456
109,James,Taylor,james.t@example.com,555-678-9012,2022-09-14,Financial Analyst,Finance,118000,901-23-4567
110,Jennifer,Anderson,jennifer.a@example.com,555-789-0123,2022-10-05,IT Support,IT,90000,012-34-5678
```

2. Create a sample CSV file for financial data (`financial_transactions.csv`):
```
transaction_id,employee_id,transaction_date,transaction_type,amount,account_number,description
1001,101,2023-01-10,Expense,1299.99,ACCT-12345,Hardware purchase
1002,102,2023-01-15,Expense,899.99,ACCT-23456,Conference registration
1003,103,2023-01-20,Reimbursement,159.98,ACCT-34567,Travel expenses
1004,104,2023-01-25,Expense,129.99,ACCT-45678,Software subscription
1005,105,2023-01-30,Advance,1500.00,ACCT-56789,Travel advance
1006,106,2023-02-05,Expense,89.99,ACCT-67890,Office supplies
1007,107,2023-02-10,Reimbursement,129.99,ACCT-78901,Client meeting
1008,108,2023-02-15,Expense,499.99,ACCT-89012,Training course
1009,109,2023-02-20,Expense,79.98,ACCT-90123,Books and publications
1010,110,2023-02-25,Reimbursement,249.99,ACCT-01234,Equipment repair
```

3. Upload these files to your S3 bucket:
   ```
   aws s3 cp employees.csv s3://your-name-lakeformation-YYYYMMDD/raw/hr/
   aws s3 cp financial_transactions.csv s3://your-name-lakeformation-YYYYMMDD/raw/finance/
   ```

### Step 3: Set Up Lake Formation
1. Navigate to the AWS Lake Formation console
2. Complete the initial setup if this is your first time using Lake Formation
3. For "Administrators", add your current IAM user or role
4. For "Database creators", add your current IAM user or role
5. Uncheck "Use only IAM access control for new databases" to enable Lake Formation permissions

### Step 4: Register Data Lake Location
1. In the Lake Formation console, go to "Register and ingest" > "Data lake locations"
2. Click "Register location"
3. Select your S3 bucket: `s3://your-name-lakeformation-YYYYMMDD`
4. For IAM role, create or select a role with appropriate S3 permissions
5. Register the location

### Step 5: Create a Database in the Glue Data Catalog
1. In the Lake Formation console, go to "Data catalog" > "Databases"
2. Click "Create database"
3. Name the database `company_data`
4. Leave other settings as default
5. Create the database

### Step 6: Create Crawlers to Catalog the Data
1. Navigate to the AWS Glue console
2. Go to "Crawlers" and click "Create crawler"
3. Name the crawler `hr_data_crawler`
4. For data source, choose S3 and specify your bucket path: `s3://your-name-lakeformation-YYYYMMDD/raw/hr/`
5. Create or select an IAM role with appropriate permissions
6. For output, select the `company_data` database
7. Set the crawler schedule to run on demand
8. Create the crawler and run it
9. Create another crawler named `finance_data_crawler` for the finance data path
10. Run both crawlers and wait for them to complete

### Step 7: Create IAM Users and Groups for Testing
1. Navigate to the IAM console
2. Create the following users:
   - `hr-analyst`
   - `finance-analyst`
   - `data-engineer`
   - `executive`
3. Create the following groups and add users:
   - `hr-group`: Add `hr-analyst`
   - `finance-group`: Add `finance-analyst`
   - `data-engineering-group`: Add `data-engineer`
   - `executive-group`: Add `executive`
4. Create passwords for each user for console access

### Step 8: Configure Lake Formation Permissions
1. Navigate back to the Lake Formation console
2. Go to "Permissions" > "Data lake permissions"
3. Click "Grant" to set up the following permissions:

   a. For HR Analyst:
   - Principal: `hr-analyst` user
   - LF-Tags or catalog resources: Choose "Named data catalog resources"
   - Database: `company_data`
   - Tables: `employees`
   - Table permissions: Select, Describe
   - Column-level permissions: All columns EXCEPT `ssn` and `salary`

   b. For Finance Analyst:
   - Principal: `finance-analyst` user
   - LF-Tags or catalog resources: Choose "Named data catalog resources"
   - Database: `company_data`
   - Tables: `financial_transactions`, `employees`
   - Table permissions: Select, Describe
   - For `employees`, restrict columns to `employee_id`, `first_name`, `last_name`, `department`
   - For `financial_transactions`, grant access to all columns

   c. For Data Engineer:
   - Principal: `data-engineer` user
   - LF-Tags or catalog resources: Choose "Named data catalog resources"
   - Database: `company_data`
   - Tables: All tables
   - Table permissions: All permissions
   - Column-level permissions: All columns

   d. For Executive:
   - Principal: `executive` user
   - LF-Tags or catalog resources: Choose "Named data catalog resources"
   - Database: `company_data`
   - Tables: All tables
   - Table permissions: Select, Describe
   - Column-level permissions: All columns EXCEPT `ssn` in `employees` and `account_number` in `financial_transactions`

### Step 9: Implement Row-Level Filtering (Optional)
1. In the Lake Formation console, go to "Permissions" > "Data filters"
2. Click "Create filter"
3. Name the filter `hr_department_filter`
4. Select the `company_data` database and `employees` table
5. Add a row filter expression: `department = 'Engineering' OR department = 'Data Science'`
6. Create the filter
7. Grant permissions using this filter to the `hr-analyst` user

### Step 10: Test Access with Different Users
1. Sign out of your current AWS account
2. Sign in as each user you created and test access through Athena:

   a. As `hr-analyst`:
   ```sql
   SELECT * FROM company_data.employees;  -- Should see all columns except ssn and salary
   SELECT ssn FROM company_data.employees;  -- Should fail
   SELECT * FROM company_data.financial_transactions;  -- Should fail
   ```

   b. As `finance-analyst`:
   ```sql
   SELECT * FROM company_data.financial_transactions;  -- Should succeed
   SELECT employee_id, first_name, last_name, department FROM company_data.employees;  -- Should succeed
   SELECT salary FROM company_data.employees;  -- Should fail
   ```

   c. As `data-engineer`:
   ```sql
   SELECT * FROM company_data.employees;  -- Should see all columns
   SELECT * FROM company_data.financial_transactions;  -- Should see all columns
   ```

   d. As `executive`:
   ```sql
   SELECT * FROM company_data.employees;  -- Should see all columns except ssn
   SELECT * FROM company_data.financial_transactions;  -- Should see all columns except account_number
   ```

### Step 11: Set Up LF-Tags for Attribute-Based Access Control (Optional)
1. In the Lake Formation console, go to "Permissions" > "LF-Tags"
2. Click "Add LF-Tag"
3. Create the following LF-Tags:
   - Key: `Sensitivity`, Values: `Public`, `Confidential`, `Restricted`
   - Key: `Department`, Values: `HR`, `Finance`, `All`
4. Assign LF-Tags to tables and columns:
   - `employees` table: `Department=HR`, `Sensitivity=Confidential`
   - `ssn` column in `employees`: `Sensitivity=Restricted`
   - `financial_transactions` table: `Department=Finance`, `Sensitivity=Confidential`
   - `account_number` column in `financial_transactions`: `Sensitivity=Restricted`
5. Grant LF-Tag permissions to users and groups:
   - `hr-analyst`: `Department=HR`, `Sensitivity=Confidential`
   - `finance-analyst`: `Department=Finance`, `Sensitivity=Confidential`
   - `data-engineer`: `Department=All`, `Sensitivity=Confidential`
   - `executive`: `Department=All`, `Sensitivity=Confidential`

### Step 12: Monitor Data Access with CloudTrail
1. Navigate to the CloudTrail console
2. Create a trail if you don't have one already
3. Configure the trail to log data events for your S3 bucket
4. Review CloudTrail logs to see access patterns and permission checks

## Validation Steps
1. Verify that Lake Formation permissions are correctly applied
2. Confirm that column-level security restricts access to sensitive columns
3. Check that row-level filtering works as expected (if implemented)
4. Verify that LF-Tags control access based on attributes (if implemented)
5. Review CloudTrail logs to ensure access controls are working

## Cleanup Instructions
1. Delete the Lake Formation permissions
   ```
   # Use Lake Formation console to revoke permissions
   ```
2. Deregister the data lake location
   ```
   # Use Lake Formation console to deregister location
   ```
3. Delete the Glue crawlers
   ```
   aws glue delete-crawler --name hr_data_crawler
   aws glue delete-crawler --name finance_data_crawler
   ```
4. Delete the Glue database and tables
   ```
   aws glue delete-database --name company_data
   ```
5. Delete the IAM users and groups
   ```
   # Use IAM console to delete users and groups
   ```
6. Delete the S3 bucket and its contents
   ```
   aws s3 rb s3://your-name-lakeformation-YYYYMMDD --force
   ```

## Challenge Extensions (Optional)
1. Implement cross-account access to your data lake
2. Set up Lake Formation tag-based access control with more complex policies
3. Create a workflow to automatically update permissions when new data arrives
4. Implement data masking for sensitive columns instead of completely restricting access
5. Set up Lake Formation permissions for federated users through AWS SSO

## Additional Resources
- [AWS Lake Formation Documentation](https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html)
- [Lake Formation Permissions Reference](https://docs.aws.amazon.com/lake-formation/latest/dg/lf-permissions-reference.html)
- [Column-Level Security in Lake Formation](https://docs.aws.amazon.com/lake-formation/latest/dg/column-level-security.html)
- [Row-Level Security in Lake Formation](https://docs.aws.amazon.com/lake-formation/latest/dg/row-level-security.html)

## Notes and Tips
- Lake Formation permissions are additive to IAM permissions - users need both
- When troubleshooting access issues, check both Lake Formation and IAM permissions
- Use LF-Tags for scalable permission management across many tables
- Consider using resource links for sharing tables across accounts
- Remember that Lake Formation permissions apply to metadata operations and data access
- Use CloudTrail to audit permission changes and access patterns
