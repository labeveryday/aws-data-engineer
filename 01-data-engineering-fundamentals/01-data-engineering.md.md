# Section 2: Data Engineering Fundamentals

This section covers the basics of data engineering.

## 5-Types of Data (Structured, Unstructured, Semi-Structured)

**There are 3 types of Data:**
- Structured 
- Unstructured 
- Semi-structured

**Structured Data** 
- Data that is organized in a defined manner or schema, typically found in relational databases. 
- Characteristics:
	- Easily queryable
	- Organized in rows and columns
	- Has a consistent structure
- Examples: 
	- Database tables
	- CSV files with consistent columns
	- Excel spreadsheets

**Unstructured Data:**
- Data that doesn't have a predefined structure or schema.
- Characteristics:
	- Not easily queryable without preprocessing 
	- May come in various formats
- Examples: 
	- Text files without a fixed format
	- Videos and audio files
	- Images
	- Emails and word processing documents

**Semi-Structured Data:**
- Data that is not as organized as structured data but has some level of structure in the form of tags, hierarchies, or other patterns.
- Characteristics:
	- Elements might be tagged or categorized in some way
	- More flexible than structured data but not as chaotic as unstructured data
- Examples:
	- XML and JSON files
	- Email headers (which have a mixed of structured fields like date, subject, etc. and unstructured data in the body)
	- Log files with varied formats.
## 6-Properties of Data (Volume / Velocity / Variety)

**The 3 Properties of Data:**
- Volume 
- Velocity
- Variety

**Volume:**
- Refers to the amount or size of data that organizations are dealing with at any given time. 
- Characteristics:
	- May range from gigabytes or petabytes or even more
	- Challenges in storing, processing, and analyzing high volumes of data
- Examples:
	- A popular social media platform processing terabytes of data daily from user posts, images, and videos
	- Retailers collecting years' worth of transaction data, amounting to several petabytes.

**Velocity:**
- Refers to the speed at which new data is generated, collected, and processed.
- Characteristics:
	- High velocity requires real-time or near-real-time processing capabilities
	- Rapid ingestion and processing can be critical for certain applications
- Examples:
	- Sensor data from IoT devices streaming readings every millisecond
	- High-frequency trading systems where milliseconds can make a difference in decision-making. 

**Variety:**
- Refers to the different types, structures, and sources of data.
- Characteristics:
	- Data can be structured, semi-structured, or unstructured
	- Data can come from multiple sources and in various formats. 
- Examples:
	- A business analyzing data from relational databases (structured), emails (unstructured), and JSON logs (semi-structured)
	- Healthcare systems collecting data from electronic medical records, wearable health devices, and patient feedback forms.

## 7-Data Warehouses vs. Data Lakes (and Lakehouses)

**Data Warehouse (Legacy approach)**
- A centralized repository optimized for analysis where data from different sources is stored in a *structured format*.
- Characteristics:
	- Designed for complex queries and analysis
	- Data is cleaned, transformed, and loaded (ETL process)
	- Typically uses a star or snowflake schema
	- Optimized for read-heavy operations.
- Examples:
	- Amazon Redshift
	- Google BigQuery
	- Microsoft Azure SQL Data Warehouse

>ETL: (Extract, Transform, and Load)


![](Screenshot%202024-05-20%20at%201.09.39%20PM.png)

**Data Lake:**
- A storage repository that holds vasts amounts of raw data in its native format, including structured, semi-structured, and unstructured data.
- Characteristics:
	- Can store large volumes of raw data without predefined schema
	- Data is loaded as-is, no need for preprocessing
	- Supports batch, real-time, and stream processing
	- Can be queried for data transformation or exploration puposes
- Examples:
	- Amazon Simple Storage Service (S3) when used a data lake
	- Azure Data Lake Storage
	- Hadoop Distributed File System (HDFS)

S3 (raw data) --> AWS Glue (Extract structure and schema)--> Amazon Athena (query the data)

**Comparing the TWO:**
- Schema:
	- Data Warehouse: 
		- Schema-on-write (predefined schema before writing data)
		- Extract - Transform - Load (ELT)
	- Data Lake:
		- Schema-on-read (Schema is defined at the time of reading data)
		- Extract - Load - Transform (ETL)
