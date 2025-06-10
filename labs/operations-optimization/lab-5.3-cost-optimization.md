# Lab 5.3: Cost Optimization Strategies

## Overview
This lab focuses on implementing cost optimization strategies for AWS data services. You will learn how to analyze costs, identify optimization opportunities, and implement cost-saving measures for data pipelines and storage, which are essential skills for the AWS Certified Data Engineer exam.

**Learning Objectives:**
- Analyze and understand AWS data service costs
- Implement S3 storage class optimization
- Configure Redshift cost optimization strategies
- Optimize Glue ETL job costs
- Implement data lifecycle policies
- Set up cost monitoring and alerting
- Create cost allocation strategies with tags

**AWS Services Used:**
- AWS Cost Explorer
- Amazon S3
- Amazon Redshift
- AWS Glue
- AWS Lambda
- AWS Budgets
- AWS Cost and Usage Report
- AWS Trusted Advisor

**Estimated Time:** 3 hours

**Estimated Cost:** $5-10 (Most resources fall under Free Tier if available)

## Prerequisites
- AWS Account with appropriate permissions
- IAM permissions for Cost Explorer, S3, Redshift, and Glue
- Basic understanding of AWS pricing models
- Familiarity with AWS data services
- Access to billing information for your AWS account

## Architecture Diagram
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │     │             │
│  AWS Cost   │────▶│  Cost       │────▶│  AWS        │────▶│  SNS        │
│  Explorer   │     │  Analysis   │     │  Budgets    │     │  Alerts     │
│             │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                    │                    │
                          │                    │                    │
                          ▼                    ▼                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │     │             │
│  S3         │◀───▶│  Redshift   │◀───▶│  Glue       │◀───▶│  Lambda     │
│  Lifecycle  │     │  Scaling    │     │  Job        │     │  Functions  │
│  Policies   │     │  Optimization│     │  Tuning     │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## Implementation Steps

### Step 1: Set Up Cost Analysis Environment

#### 1.1: Enable Cost Explorer
1. Sign in to the AWS Management Console
2. Navigate to the AWS Cost Management console
3. Go to "Cost Explorer" and enable it if not already enabled
4. Wait for the data to be populated (may take up to 24 hours if newly enabled)

#### 1.2: Create a Cost and Usage Report
1. In the AWS Cost Management console, go to "Cost & Usage Reports"
2. Click "Create report"
3. Configure the report:
   - Report name: `DataServicesUsageReport`
   - Additional report details: Include resource IDs
   - Time granularity: Hourly
   - Report data integration: None
   - S3 bucket: Create a new bucket or select an existing one
   - Report path prefix: `cost-reports`
   - Time granularity: Hourly
   - Compression type: Parquet
   - Enable report data integration for: None
4. Click "Next" and then "Create report"

### Step 2: Create Sample Data Resources for Optimization

#### 2.1: Create S3 Buckets with Different Storage Classes
1. Navigate to the Amazon S3 console
2. Create a new S3 bucket with a unique name (e.g., `your-name-cost-optimization-YYYYMMDD`)
   ```
   aws s3 mb s3://your-name-cost-optimization-YYYYMMDD
   ```
3. Create the following folder structure:
   ```
   aws s3api put-object --bucket your-name-cost-optimization-YYYYMMDD --key standard/
   aws s3api put-object --bucket your-name-cost-optimization-YYYYMMDD --key infrequent-access/
   aws s3api put-object --bucket your-name-cost-optimization-YYYYMMDD --key glacier/
   aws s3api put-object --bucket your-name-cost-optimization-YYYYMMDD --key deep-archive/
   ```

