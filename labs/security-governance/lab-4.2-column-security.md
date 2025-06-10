# Lab 4.2: Column-Level Security

## Overview
This lab focuses on implementing column-level security in AWS data services. You will learn how to restrict access to sensitive columns in your data using AWS Lake Formation, Amazon Redshift, and AWS Glue, which are essential skills for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Implement column-level security in AWS Lake Formation
- Configure column-level permissions in Amazon Redshift
- Use AWS Glue to enforce column-level access controls
- Apply data masking techniques for sensitive columns
- Implement dynamic data masking
- Test and validate column-level security controls
- Monitor column-level access patterns

**AWS Services Used:**
- AWS Lake Formation
- Amazon Redshift
- AWS Glue
- Amazon S3
- AWS Identity and Access Management (IAM)
- Amazon Athena
- AWS CloudTrail

**Estimated Time:** 3 hours

**Estimated Cost:** $5-10 (Redshift charges apply)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for Lake Formation, Redshift, Glue, and S3
- Basic understanding of data security concepts
- Familiarity with SQL and data access patterns

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
│  Amazon     │◀───▶│  Column     │◀───▶│  Amazon     │
│  Redshift   │     │  Security   │     │  Athena     │
│             │     │  Controls   │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          │
                          ▼
                    ┌─────────────┐
                    │             │
                    │  IAM Users  │
                    │  and Roles  │
                    │             │
                    └─────────────┘
```

## Implementation Steps

### Step 1: Create S3 Bucket for Data Lake
1. Sign in to the AWS Management Console and navigate to the S3 service
2. Create a new S3 bucket with a unique name (e.g., `your-name-column-security-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-column-security-YYYYMMDD
   ```
3. Create the following folder structure:
   ```
   aws s3api put-object --bucket your-name-column-security-YYYYMMDD --key data/
   ```

### Step 2: Prepare Sample Data with Sensitive Columns
1. Create a sample CSV file for employee data (`employees.csv`) with sensitive columns:
```
employee_id,first_name,last_name,email,phone_number,hire_date,job_title,department,salary,ssn,address,birth_date
101,John,Doe,john.doe@example.com,555-123-4567,2022-01-15,Software Engineer,Engineering,120000,123-45-6789,123 Main St Seattle WA 98101,1985-06-15
102,Jane,Smith,jane.smith@example.com,555-987-6543,2022-02-20,Data Scientist,Data Science,130000,234-56-7890,456 Oak Ave Portland OR 97205,1990-03-22
103,Robert,Johnson,robert.j@example.com,555-456-7890,2022-03-10,Product Manager,Product,140000,345-67-8901,789 Pine Rd San Francisco CA 94105,1982-11-08
104,Sarah,Williams,sarah.w@example.com,555-789-0123,2022-04-05,UX Designer,Design,110000,456-78-9012,101 Cedar Ln Los Angeles CA 90001,1988-09-17
105,Michael,Brown,michael.b@example.com,555-234-5678,2022-05-12,DevOps Engineer,Engineering,125000,567-89-0123,202 Elm St Denver CO 80201,1979-04-30
106,Emily,Davis,emily.d@example.com,555-345-6789,2022-06-18,Marketing Specialist,Marketing,95000,678-90-1234,303 Maple Dr Chicago IL 60601,1992-07-25
107,David,Miller,david.m@example.com,555-456-7890,2022-07-22,Sales Representative,Sales,105000,789-01-2345,404 Birch Blvd Boston MA 02108,1984-12-03
108,Lisa,Wilson,lisa.w@example.com,555-567-8901,2022-08-30,HR Manager,Human Resources,115000,890-12-3456,505 Walnut St Miami FL 33101,1981-02-19
109,James,Taylor,james.t@example.com,555-678-9012,2022-09-14,Financial Analyst,Finance,118000,901-23-4567,606 Cherry Ave Austin TX 78701,1987-10-11
110,Jennifer,Anderson,jennifer.a@example.com,555-789-0123,2022-10-05,IT Support,IT,90000,012-34-5678,707 Spruce Ct Phoenix AZ 85001,1993-05-28
```

2. Create a sample CSV file for financial data (`financial_transactions.csv`):
```
transaction_id,employee_id,transaction_date,transaction_type,amount,account_number,description,approval_status,approver_id,cost_center,project_code
1001,101,2023-01-10,Expense,1299.99,ACCT-12345,Hardware purchase,Approved,201,CC-001,PROJ-A
1002,102,2023-01-15,Expense,899.99,ACCT-23456,Conference registration,Approved,202,CC-002,PROJ-B
1003,103,2023-01-20,Reimbursement,159.98,ACCT-34567,Travel expenses,Approved,201,CC-003,PROJ-C
1004,104,2023-01-25,Expense,129.99,ACCT-45678,Software subscription,Pending,203,CC-001,PROJ-D
1005,105,2023-01-30,Advance,1500.00,ACCT-56789,Travel advance,Approved,202,CC-002,PROJ-A
1006,106,2023-02-05,Expense,89.99,ACCT-67890,Office supplies,Approved,203,CC-003,PROJ-B
1007,107,2023-02-10,Reimbursement,129.99,ACCT-78901,Client meeting,Rejected,201,CC-001,PROJ-C
1008,108,2023-02-15,Expense,499.99,ACCT-89012,Training course,Approved,202,CC-002,PROJ-D
1009,109,2023-02-20,Expense,79.98,ACCT-90123,Books and publications,Approved,203,CC-003,PROJ-A
1010,110,2023-02-25,Reimbursement,249.99,ACCT-01234,Equipment repair,Pending,201,CC-001,PROJ-B
```

3. Upload these files to your S3 bucket:
   ```
   aws s3 cp employees.csv s3://your-name-column-security-YYYYMMDD/data/hr/
   aws s3 cp financial_transactions.csv s3://your-name-column-security-YYYYMMDD/data/finance/
   ```

### Step 3: Set Up AWS Lake Formation
1. Navigate to the AWS Lake Formation console
2. Complete the initial setup if this is your first time using Lake Formation
3. For "Administrators", add your current IAM user or role
4. For "Database creators", add your current IAM user or role
5. Uncheck "Use only IAM access control for new databases" to enable Lake Formation permissions

### Step 4: Register Data Lake Location
1. In the Lake Formation console, go to "Register and ingest" > "Data lake locations"
2. Click "Register location"
3. Select your S3 bucket: `s3://your-name-column-security-YYYYMMDD`
4. For IAM role, create or select a role with appropriate S3 permissions
5. Register the location