- Data Types:
	- Data Warehouse:
		- Stores structured data
	- Data Lake:
		- Stores raw data (Structured and Unstructured)
- Agility:
	- Data Warehouse: 
		- Less agile due to predefined schema
	- Data Lake: 
		- More agile as it accepts raw data without a predefined structure.
- Processing:
	- Data Warehouse:
		- Extract - Transform - Load (ELT)
	- Data Lake: 
		- Extract - Load - Transform (ETL) or just load for storage purposes
- Cost:
	- Data Warehouse:
		- Typically more expensive because of optimizations for complex queries
	- Data Lake: 
		- Cost-effective storage solutions, but costs can rise when processing large amounts of data.

**Choosing a Warehouse vs Lake:**
- Use a Data Warehouse when:
	- You have structured data sources and require fast and complex queries.
	- Data integration from different sources is essential
	- Business intelligence and analytics are the primary use cases.
- Use a Data Lake when:
	- You have a mix of structured, semi-structured, or unstructured data.
	- You need a scalable and cost-effective solution to store massive amounts of data
	- Future needs for data are uncertain, and you want flexibility in storage and processing.
	- Advanced analytics, machine learning, or data discovery are key goals.
- Often, organizations use a combination of both, ingesting raw data into a data lake and then processing and moving refined data into a data warehouse for analysis.

**Data Lakehouse:**
- A hybrid architecture that combines the best features of data lakes and data warehouses, aiming to provide the performance, reliability, and capabilities of a data warehouse while maintaining the flexibility, scale, and low-cost storage of data lakes.  
- Characteristics:
	- Supports both structured and unstructured data
	- Allows for schema-on-write and schema-on-read
	- Provides capabilities for both detailed analytics and machine learning tasks.
	- Typically built on top of cloud or distributed architectures.
	- Benefits from technologies like Delta Lake, which bring ACID transactions to big data.
- Examples:
	- AWS Lake Formation (with S3 and Redshift Spectrum)
	- Delta Lake: An open-source storage layer that brings ACID transactions to Apache Spark and big data workloads
	- Databricks Lakehouse Platform: A unified platform that combines the capabilities of data lakes and data warehouses
	- Azure Synapse Analytics: Microsoft's analytics service that brings together big data and data warehousing.

## 8-Data Mesh

![](Screenshot%202024-05-20%20at%201.58.35%20PM.png)

- Coined in 2019
- It is more about governance and organization
- Individual teams own data products within a given domain
- These products serve various use cases around the organization
- Domain-based data management
- Federated governance with central standards
- Self-service tooling & infrastructure
- Data lakes, warehouses, etc. may be part of it:
	- But a data mesh is more about the data management paradigm and not the specific technologies or architectures.

## 9-Managing and Orchestrating ETL Pipelines

**ETL:**
- stands for Extract, Transform, and Load. It's a process used to move data from source systems into a data warehouse.
- **Extract:**
	- Retrieve raw data from source systems, which can be databases, CRMs, flat files, APIs, or other data repositories. 
	- Ensure data integrity during the extraction phase.
	- Can be done in real-time or in batches, depending on requirements.
- **Transform:**
	- Convert the extracted data into a format suitable for the target data warehouse.
	- Can involve various operations such as:
		- Data cleansing (e.g., removing duplicates, fixing errors)
		- Data enrichment (e.g., adding additional data from other sources)
		- Format changes (e.g., date formatting, string manipulation)
		- Aggregations or computations (e.g., calculating totals or averages)
		- Encoding or decoding data (zip or unzip)
		- Handling missing values
- **Load:**
	- Move the transformed data into the target data warehouse or another data repository
	- Can be done in batches (all at once) or in a streaming manner (as data becomes available).
	- Ensure that data maintains its integrity during the loading phase. 

**Managing ETL Pipelines**
- This process must be automated in some reliable way.
- AWS Glue (automates ETL and ELT)
- Orchestration services
	- EventBridge
	- Amazon Managed Workflows for Apache Airflow (Amazon MWAA)
	- AWS Step Functions
	- Lambda
	- Glue Workflows