4. Upload sample files to each folder:
   ```
   # Create sample files of different sizes
   dd if=/dev/zero of=sample-1mb.dat bs=1024 count=1024
   dd if=/dev/zero of=sample-10mb.dat bs=1024 count=10240
   dd if=/dev/zero of=sample-100mb.dat bs=1024 count=102400
   
   # Upload to standard storage
   aws s3 cp sample-1mb.dat s3://your-name-cost-optimization-YYYYMMDD/standard/
   aws s3 cp sample-10mb.dat s3://your-name-cost-optimization-YYYYMMDD/standard/
   aws s3 cp sample-100mb.dat s3://your-name-cost-optimization-YYYYMMDD/standard/
   
   # Upload to infrequent access with appropriate storage class
   aws s3 cp sample-1mb.dat s3://your-name-cost-optimization-YYYYMMDD/infrequent-access/ --storage-class STANDARD_IA
   aws s3 cp sample-10mb.dat s3://your-name-cost-optimization-YYYYMMDD/infrequent-access/ --storage-class STANDARD_IA
   aws s3 cp sample-100mb.dat s3://your-name-cost-optimization-YYYYMMDD/infrequent-access/ --storage-class STANDARD_IA
   
   # Upload to Glacier
   aws s3 cp sample-1mb.dat s3://your-name-cost-optimization-YYYYMMDD/glacier/ --storage-class GLACIER
   aws s3 cp sample-10mb.dat s3://your-name-cost-optimization-YYYYMMDD/glacier/ --storage-class GLACIER
   aws s3 cp sample-100mb.dat s3://your-name-cost-optimization-YYYYMMDD/glacier/ --storage-class GLACIER
   
   # Upload to Deep Archive
   aws s3 cp sample-1mb.dat s3://your-name-cost-optimization-YYYYMMDD/deep-archive/ --storage-class DEEP_ARCHIVE
   aws s3 cp sample-10mb.dat s3://your-name-cost-optimization-YYYYMMDD/deep-archive/ --storage-class DEEP_ARCHIVE
   aws s3 cp sample-100mb.dat s3://your-name-cost-optimization-YYYYMMDD/deep-archive/ --storage-class DEEP_ARCHIVE
   ```

#### 2.2: Set Up a Small Redshift Cluster
1. Navigate to the Amazon Redshift console
2. Click "Create cluster"
3. Configure the cluster:
   - Cluster identifier: `cost-optimization-cluster`
   - Node type: dc2.large (smallest available for testing)
   - Number of nodes: 2
   - Database name: `costoptimization`
   - Admin username: `admin`
   - Admin password: Create and save a secure password
4. For network and security:
   - Choose a VPC and subnet
   - Enable "Publicly accessible" (for lab purposes)
   - Create a new security group or use an existing one
5. Create the cluster and wait for it to become available

#### 2.3: Create AWS Glue Jobs with Different Configurations
1. Navigate to the AWS Glue console
2. Create a new Glue job with standard configuration:
   - Name: `standard-etl-job`
   - IAM role: Create or select a role with appropriate permissions
   - Type: Spark
   - Glue version: Glue 3.0
   - Worker type: G.1X
   - Number of workers: 5
   - Job timeout: 60 minutes
   - Script:

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import time

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Simulate data processing
print("Starting data processing simulation")
for i in range(30):
    print(f"Processing batch {i+1}/30")
    time.sleep(10)  # Sleep for 10 seconds

print("Job completed successfully")
job.commit()
```

3. Create another Glue job with optimized configuration:
   - Name: `optimized-etl-job`
   - IAM role: Same as above
   - Type: Spark
   - Glue version: Glue 3.0
   - Worker type: G.1X
   - Number of workers: 2
   - Job timeout: 30 minutes
   - Same script as above

### Step 3: Implement S3 Storage Optimization

#### 3.1: Configure S3 Lifecycle Policies
1. Navigate to the S3 console
2. Select your bucket `your-name-cost-optimization-YYYYMMDD`
3. Go to the "Management" tab and click "Create lifecycle rule"
4. Create a rule for transitioning standard objects:
   - Rule name: `standard-to-ia-to-glacier`
   - Rule scope: Limit the scope to specific prefixes
   - Prefix: `standard/`
   - Lifecycle rule actions:
     - Transition current versions of objects between storage classes
     - Transition to Standard-IA after 30 days
     - Transition to Glacier after 90 days
     - Transition to Glacier Deep Archive after 180 days
5. Create the rule

6. Create another rule for cleaning up incomplete multipart uploads:
   - Rule name: `cleanup-incomplete-uploads`
   - Rule scope: Apply to all objects in the bucket
   - Lifecycle rule actions:
     - Delete expired object delete markers or incomplete multipart uploads
     - Delete incomplete multipart uploads after 7 days
7. Create the rule

#### 3.2: Analyze S3 Storage Costs
1. Navigate to the S3 console
2. Select your bucket `your-name-cost-optimization-YYYYMMDD`
3. Go to the "Metrics" tab
4. Click "Create storage class analysis"
5. Configure the analysis:
   - Filter: Entire bucket
   - Name: `storage-class-analysis`
6. Create the analysis

### Step 4: Optimize Redshift Costs

#### 4.1: Configure Redshift Concurrency Scaling
1. Navigate to the Redshift console
2. Select your cluster `cost-optimization-cluster`
3. Click "Properties"
4. Under "Concurrency scaling", click "Edit"
5. Enable concurrency scaling
6. Save changes

#### 4.2: Set Up Redshift Pause and Resume Schedule
1. In the Redshift console, select your cluster
2. Click "Actions" > "Manage scheduling"
3. Configure a schedule:
   - Enable schedule: Yes
   - Schedule action: Pause cluster
   - Schedule frequency: Custom
   - Set a time when you don't need the cluster (e.g., nights and weekends)
4. Add another schedule for resuming the cluster
5. Save the schedules

#### 4.3: Configure Redshift Snapshot Management
1. In the Redshift console, select your cluster
2. Click "Properties"
3. Under "Backup", click "Edit"
4. Configure automated snapshots:
   - Automated snapshot retention period: 7 days (default is 35)
   - Manual snapshot retention period: 30 days
5. Save changes

### Step 5: Optimize AWS Glue Costs

#### 5.1: Configure Glue Job Bookmarks
1. Navigate to the AWS Glue console
2. Select your job `optimized-etl-job`
3. Click "Action" > "Edit job"
4. Under "Job parameters", add:
   - Key: `--job-bookmark-option`
   - Value: `job-bookmark-enable`
5. Save the job

#### 5.2: Configure Autoscaling for Glue Jobs
1. Modify your `optimized-etl-job` script to include autoscaling:

```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import time

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Enable autoscaling
spark.conf.set("spark.dynamicAllocation.enabled", "true")
spark.conf.set("spark.dynamicAllocation.minExecutors", "2")
spark.conf.set("spark.dynamicAllocation.maxExecutors", "10")