### Step 5: Create a Database in the Glue Data Catalog
1. In the Lake Formation console, go to "Data catalog" > "Databases"
2. Click "Create database"
3. Name the database `sensitive_data`
4. Leave other settings as default
5. Create the database

### Step 6: Create Crawlers to Catalog the Data
1. Navigate to the AWS Glue console
2. Go to "Crawlers" and click "Create crawler"
3. Name the crawler `hr_data_crawler`
4. For data source, choose S3 and specify your bucket path: `s3://your-name-column-security-YYYYMMDD/data/hr/`
5. Create or select an IAM role with appropriate permissions
6. For output, select the `sensitive_data` database
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

### Step 8: Configure Column-Level Security in Lake Formation
1. Navigate back to the Lake Formation console
2. Go to "Permissions" > "Data lake permissions"
3. Click "Grant" to set up the following column-level permissions:

   a. For HR Analyst:
   - Principal: `hr-analyst` user
   - LF-Tags or catalog resources: Choose "Named data catalog resources"
   - Database: `sensitive_data`
   - Tables: `employees`
   - Table permissions: Select, Describe
   - Column-level permissions: Include columns
   - Columns: Select all EXCEPT `ssn`, `salary`, `birth_date`, `address`

   b. For Finance Analyst:
   - Principal: `finance-analyst` user
   - LF-Tags or catalog resources: Choose "Named data catalog resources"
   - Database: `sensitive_data`
   - Tables: `financial_transactions`, `employees`
   - Table permissions: Select, Describe
   - For `employees`, include only columns: `employee_id`, `first_name`, `last_name`, `department`, `job_title`
   - For `financial_transactions`, exclude columns: `account_number`

   c. For Data Engineer:
   - Principal: `data-engineer` user
   - LF-Tags or catalog resources: Choose "Named data catalog resources"
   - Database: `sensitive_data`
   - Tables: All tables
   - Table permissions: All permissions
   - Column-level permissions: Include all columns

   d. For Executive:
   - Principal: `executive` user
   - LF-Tags or catalog resources: Choose "Named data catalog resources"
   - Database: `sensitive_data`
   - Tables: All tables
   - Table permissions: Select, Describe
   - Column-level permissions: Exclude columns
   - Columns: `ssn` in `employees` and `account_number` in `financial_transactions`