## 10-Common Data Sources and Data Formats

**Data Sources:**
- JDBC (Java Database Connectivity)
	- Platform-independent
	- Language-dependent
- ODBC (Open Database Connectivity)
	- Platform-dependent (thx to drivers)
	- Language-independent
- Raw logs
- APIs
- Streams (kafka, Kenesis)

**Common Data Formats:**
- CSV (Comma-Separated Values)
	- Text-based format that represents data in a tabular from where each line corresponds to a row and values within a row are separated by commas.
	- When to Use:
		- For small to medium datasets
		- For data interchange between systems with different technologies.
		- For human-readable and editable data storage.
		- Importing/Exporting data from databases or spreadsheets.
	- Systems:
		- Databases (SQL-based)
		- Excel
		- Pandas in Python
		- R 
		- and many ETL tools
- JSON (JavaScript Object Notation)
	- Lightweight, text-based and human-readable data interchange format that represents structured or semi-structured data based on key-value pairs
	- When to Use:
		- Data interchange between a web server and a web client
		- Configurations and settings for software applications
		- Use cases that need a flexible schema or nested data structures
	- Systems:
		- Web browsers, many programming languages (like JavaSript, Python, Java, etc), RESTful APIs, NoSQL databases (like MongoDB)
- Avro:
	- Binary format that stores both the data and its schema, allowing it to be processed later with different systems without needing the original system's context. 
	- When to Use:
		- With big data and real-time processing systems. 
		- When schema evolution (changes in data structure) is needed.
		- Efficient serialization for data transport between systems.
	- Systems:
		- Apache Kafka
		- Apache Spark
		- Apache Flink
		- Hadoop ecosystem
- Parquet
	- Columnar storage format optimized for analytics. Allows for efficient compression and encoding schemes. 
	- When to Use:
		- Analyzing large datasets with analytics engines.
		- Use cases where reading specific columns instead of entire records is beneficial
		- Storing data on distributed systems where I/O operations and storage need optimization. 
	- Systems:
		- Hadoop ecosystem
		- Apache Spark
		- Apache Hive
		- Apache Impala
		- Amazon Redshift Spectrum

## 11-Quick Review of Data Modeling, Data Lineage, and Schema Evolution

**Here's a star schema:**
- Fact tables
- Dimensions
- Primary / foreign keys

![](Screenshot%202024-05-20%20at%203.35.58%20PM.png)

>NOTE: This sort of diagram is an Entity Relationship Diagram (ERD)

**Data Lineage:**
- A visual representation that traces the flow and transformation of data through its lifecycle, from its source to its final destination. 
- This is a record of what you did with the data along the way
- **Importance:**
	- Helps in tracking errors back to their source.
	- Ensures compliance with regulations
	- Provides a clear understanding of how data is moved, transformed, and consumed within systems. 

![](Screenshot%202024-05-20%20at%203.40.02%20PM.png)

**Example of Data Lineage on AWS:**
- Example of capturing data lineage
	- Uses Spline Agent (for Spark) attached to Glue
	- Dump lineage data into Neptune via Lambda

![](Screenshot%202024-05-20%20at%203.43.30%20PM.png)

Blog: https://aws.amazon.com/blogs/big-data/build-data-lineage-for-data-lakes-using-aws-glue-amazon-neptune-and-spline/


Schema Evolution:
- The ability to adapt and change the schema of a dataset over time without disrupting existing processes or systems. 
- Importance:
	- Ensures data systems can adapt to changing business requirements
	- Allows for the addition, removal, or modification of columns/fields in a dataset
	- Maintains backward compatibility with older data records.
- Glue Schema Registry
	- Schema discovery, compatibility, validation, registration. 
![](Screenshot%202024-05-20%20at%203.48.18%20PM.png)

## 12-Database Performance Optimization

- **Indexing:**
	- ==Avoid full table scans!==
	- Enforce data uniqueness and integrity
- **Partitioning:**
	- Reduce amount of data scanned
	- For example, maybe you know you are only going to read from a partition based on the current month. 
	- Helps with data lifecycle management
	- Enables parallel processing
