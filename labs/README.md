# AWS Data Engineer Labs

This directory contains hands-on labs designed to help prepare for the AWS Certified Data Engineer - Associate (DEA-C01) exam. Each lab focuses on specific exam domains and provides practical experience with AWS data services.

## Lab Structure

Each lab follows a consistent structure:

1. **Overview**: Description of the lab and learning objectives
2. **Prerequisites**: Required AWS services, permissions, and sample data
3. **Step-by-step Instructions**: Detailed implementation steps
4. **Validation**: How to verify successful completion
5. **Cleanup**: Instructions to remove resources and avoid charges
6. **Challenge Extensions**: Optional advanced tasks

## Lab Categories

### Data Ingestion
Labs focused on collecting and importing data from various sources into AWS.
- [Lab 1.1: Batch Ingestion with AWS Glue](./data-ingestion/lab-1.1-batch-ingestion-glue.md)
- [Lab 1.2: Streaming Data with Kinesis](./data-ingestion/lab-1.2-streaming-kinesis.md)
- [Lab 1.3: Database Migration with DMS](./data-ingestion/lab-1.3-database-migration-dms.md)

### Data Storage
Labs covering different storage options and data organization strategies.
- [Lab 2.1: S3 Data Lake Organization](./data-storage/lab-2.1-s3-data-lake.md)
- [Lab 2.2: Redshift Data Warehouse Setup](./data-storage/lab-2.2-redshift-warehouse.md)
- [Lab 2.3: DynamoDB for NoSQL Data](./data-storage/lab-2.3-dynamodb-nosql.md)

### Data Transformation
Labs on processing and transforming data using AWS services.
- [Lab 3.1: ETL with AWS Glue](./data-transformation/lab-3.1-etl-glue.md)
- [Lab 3.2: Stream Processing with Kinesis Analytics](./data-transformation/lab-3.2-stream-processing.md)
- [Lab 3.3: Data Quality and Validation](./data-transformation/lab-3.3-data-quality.md)

### Security and Governance
Labs focusing on securing data and implementing governance controls.
- [Lab 4.1: Lake Formation Permissions](./security-governance/lab-4.1-lake-formation.md)
- [Lab 4.2: Column-Level Security](./security-governance/lab-4.2-column-security.md)
- [Lab 4.3: Cross-Account Data Sharing](./security-governance/lab-4.3-cross-account.md)

### Operations and Optimization
Labs on monitoring, managing, and optimizing data pipelines.
- [Lab 5.1: Pipeline Orchestration with Step Functions](./operations-optimization/lab-5.1-step-functions.md)
- [Lab 5.2: Monitoring and Alerting](./operations-optimization/lab-5.2-monitoring.md)
- [Lab 5.3: Cost Optimization Strategies](./operations-optimization/lab-5.3-cost-optimization.md)

## Sample Datasets

The labs use the following sample datasets:

1. **NYC Taxi Data**: Trip records from the NYC Taxi & Limousine Commission
2. **E-commerce Dataset**: Synthetic online retail transaction data
3. **IoT Sensor Data**: Simulated sensor readings for real-time processing
4. **Customer Database**: Sample customer records for migration exercises

## Getting Started

1. Ensure you have an AWS account with appropriate permissions
2. Review the prerequisites for each lab before starting
3. Follow labs in sequence within each category for best learning progression
4. Complete cleanup steps after each lab to avoid unnecessary charges

## Cost Considerations

These labs are designed with cost efficiency in mind:
- Many labs can be completed within AWS Free Tier limits
- Estimated costs are provided for services that may incur charges
- Cleanup instructions are included to help avoid ongoing charges
- Consider using AWS Budgets to set alerts for cost management