### Step 9: Set Up Amazon Redshift for Column-Level Security
1. Navigate to the Amazon Redshift console
2. Click "Create cluster"
3. Configure the cluster:
   - Cluster identifier: `column-security-cluster`
   - Node type: dc2.large (for lab purposes)
   - Number of nodes: 2
   - Database name: `sensitive_data`
   - Admin username: `admin`
   - Admin password: Create and save a secure password
4. For network and security:
   - Choose a VPC and subnet
   - Enable "Publicly accessible" (for lab purposes)
   - Create a new security group or use an existing one
5. Create the cluster and wait for it to become available

### Step 10: Load Data into Redshift
1. Use a SQL client (like the Redshift Query Editor in the console) to connect to your cluster
2. Create tables for the employee and financial data:

```sql
-- Create schema
CREATE SCHEMA sensitive_data;
SET search_path TO sensitive_data;

-- Create employees table
CREATE TABLE employees (
    employee_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(20),
    hire_date DATE,
    job_title VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    ssn VARCHAR(11),
    address VARCHAR(200),
    birth_date DATE
);

-- Create financial_transactions table
CREATE TABLE financial_transactions (
    transaction_id INT,
    employee_id INT,
    transaction_date DATE,
    transaction_type VARCHAR(50),
    amount DECIMAL(10,2),
    account_number VARCHAR(20),
    description VARCHAR(200),
    approval_status VARCHAR(20),
    approver_id INT,
    cost_center VARCHAR(20),
    project_code VARCHAR(20)
);
```

3. Load data from S3 into Redshift:

```sql
-- Load employees data
COPY sensitive_data.employees
FROM 's3://your-name-column-security-YYYYMMDD/data/hr/employees.csv'
IAM_ROLE 'arn:aws:iam::<your-account-id>:role/RedshiftLoadRole'
CSV IGNOREHEADER 1;

-- Load financial_transactions data
COPY sensitive_data.financial_transactions
FROM 's3://your-name-column-security-YYYYMMDD/data/finance/financial_transactions.csv'
IAM_ROLE 'arn:aws:iam::<your-account-id>:role/RedshiftLoadRole'
CSV IGNOREHEADER 1;
```

### Step 11: Configure Column-Level Security in Redshift
1. Create Redshift users and roles:

```sql
-- Create users
CREATE USER hr_analyst PASSWORD 'YourSecurePassword1';
CREATE USER finance_analyst PASSWORD 'YourSecurePassword2';
CREATE USER data_engineer PASSWORD 'YourSecurePassword3';
CREATE USER executive PASSWORD 'YourSecurePassword4';

-- Create roles
CREATE ROLE hr_role;
CREATE ROLE finance_role;
CREATE ROLE data_engineer_role;
CREATE ROLE executive_role;

-- Grant roles to users
GRANT hr_role TO hr_analyst;
GRANT finance_role TO finance_analyst;
GRANT data_engineer_role TO data_engineer;
GRANT executive_role TO executive;
```

2. Create views with column-level restrictions:

