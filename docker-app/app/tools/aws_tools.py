"""
AWS Tools for AWS Data Engineer Agents

This module implements tools for accessing AWS documentation and service information.
"""

from typing import Dict, List, Any
from strands import tool
import boto3
import json


@tool
def aws_service_info_tool(service_name: str) -> str:
    """
    Provides information about specific AWS services relevant to data engineering.
    
    Args:
        service_name: Name of the AWS service (e.g., 'glue', 's3', 'kinesis')
        
    Returns:
        Information about the AWS service including key features and use cases
    """
    try:
        # Service information database
        services_info = {
            "glue": {
                "name": "AWS Glue",
                "category": "Data Integration",
                "description": "Serverless data integration service for ETL workloads",
                "key_features": [
                    "Visual ETL job creation",
                    "Automatic schema discovery",
                    "Built-in data catalog",
                    "Serverless execution",
                    "Support for Apache Spark and Python"
                ],
                "use_cases": [
                    "ETL data processing",
                    "Data catalog management",
                    "Data preparation for analytics",
                    "Data lake organization"
                ],
                "pricing": "Pay per use - charged for crawler runtime and ETL job runtime"
            },
            "kinesis": {
                "name": "Amazon Kinesis",
                "category": "Real-time Data Streaming",
                "description": "Platform for streaming data on AWS",
                "key_features": [
                    "Real-time data ingestion",
                    "Multiple data streams",
                    "Built-in analytics",
                    "Integration with other AWS services"
                ],
                "use_cases": [
                    "Real-time analytics",
                    "Log and event data collection",
                    "IoT data streaming",
                    "Clickstream analysis"
                ],
                "pricing": "Pay per shard hour and data records processed"
            },
            "s3": {
                "name": "Amazon S3",
                "category": "Object Storage",
                "description": "Scalable object storage service",
                "key_features": [
                    "Virtually unlimited storage",
                    "Multiple storage classes",
                    "Data lifecycle management",
                    "Strong consistency",
                    "Versioning and encryption"
                ],
                "use_cases": [
                    "Data lake storage",
                    "Backup and archiving",
                    "Content distribution",
                    "Big data analytics"
                ],
                "pricing": "Pay for storage used, requests, and data transfer"
            },
            "redshift": {
                "name": "Amazon Redshift",
                "category": "Data Warehouse",
                "description": "Fast, scalable data warehouse service",
                "key_features": [
                    "Columnar storage",
                    "Massively parallel processing",
                    "Advanced compression",
                    "Machine learning integration",
                    "Serverless option available"
                ],
                "use_cases": [
                    "Business intelligence",
                    "Data warehousing",
                    "Analytics workloads",
                    "Reporting and dashboards"
                ],
                "pricing": "Pay per node hour or serverless usage"
            },
            "dynamodb": {
                "name": "Amazon DynamoDB",
                "category": "NoSQL Database",
                "description": "Fast and flexible NoSQL database service",
                "key_features": [
                    "Single-digit millisecond latency",
                    "Automatic scaling",
                    "Built-in security",
                    "Global tables",
                    "Streams for change capture"
                ],
                "use_cases": [
                    "Web and mobile applications",
                    "Gaming applications",
                    "IoT applications",
                    "Real-time personalization"
                ],
                "pricing": "Pay per request or provisioned capacity"
            },
            "dms": {
                "name": "AWS Database Migration Service",
                "category": "Database Migration",
                "description": "Service to migrate databases to AWS",
                "key_features": [
                    "Minimal downtime migration",
                    "Continuous data replication",
                    "Support for heterogeneous migrations",
                    "Schema conversion tool"
                ],
                "use_cases": [
                    "Database migration to cloud",
                    "Database consolidation",
                    "Continuous replication",
                    "Development and test environments"
                ],
                "pricing": "Pay per replication instance hour"
            },
            "lake-formation": {
                "name": "AWS Lake Formation",
                "category": "Data Lake Management",
                "description": "Service to set up secure data lakes",
                "key_features": [
                    "Centralized permissions",
                    "Data discovery and cataloging",
                    "Row and column-level security",
                    "Audit and compliance"
                ],
                "use_cases": [
                    "Data lake security",
                    "Data governance",
                    "Compliance management",
                    "Access control"
                ],
                "pricing": "No additional charges - pay for underlying services"
            },
            "step-functions": {
                "name": "AWS Step Functions",
                "category": "Workflow Orchestration",
                "description": "Serverless workflow orchestration service",
                "key_features": [
                    "Visual workflow designer",
                    "Error handling and retry logic",
                    "Integration with AWS services",
                    "State management"
                ],
                "use_cases": [
                    "Data processing pipelines",
                    "Microservices orchestration",
                    "ETL workflow management",
                    "Business process automation"
                ],
                "pricing": "Pay per state transition"
            },
            "cloudwatch": {
                "name": "Amazon CloudWatch",
                "category": "Monitoring and Observability",
                "description": "Monitoring service for AWS resources and applications",
                "key_features": [
                    "Metrics collection",
                    "Log aggregation",
                    "Alarms and notifications",
                    "Dashboards",
                    "Custom metrics"
                ],
                "use_cases": [
                    "Infrastructure monitoring",
                    "Application performance monitoring",
                    "Log analysis",
                    "Automated responses"
                ],
                "pricing": "Pay for metrics, logs, and dashboard usage"
            }
        }
        
        service_key = service_name.lower().replace(" ", "-").replace("aws-", "").replace("amazon-", "")
        service_info = services_info.get(service_key)
        
        if not service_info:
            available_services = list(services_info.keys())
            return f"Service '{service_name}' not found. Available services: {', '.join(available_services)}"
        
        info = f"""**{service_info['name']}**
*Category: {service_info['category']}*

**Description:**
{service_info['description']}

**Key Features:**
{chr(10).join(f"• {feature}" for feature in service_info['key_features'])}

**Common Use Cases:**
{chr(10).join(f"• {use_case}" for use_case in service_info['use_cases'])}

**Pricing Model:**
{service_info['pricing']}
"""
        
        return info
        
    except Exception as e:
        return f"Error retrieving AWS service information: {str(e)}"