# Simulate data processing
print("Starting data processing simulation with autoscaling")
for i in range(30):
    print(f"Processing batch {i+1}/30")
    time.sleep(5)  # Sleep for 5 seconds

print("Job completed successfully")
job.commit()
```

2. Save the job

#### 5.3: Configure Glue Development Endpoints Cost Controls
1. Navigate to the AWS Glue console
2. Go to "Dev endpoints" and click "Add endpoint"
3. Configure the endpoint with cost-saving settings:
   - Name: `cost-optimized-dev-endpoint`
   - IAM role: Select an appropriate role
   - Worker type: G.1X (instead of G.2X)
   - Number of workers: 2 (minimum needed)
   - Idle timeout: 30 minutes (default is 2880)
4. Create the endpoint

### Step 6: Set Up Cost Monitoring and Alerting

#### 6.1: Create AWS Budgets
1. Navigate to the AWS Cost Management console
2. Go to "Budgets" and click "Create budget"
3. Choose "Cost budget"
4. Configure the budget:
   - Name: `DataServicesBudget`
   - Period: Monthly
   - Start date: First day of current month
   - Budget amount: Set an appropriate amount (e.g., $100)
   - Budget scope: Filter by tags, services, or accounts
   - Services: Select Amazon S3, Amazon Redshift, AWS Glue
5. Click "Next"
6. Set up alerts:
   - Alert threshold: 80% of budgeted amount
   - Email recipients: Your email address
7. Create the budget

#### 6.2: Create a Lambda Function for Cost Optimization
1. Navigate to the Lambda console
2. Click "Create function"
3. Choose "Author from scratch"
4. Configure the function:
   - Function name: `CostOptimizationFunction`
   - Runtime: Python 3.9
   - Architecture: x86_64
   - Execution role: Create a new role with basic Lambda permissions
5. Click "Create function"
6. Replace the code with the following:

```python
import json
import boto3
import os
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Initialize clients
    redshift = boto3.client('redshift')
    glue = boto3.client('glue')
    ce = boto3.client('ce')
    
    # Get current date and time
    now = datetime.utcnow()
    start_date = (now - timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = now.strftime('%Y-%m-%d')
    
    # Check Redshift cluster utilization
    try:
        clusters = redshift.describe_clusters()
        for cluster in clusters.get('Clusters', []):
            cluster_id = cluster['ClusterIdentifier']
            node_type = cluster['NodeType']
            node_count = cluster['NumberOfNodes']
            
            # Get CloudWatch metrics for CPU utilization
            cloudwatch = boto3.client('cloudwatch')
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/Redshift',
                MetricName='CPUUtilization',
                Dimensions=[
                    {'Name': 'ClusterIdentifier', 'Value': cluster_id}
                ],
                StartTime=now - timedelta(days=7),
                EndTime=now,
                Period=86400,  # 1 day in seconds
                Statistics=['Average']
            )
            
            # Calculate average CPU utilization
            datapoints = response.get('Datapoints', [])
            if datapoints:
                avg_cpu = sum(point['Average'] for point in datapoints) / len(datapoints)
                print(f"Cluster {cluster_id} average CPU utilization: {avg_cpu:.2f}%")
                
                # Recommend downsizing if utilization is consistently low
                if avg_cpu < 30.0:
                    print(f"RECOMMENDATION: Consider downsizing cluster {cluster_id} due to low CPU utilization")
    except Exception as e:
        print(f"Error analyzing Redshift clusters: {str(e)}")
    
    # Check Glue job efficiency
    try:
        jobs = glue.get_jobs()
        for job in jobs.get('Jobs', []):
            job_name = job['Name']
            dpu_capacity = job.get('MaxCapacity', 0)
            worker_type = job.get('WorkerType', 'Unknown')
            num_workers = job.get('NumberOfWorkers', 0)
            
            # Get job runs
            job_runs = glue.get_job_runs(JobName=job_name, MaxResults=10)
            
            # Calculate average duration and DPU hours
            total_duration = 0
            count = 0
            for run in job_runs.get('JobRuns', []):
                if run.get('JobRunState') == 'SUCCEEDED':
                    start_time = run.get('StartedOn')
                    end_time = run.get('CompletedOn')
                    if start_time and end_time:
                        duration = (end_time - start_time).total_seconds() / 3600  # hours
                        total_duration += duration
                        count += 1
            
            if count > 0:
                avg_duration = total_duration / count
                dpu_hours = avg_duration * dpu_capacity
                print(f"Job {job_name} average duration: {avg_duration:.2f} hours, DPU-hours: {dpu_hours:.2f}")
                
                # Recommend optimization if job is inefficient
                if dpu_hours > 10 and worker_type == 'G.1X' and num_workers > 2:
                    print(f"RECOMMENDATION: Consider optimizing job {job_name} to reduce DPU-hours")
    except Exception as e:
        print(f"Error analyzing Glue jobs: {str(e)}")
    
    # Get cost and usage data
    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ]
        )
        
        # Analyze costs by service
        for result in response['ResultsByTime']:
            for group in result['Groups']:
                service = group['Keys'][0]
                amount = float(group['Metrics']['BlendedCost']['Amount'])
                if service in ['Amazon Redshift', 'Amazon S3', 'AWS Glue'] and amount > 0:
                    print(f"Cost for {service}: ${amount:.2f}")
    except Exception as e:
        print(f"Error getting cost data: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Cost optimization analysis completed')
    }