```sql
-- HR view with restricted columns
CREATE VIEW sensitive_data.hr_employees_view AS
SELECT 
    employee_id,
    first_name,
    last_name,
    email,
    phone_number,
    hire_date,
    job_title,
    department
FROM 
    sensitive_data.employees;

-- Finance view with restricted columns
CREATE VIEW sensitive_data.finance_employees_view AS
SELECT 
    employee_id,
    first_name,
    last_name,
    department,
    job_title
FROM 
    sensitive_data.employees;

CREATE VIEW sensitive_data.finance_transactions_view AS
SELECT 
    transaction_id,
    employee_id,
    transaction_date,
    transaction_type,
    amount,
    description,
    approval_status,
    approver_id,
    cost_center,
    project_code
FROM 
    sensitive_data.financial_transactions;

-- Executive view with restricted columns
CREATE VIEW sensitive_data.executive_employees_view AS
SELECT 
    employee_id,
    first_name,
    last_name,
    email,
    phone_number,
    hire_date,
    job_title,
    department,
    salary,
    address,
    birth_date
FROM 
    sensitive_data.employees;

CREATE VIEW sensitive_data.executive_transactions_view AS
SELECT 
    transaction_id,
    employee_id,
    transaction_date,
    transaction_type,
    amount,
    description,
    approval_status,
    approver_id,
    cost_center,
    project_code
FROM 
    sensitive_data.financial_transactions;
```

3. Grant permissions to roles:

```sql
-- Grant permissions to HR role
GRANT SELECT ON sensitive_data.hr_employees_view TO hr_role;

-- Grant permissions to Finance role
GRANT SELECT ON sensitive_data.finance_employees_view TO finance_role;
GRANT SELECT ON sensitive_data.finance_transactions_view TO finance_role;

-- Grant permissions to Data Engineer role
GRANT SELECT ON sensitive_data.employees TO data_engineer_role;
GRANT SELECT ON sensitive_data.financial_transactions TO data_engineer_role;

-- Grant permissions to Executive role
GRANT SELECT ON sensitive_data.executive_employees_view TO executive_role;
GRANT SELECT ON sensitive_data.executive_transactions_view TO executive_role;
```

### Step 12: Implement Dynamic Data Masking in Redshift
1. Create masking policies for sensitive columns:

```sql
-- Create dynamic masking policy for SSN
CREATE MASKING POLICY ssn_mask
WITH (ssn VARCHAR(11))
USING (
    CASE
        WHEN CURRENT_USER IN ('admin', 'data_engineer') THEN ssn
        ELSE 'XXX-XX-' || SUBSTRING(ssn, 8, 4)
    END
);

-- Create dynamic masking policy for salary
CREATE MASKING POLICY salary_mask
WITH (salary DECIMAL(10,2))
USING (
    CASE
        WHEN CURRENT_USER IN ('admin', 'data_engineer', 'executive') THEN salary
        ELSE NULL
    END
);

-- Create dynamic masking policy for account numbers
CREATE MASKING POLICY account_mask
WITH (account_number VARCHAR(20))
USING (
    CASE
        WHEN CURRENT_USER IN ('admin', 'data_engineer') THEN account_number
        ELSE 'XXXX-' || SUBSTRING(account_number, 6, 5)
    END
);
```

2. Attach masking policies to columns:

```sql
-- Attach masking policies to employees table
ATTACH MASKING POLICY ssn_mask ON sensitive_data.employees(ssn);
ATTACH MASKING POLICY salary_mask ON sensitive_data.employees(salary);

-- Attach masking policy to financial_transactions table
ATTACH MASKING POLICY account_mask ON sensitive_data.financial_transactions(account_number);
```

### Step 13: Test Column-Level Security in Athena
1. Navigate to the Amazon Athena console
2. Set up a query result location if not already configured
3. Sign in as each user you created and test access through Athena:

   a. As `hr-analyst`:
   ```sql
   SELECT * FROM sensitive_data.employees;  -- Should see all columns except ssn, salary, birth_date, address
   SELECT ssn FROM sensitive_data.employees;  -- Should fail
   SELECT * FROM sensitive_data.financial_transactions;  -- Should fail
   ```

   b. As `finance-analyst`:
   ```sql
   SELECT * FROM sensitive_data.financial_transactions;  -- Should see all columns except account_number
   SELECT employee_id, first_name, last_name, department, job_title FROM sensitive_data.employees;  -- Should succeed
   SELECT salary FROM sensitive_data.employees;  -- Should fail
   ```

   c. As `data-engineer`:
   ```sql
   SELECT * FROM sensitive_data.employees;  -- Should see all columns
   SELECT * FROM sensitive_data.financial_transactions;  -- Should see all columns
   ```

   d. As `executive`:
   ```sql
   SELECT * FROM sensitive_data.employees;  -- Should see all columns except ssn
   SELECT * FROM sensitive_data.financial_transactions;  -- Should see all columns except account_number
   ```