@tool
def aws_best_practices_tool(domain: str) -> str:
    """
    Retrieves best practices for AWS data engineering in specific domains.
    
    Args:
        domain: Domain area (ingestion, storage, security, operations)
        
    Returns:
        Best practices and recommendations for the specified domain
    """
    try:
        best_practices = {
            "ingestion": {
                "title": "Data Ingestion Best Practices",
                "practices": [
                    "Choose the right ingestion pattern (batch vs streaming vs micro-batch)",
                    "Implement proper error handling and retry mechanisms",
                    "Use compression to reduce data transfer costs",
                    "Implement data validation at ingestion points",
                    "Consider data partitioning strategies early",
                    "Use AWS Glue for schema evolution and discovery",
                    "Implement monitoring and alerting for data pipelines",
                    "Use Kinesis for real-time streaming requirements",
                    "Consider DMS for database migration scenarios",
                    "Implement proper data lineage tracking"
                ]
            },
            "storage": {
                "title": "Data Storage Best Practices",
                "practices": [
                    "Design your data lake with proper folder structure",
                    "Use appropriate S3 storage classes for cost optimization",
                    "Implement data lifecycle policies",
                    "Use columnar formats (Parquet, ORC) for analytics workloads",
                    "Partition data appropriately for query performance",
                    "Enable S3 versioning for critical data",
                    "Use Redshift for structured analytics workloads",
                    "Consider DynamoDB for high-performance NoSQL needs",
                    "Implement proper backup and disaster recovery",
                    "Use data compression to reduce storage costs"
                ]
            },
            "security": {
                "title": "Data Security Best Practices",
                "practices": [
                    "Implement least privilege access principles",
                    "Use AWS Lake Formation for centralized permissions",
                    "Enable encryption at rest and in transit",
                    "Implement row and column-level security",
                    "Use IAM roles instead of users for applications",
                    "Enable CloudTrail for audit logging",
                    "Implement data masking for sensitive information",
                    "Use VPC endpoints for secure service access",
                    "Regularly review and rotate access keys",
                    "Implement data classification and tagging"
                ]
            },
            "operations": {
                "title": "Data Operations Best Practices",
                "practices": [
                    "Implement comprehensive monitoring and alerting",
                    "Use Step Functions for workflow orchestration",
                    "Implement proper error handling and recovery",
                    "Set up automated testing for data pipelines",
                    "Use Infrastructure as Code (CloudFormation/CDK)",
                    "Implement cost monitoring and optimization",
                    "Set up proper logging and observability",
                    "Use tags for resource organization and cost allocation",
                    "Implement automated backup and recovery procedures",
                    "Plan for scalability and performance optimization"
                ]
            }
        }
        
        domain_key = domain.lower()
        if domain_key not in best_practices:
            available_domains = list(best_practices.keys())
            return f"Domain '{domain}' not found. Available domains: {', '.join(available_domains)}"
        
        practices = best_practices[domain_key]
        
        result = f"**{practices['title']}**\n\n"
        result += '\n'.join(f"{i+1}. {practice}" for i, practice in enumerate(practices['practices']))
        
        return result
        
    except Exception as e:
        return f"Error retrieving best practices: {str(e)}"