```

7. Click "Deploy"
8. Add permissions to the Lambda function's role:
   - Navigate to the IAM console
   - Find the role created for your Lambda function
   - Attach the following policies:
     - `AmazonRedshiftReadOnlyAccess`
     - `AWSGlueConsoleFullAccess`
     - `AmazonS3ReadOnlyAccess`
     - `CloudWatchReadOnlyAccess`
     - `AWSCostExplorerServiceFullAccess`

#### 6.3: Schedule the Lambda Function
1. Navigate to the Amazon EventBridge console
2. Go to "Rules" and click "Create rule"
3. Configure the rule:
   - Name: `WeeklyCostOptimizationCheck`
   - Description: "Weekly check for cost optimization opportunities"
   - Rule type: Schedule
4. Define the schedule pattern:
   - Schedule type: Cron expression
   - Cron expression: `0 0 ? * MON *` (Runs at midnight every Monday)
5. Click "Next"
6. Select target:
   - Target type: AWS service
   - Target: Lambda function
   - Function: `CostOptimizationFunction`
7. Click "Next", then "Next" again
8. Click "Create rule"

### Step 7: Implement Resource Tagging for Cost Allocation

#### 7.1: Create a Tagging Strategy
1. Define a set of tags for cost allocation:
   - `Environment`: dev, test, prod
   - `Department`: data-engineering, analytics, marketing
   - `Project`: project-a, project-b
   - `CostCenter`: cc-1234, cc-5678

#### 7.2: Apply Tags to Resources
1. Navigate to the S3 console
2. Select your bucket `your-name-cost-optimization-YYYYMMDD`
3. Go to "Properties" > "Tags" and click "Edit"
4. Add the following tags:
   - Key: `Environment`, Value: `dev`
   - Key: `Department`, Value: `data-engineering`
   - Key: `Project`, Value: `cost-optimization-lab`
   - Key: `CostCenter`, Value: `cc-1234`
5. Save the tags

6. Navigate to the Redshift console
7. Select your cluster `cost-optimization-cluster`
8. Click "Tags" and add the same set of tags
9. Save the tags

10. Navigate to the AWS Glue console
11. Select your jobs and add the same set of tags
12. Save the tags

#### 7.3: Create Cost Allocation Reports
1. Navigate to the AWS Cost Management console
2. Go to "Cost allocation tags"
3. Select the tags you created and click "Activate"
4. Go to "Cost Explorer"
5. Create a new report:
   - Report type: Cost
   - Time range: Last 3 months
   - Granularity: Monthly
   - Group by: Tag: Environment
   - Filter: Services (Amazon S3, Amazon Redshift, AWS Glue)
6. Save the report as `EnvironmentCostAllocation`

7. Create another report grouped by Department
8. Save the report as `DepartmentCostAllocation`

### Step 8: Analyze and Document Cost Optimization Recommendations

1. Create a document summarizing cost optimization recommendations:

```markdown
# AWS Data Services Cost Optimization Recommendations