### Step 14: Test Column-Level Security in Redshift
1. Connect to Redshift as each user and run queries:

   a. As `hr_analyst`:
   ```sql
   SELECT * FROM sensitive_data.hr_employees_view;  -- Should succeed
   SELECT * FROM sensitive_data.employees;  -- Should fail
   SELECT * FROM sensitive_data.financial_transactions;  -- Should fail
   ```

   b. As `finance_analyst`:
   ```sql
   SELECT * FROM sensitive_data.finance_employees_view;  -- Should succeed
   SELECT * FROM sensitive_data.finance_transactions_view;  -- Should succeed
   SELECT * FROM sensitive_data.employees;  -- Should fail
   ```

   c. As `data_engineer`:
   ```sql
   SELECT * FROM sensitive_data.employees;  -- Should see all columns with actual values
   SELECT * FROM sensitive_data.financial_transactions;  -- Should see all columns with actual values
   ```

   d. As `executive`:
   ```sql
   SELECT * FROM sensitive_data.executive_employees_view;  -- Should see all columns except ssn (masked)
   SELECT * FROM sensitive_data.executive_transactions_view;  -- Should see all columns except account_number (masked)
   ```

### Step 15: Monitor Column-Level Access
1. Navigate to the CloudTrail console
2. Create a trail if you don't have one already
3. Configure the trail to log data events for your S3 bucket and Glue Data Catalog
4. Review CloudTrail logs to see access patterns and permission checks

## Validation Steps
1. Verify that Lake Formation column-level permissions are correctly applied
2. Confirm that Redshift views restrict access to sensitive columns
3. Check that dynamic data masking works as expected
4. Verify that different users can access only their authorized columns
5. Review CloudTrail logs to ensure access controls are working

## Cleanup Instructions
1. Delete the Redshift cluster
   ```
   aws redshift delete-cluster --cluster-identifier column-security-cluster --skip-final-cluster-snapshot
   ```
2. Delete the Lake Formation permissions
   ```
   # Use Lake Formation console to revoke permissions
   ```
3. Deregister the data lake location
   ```
   # Use Lake Formation console to deregister location
   ```
4. Delete the Glue crawlers
   ```
   aws glue delete-crawler --name hr_data_crawler
   aws glue delete-crawler --name finance_data_crawler
   ```
5. Delete the Glue database and tables
   ```
   aws glue delete-database --name sensitive_data
   ```
6. Delete the IAM users and groups
   ```
   # Use IAM console to delete users and groups
   ```
7. Delete the S3 bucket and its contents
   ```
   aws s3 rb s3://your-name-column-security-YYYYMMDD --force
   ```

## Challenge Extensions (Optional)
1. Implement cell-level security using AWS Lake Formation row expressions
2. Create more complex masking policies based on user attributes
3. Implement column-level encryption for highly sensitive data
4. Set up cross-account column-level security
5. Create a custom audit solution for column-level access
6. Implement column-level security in Amazon RDS using PostgreSQL column privileges

## Additional Resources
- [AWS Lake Formation Column-Level Security](https://docs.aws.amazon.com/lake-formation/latest/dg/column-level-security.html)
- [Amazon Redshift Dynamic Data Masking](https://docs.aws.amazon.com/redshift/latest/dg/t_ddm.html)
- [Redshift Column-Level Access Control](https://docs.aws.amazon.com/redshift/latest/dg/r_GRANT.html)
- [AWS Glue Data Catalog Security](https://docs.aws.amazon.com/glue/latest/dg/security-data-catalog.html)

## Notes and Tips
- Column-level security should be part of a defense-in-depth strategy
- Consider using both Lake Formation and service-specific controls for comprehensive protection
- Dynamic data masking is preferable to complete restriction when users need to know that data exists
- Monitor access patterns to detect potential security issues
- Regularly review and update column-level permissions as data sensitivity changes
- Document your column security policies and share them with stakeholders