@tool
def aws_architecture_patterns_tool(pattern_type: str) -> str:
    """
    Provides common AWS architecture patterns for data engineering.
    
    Args:
        pattern_type: Type of pattern (data-lake, real-time, batch-processing, etc.)
        
    Returns:
        Architecture pattern description with components and flow
    """
    try:
        patterns = {
            "data-lake": {
                "name": "Modern Data Lake Architecture",
                "description": "Scalable data lake architecture using AWS services",
                "components": [
                    "S3 as the central data store",
                    "AWS Glue for ETL and data catalog",
                    "Lake Formation for security and governance",
                    "Athena for ad-hoc querying",
                    "Redshift for data warehousing",
                    "QuickSight for visualization"
                ],
                "flow": [
                    "Data ingestion from various sources to S3",
                    "Glue crawlers discover and catalog data",
                    "ETL jobs transform and prepare data",
                    "Lake Formation manages access and security",
                    "Analytics tools query processed data"
                ]
            },
            "real-time": {
                "name": "Real-time Data Processing Architecture",
                "description": "Architecture for processing streaming data in real-time",
                "components": [
                    "Kinesis Data Streams for data ingestion",
                    "Kinesis Analytics for stream processing",
                    "Lambda for event-driven processing",
                    "DynamoDB for low-latency storage",
                    "ElastiCache for caching",
                    "CloudWatch for monitoring"
                ],
                "flow": [
                    "Streaming data ingested via Kinesis",
                    "Real-time processing with Analytics/Lambda",
                    "Results stored in DynamoDB or S3",
                    "Dashboards show real-time insights"
                ]
            },
            "batch-processing": {
                "name": "Batch Data Processing Architecture",
                "description": "Architecture for large-scale batch data processing",
                "components": [
                    "S3 for data storage",
                    "EMR or Glue for batch processing",
                    "Step Functions for orchestration",
                    "CloudWatch for monitoring",
                    "SNS for notifications",
                    "Redshift for analytics"
                ],
                "flow": [
                    "Data lands in S3 from various sources",
                    "Step Functions orchestrate processing jobs",
                    "EMR/Glue processes data in batches",
                    "Processed data stored for analytics",
                    "Notifications sent on completion/failure"
                ]
            },
            "hybrid": {
                "name": "Hybrid Batch and Stream Processing",
                "description": "Lambda architecture combining batch and stream processing",
                "components": [
                    "Kinesis for streaming data",
                    "S3 for batch data storage",
                    "Lambda for stream processing",
                    "Glue/EMR for batch processing",
                    "DynamoDB for serving layer",
                    "API Gateway for data access"
                ],
                "flow": [
                    "Data flows through both batch and stream paths",
                    "Stream processing provides real-time views",
                    "Batch processing provides comprehensive views",
                    "Results merged in serving layer"
                ]
            }
        }
        
        pattern_key = pattern_type.lower().replace("-", "-").replace("_", "-")
        pattern = patterns.get(pattern_key)
        
        if not pattern:
            available_patterns = list(patterns.keys())
            return f"Pattern '{pattern_type}' not found. Available patterns: {', '.join(available_patterns)}"
        
        result = f"**{pattern['name']}**\n\n"
        result += f"**Description:**\n{pattern['description']}\n\n"
        result += f"**Key Components:**\n"
        result += '\n'.join(f"• {component}" for component in pattern['components'])
        result += f"\n\n**Data Flow:**\n"
        result += '\n'.join(f"{i+1}. {step}" for i, step in enumerate(pattern['flow']))
        
        return result
        
    except Exception as e:
        return f"Error retrieving architecture pattern: {str(e)}"