## Amazon S3
- Implement lifecycle policies to transition data to cheaper storage classes
- Use S3 Intelligent-Tiering for data with unknown or changing access patterns
- Enable S3 analytics to identify optimization opportunities
- Delete incomplete multipart uploads and old versions
- Compress data before storing in S3

## Amazon Redshift
- Use appropriate node types based on workload (compute vs. storage optimized)
- Implement pause/resume schedules for non-production clusters
- Use concurrency scaling only when needed
- Optimize queries to reduce execution time
- Use appropriate sort and distribution keys
- Implement automated vacuum and analyze operations

## AWS Glue
- Use job bookmarks to process only new data
- Optimize worker type and number based on data volume
- Use dynamic allocation to scale resources as needed
- Implement appropriate timeout settings
- Schedule jobs during off-peak hours
- Use Glue 3.0 for better performance and cost efficiency

## General Recommendations
- Implement comprehensive tagging strategy for cost allocation
- Set up budgets and alerts for cost monitoring
- Regularly review and analyze usage patterns
- Implement automated cost optimization checks
- Consider reserved instances for stable workloads
- Delete unused resources promptly
```

2. Save this document for future reference

## Validation Steps
1. Verify that S3 lifecycle policies are correctly configured
2. Confirm that Redshift pause/resume schedules are set up
3. Check that Glue job optimizations are implemented
4. Verify that cost monitoring and alerting are working
5. Confirm that resource tagging is applied consistently
6. Review cost allocation reports for accuracy

## Cleanup Instructions
1. Delete the Redshift cluster
   ```
   aws redshift delete-cluster --cluster-identifier cost-optimization-cluster --skip-final-cluster-snapshot
   ```
2. Delete the Glue jobs
   ```
   aws glue delete-job --job-name standard-etl-job
   aws glue delete-job --job-name optimized-etl-job
   ```
3. Delete the Glue development endpoint
   ```
   aws glue delete-dev-endpoint --endpoint-name cost-optimized-dev-endpoint
   ```
4. Delete the Lambda function
   ```
   aws lambda delete-function --function-name CostOptimizationFunction
   ```
5. Delete the EventBridge rule
   ```
   aws events delete-rule --name WeeklyCostOptimizationCheck
   ```
6. Delete the S3 bucket and its contents
   ```
   aws s3 rb s3://your-name-cost-optimization-YYYYMMDD --force
   ```
7. Delete the AWS Budgets
   ```
   # Use AWS Cost Management console to delete budgets
   ```

## Challenge Extensions (Optional)
1. Implement AWS Cost Anomaly Detection
2. Create a custom dashboard for cost optimization metrics
3. Implement automated resource rightsizing recommendations
4. Create a cost optimization Lambda function that takes automatic actions
5. Implement cross-account cost analysis for multi-account environments
6. Create a cost optimization scorecard for different teams

## Additional Resources
- [AWS Cost Optimization Hub](https://aws.amazon.com/aws-cost-management/cost-optimization-hub/)
- [AWS Well-Architected Framework - Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)
- [S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/)
- [Redshift Cost Optimization](https://docs.aws.amazon.com/redshift/latest/dg/c-optimizing-query-performance.html)
- [AWS Glue Best Practices](https://docs.aws.amazon.com/glue/latest/dg/best-practices.html)
- [AWS Tagging Strategies](https://aws.amazon.com/answers/account-management/aws-tagging-strategies/)

## Notes and Tips
- Cost optimization is an ongoing process, not a one-time activity
- Balance cost optimization with performance and reliability requirements
- Consider the administrative overhead of complex optimization strategies
- Automate cost optimization where possible to ensure consistency
- Involve stakeholders in cost optimization decisions
- Regularly review and update your cost optimization strategy
- Consider the total cost of ownership, not just the AWS bill