- **Compression**
	- Speed up data transfer, reduce storage & disk reads
	- GZIP, LZOP, BZIP2, ZSTD (Redshift examples)
		- Various tradeoffs between compression and speed
	- Columnar compression

## 13-Data Sampling Techniques

- Random Sampling 
	- Everything has an equal chance of being selected
- Stratified Sampling 
	- Divide population into homogenous subgroups (strata)
	- Random sample within each stratum
	- Ensures representation of each subgroup
- Others:
	- Systemic, Cluster, Convenience, Judgmental

![](Screenshot%202024-05-20%20at%203.55.32%20PM.png)


## 14-Data Skew Mechanisms

Data skew:
- Refers to the unequal distribution or imbalance of data across various nodes or partitions in distributed computing systems. 
- The celebrity problem:
	- Even partitioning doesn't work if your traffic is uneven
	- Imagine you're IMDb... Brad Pitt could overload his partition
- Causes:
	- Non-uniform distribution of data
	- Inadequate partitioning strategy
	- Temporal skew
- Important to monitor data distribution and alert when skew issues arise.

**Addressing Data Skew:**
1. Adaptive Partitioning: Dynamically adjust partitioning based on data characteristics to ensure a more balanced distribution. 
2. Salting: Introduce a random factor or `salt` to the data to distribute it more uniformly. 
3. Repartitioning: Regularly redistribute the data based on its current distribution characteristics. 
4. Sampling: Use a sample of the data to determine the distribution and adjust the processing strategy accordingly
5. Custom Partitioning: Define custom rules or functions for partitioning data based on domain knowledge. 

## 15-Data Validation and Profiling

- Data Completeness
	- Ensures all required data is present and no essential parts are missing. 
	- Checks: Missing values, null counts, percentage of populated fields.
	- Importance: Missing data can lead to inaccurate analyses and insights.
- Data Consistency:
	- Ensures data values are consistent across datasets and do not contradict each other.
	- Checks: Cross-field validation, comparing data from different sources or periods
	- Importance: Inconsistent data can cause confusion and result in incorrect conclusions.
- Accuracy:
	- Ensure data is correct, reliable, and represents what it is supposed to. 
	- Checks: Comparing with trusted sources, validation against known standards or rules.
	- Importance: Inaccurate data can lead to false insights and poor decision-making.
- Integrity:
	- Ensures data maintains its correctness and consistency over its lifecycle and across systems.
	- Checks: Referential integrity (e.g., foreign key checks in databases), relationships validations. 
	- Importance: Ensures relationships between data elements are preserved, and data remains trustworthy over time. 

![](Screenshot%202024-05-20%20at%204.13.40%20PM.png)
## 16- SQL Review: Aggregations, Grouping, Sorting, Pivoting

If beginner with SQL than add a course. 

**Aggregation**
- Count (Get the total number of rows from employees table)
	- SELECT COUNT`(*)` AS total_rows FROM employees;
- SUM (Add all the salaries in the employees table)
	- SELECT SUM (salary) AS total_salary FROM employees;
- AVG
	- SELECT AVG (salary) AS average_salary FROM employees;
- MAX/MIN
	- SELECT MAX (salary) AS highest_salary FROM employees;

**Aggregate with CASE**
- WHERE clauses are specified after aggregation, so you can only filter on one thing at a time.
	- SELECT COUNT`(*)` AS high_salary_count FROM employees WHERE salary > 70000;
- One way to apply multiple filters to what you're aggregating
	- SELECT
		- COUNT (CASE WHEN salary > 70000 THEN 1 END) AS high_salary_count,
		- COUNT (CASE WHEN salary BETWEEN 50000 AND 70000 THEN 1 END) AS medium_salary_count,
		- COUNT (CASE WHEN salary <50000 THEN 1 END) AS low_salary_count
	- FROM employees;

![](Screenshot%202024-05-21%20at%2010.10.06%20AM.png)


![](Screenshot%202024-05-21%20at%2010.10.42%20AM.png)


![](Screenshot%202024-05-21%20at%2010.12.18%20AM.png)

![](Screenshot%202024-05-21%20at%2010.13.38%20AM.png)

## 17-SQL JOIN types

![](Screenshot%202024-05-21%20at%2010.14.53%20AM.png)