@tool
def aws_cost_optimization_tool(service: str = "") -> str:
    """
    Provides cost optimization recommendations for AWS data services.
    
    Args:
        service: Specific service to optimize (optional)
        
    Returns:
        Cost optimization recommendations
    """
    try:
        cost_tips = {
            "general": [
                "Use appropriate storage classes (IA, Glacier) for infrequently accessed data",
                "Implement data lifecycle policies to automatically transition data",
                "Right-size your compute resources based on actual usage",
                "Use Spot instances for fault-tolerant batch processing",
                "Enable compression to reduce storage and transfer costs",
                "Monitor and set up billing alerts",
                "Use Reserved Instances for predictable workloads",
                "Clean up unused resources regularly"
            ],
            "s3": [
                "Use S3 Intelligent-Tiering for automatic cost optimization",
                "Implement lifecycle policies to move data to cheaper storage classes",
                "Use S3 Storage Class Analysis to understand access patterns",
                "Enable S3 Transfer Acceleration only when needed",
                "Use multipart uploads for large files",
                "Delete incomplete multipart uploads",
                "Use S3 Inventory to identify optimization opportunities"
            ],
            "redshift": [
                "Use Reserved Instances for long-running clusters",
                "Implement automatic pause/resume for dev/test clusters",
                "Use Redshift Spectrum for infrequently queried data",
                "Optimize table design with proper distribution and sort keys",
                "Use compression to reduce storage costs",
                "Monitor query performance and optimize expensive queries",
                "Consider Redshift Serverless for variable workloads"
            ],
            "glue": [
                "Use appropriate worker types (G.1X, G.2X) based on job requirements",
                "Optimize job bookmarks to avoid reprocessing data",
                "Use Glue triggers efficiently to avoid unnecessary runs",
                "Monitor job metrics to identify optimization opportunities",
                "Use pushdown predicates to reduce data processing",
                "Consider using Glue DataBrew for simple transformations"
            ],
            "kinesis": [
                "Right-size the number of shards based on throughput requirements",
                "Use Kinesis Data Firehose for simple delivery scenarios",
                "Implement proper record aggregation to maximize throughput",
                "Monitor shard utilization and scale appropriately",
                "Use compression for data records",
                "Consider Kinesis Analytics for stream processing vs Lambda"
            ]
        }
        
        if service:
            service_key = service.lower()
            if service_key in cost_tips:
                tips = cost_tips[service_key]
                result = f"**Cost Optimization Tips for {service.upper()}:**\n\n"
                result += '\n'.join(f"• {tip}" for tip in tips)
                return result
            else:
                available_services = [k for k in cost_tips.keys() if k != "general"]
                return f"Service '{service}' not found. Available services: {', '.join(available_services)}"
        else:
            # Return general tips
            result = "**General AWS Cost Optimization Tips:**\n\n"
            result += '\n'.join(f"• {tip}" for tip in cost_tips["general"])
            result += f"\n\n**Available service-specific tips:** {', '.join([k for k in cost_tips.keys() if k != 'general'])}"
            return result
            
    except Exception as e:
        return f"Error retrieving cost optimization tips: {str(e)}"