![](Screenshot%202024-05-21%20at%2010.16.00%20AM.png)

![](Screenshot%202024-05-21%20at%2010.16.22%20AM.png)

![](Screenshot%202024-05-21%20at%2010.17.00%20AM.png)

![](Screenshot%202024-05-21%20at%2010.17.50%20AM.png)


![](Screenshot%202024-05-21%20at%2010.18.19%20AM.png)
## 18-SQL Regular Expressions (a quick intro)

SQL Regular Expressions
- Pattern matching
	- Think a much more powerful "LIKE"
- `~` is the regular expression operator
- `~*` is case-insensitive
- `!~*` would mean "not match expression, case insensitive"
- Regular expression 101
	- `^` match a pattern at the start of a string
	- `$` match a pattern at the end of a string (boo$ would match boo but not book)
	- `|` alternate characters (sit|sat matches both sit and sat)
	- Ranges ([a-z] matches any lower case letter)
	- Repeats ([a-z]{4} matches any four-letter lowercase word)
	- Special metacharacters
		- `\d` any digit
		- `\w` any letter, digit, or underscore
		- `\s` whitespace
		- `\t` tab
- Example:
	- SELECT `*` FROM name WHERE name `~*^(fire|ice)`;
	- selects any rows where the name starts with fire or ice (case insensitive)

## 19- A note about SQL coding exercises

1. Practicing aggregation queries in SQL

**Women and children first!**

You probably know the story of the Titanic, an ocean liner that tragically sank in 1912. A famous policy of the time was "women and children first" when loading up the lifeboats in such a situation. Does the data show this is what actually happened on the Titanic?

We've loaded up a sample of 100 passengers on the Titanic, which includes their age in years, whether they survived, and their self-reported gender, into a table named **titanic**. Explore this data, and compute:
  

- A listing of the first ten rows in the **titanic** table, to help you understand its structure and column names.
- The overall survival rate of the passengers in this data set. This result should be labeled **overall_rate**
- The overall survival rate of "women and children," identified by a gender of 'female' or age of 12 or younger. This result should be labeled **women_children_rate**.
- The overall survival rate of everyone else who does not fit our definition of "women and children." This result should be labeled **others_rate**.

Compute these as four separate SQL queries; we're not looking to use grouping here yet.

Did women and children have better odds of surviving the Titanic than others did?

2. Practicing grouping queries in SQL

**Did class matter?** We have the same sample of 100 passengers on the Titanic, but this time we want to explore if the passenger class of their ticket (first, second, or third class) affected their odds of survival. 

Your sample dataset is in a table named **titanic**. This contains a column named **Survived**, which is 1 if they survived and 0 if not. There is also a **Pclass** column indicating their passenger class (1, 2, or 3.)

Your task is to use **GROUP BY** in SQL to produce the survival rate for each passenger class in our dataset. Your output should contain a table with two columns named **Pclass** and **survival_rate**. The results should be sorted in ascending order by passenger class.

3. Practicing join queries in SQL

We've loaded up a couple of tables of data from a fictional retailer: **Products**, containing information about the products sold by the company, and **Suppliers**, containing information about the companies that provided those products. These two tables are connected by columns named **SupplierID**.

Create a report of every **ProductName** in the **Products** table, together with the **CompanyName** associated with each product's supplier.

This query should be written in such a way that **every** product is listed in your report, even if no match exists in the Suppliers table for its SupplierID. Your final results should be sorted alphabetically by ProductName.
## 20-Git review: architecture and commands

![](Screenshot%202024-05-21%20at%2010.35.00%20AM.png)


![](Screenshot%202024-05-21%20at%2010.36.56%20AM.png)

![](Screenshot%202024-05-21%20at%2010.37.59%20AM.png)

![](Screenshot%202024-05-21%20at%2010.38.39%20AM.png)

![](Screenshot%202024-05-21%20at%2010.39.16%20AM.png)
![](Screenshot%202024-05-21%20at%2010.40.28%20AM.png)
![](Screenshot%202024-05-21%20at%2010.41.00%20AM.png)
![](Screenshot%202024-05-21%20at%2010.41.24%20AM.png)






