# Domain 3: Data Security and Access Control (15-20%)

## Domain Overview

The Data Security and Access Control domain focuses on implementing security measures to protect data at rest and in transit, managing access to data resources, and ensuring compliance with security requirements. This domain covers how to encrypt data, implement access controls, and monitor data access patterns. As this domain represents 15-20% of the exam, it's important to understand AWS security services, encryption mechanisms, and access control strategies for data services.

## Key Concepts

- **Encryption** at rest and in transit
- **Key management** and rotation
- **Identity and access management**
- **Fine-grained access control**
- **Network security** for data services
- **Data masking** and **anonymization**
- **Audit logging** and **compliance**
- **Cross-account access** patterns

## Task Statement 3.1: Implement data encryption and protection

### Description

This task involves implementing encryption and data protection mechanisms to secure data at rest and in transit. You need to understand different encryption options, key management strategies, and data protection techniques for various AWS data services.

### Key Knowledge Areas

#### Encryption Fundamentals

1. **Encryption Types**
   - Symmetric encryption
   - Asymmetric encryption
   - Envelope encryption
   - Client-side encryption
   - Server-side encryption

2. **Encryption Contexts**
   - Data at rest
   - Data in transit
   - Data in use
   - Key considerations for each context

3. **Key Management**
   - Key generation
   - Key storage
   - Key rotation
   - Key access control
   - Key backup and recovery

4. **Encryption Algorithms**
   - AES (Advanced Encryption Standard)
   - RSA (Rivest–Shamir–Adleman)
   - ECC (Elliptic Curve Cryptography)
   - Algorithm selection considerations

#### AWS Encryption Services

1. **AWS Key Management Service (KMS)**
   - Customer master keys (CMKs)
   - Key policies
   - Key rotation
   - Multi-region keys
   - Custom key stores

2. **AWS CloudHSM**
   - Hardware security modules
   - FIPS 140-2 Level 3 compliance
   - Direct control of keys
   - Integration with KMS
   - Use cases vs. KMS

3. **AWS Certificate Manager (ACM)**
   - SSL/TLS certificate management
   - Public and private certificates
   - Certificate renewal
   - Integration with AWS services
   - Certificate validation

4. **AWS Secrets Manager**
   - Secret storage and management
   - Automatic secret rotation
   - Fine-grained access control
   - Integration with AWS services
   - Auditing and monitoring

#### Encryption in AWS Data Services

1. **Amazon S3 Encryption**
   - Server-side encryption options:
     - SSE-S3 (S3-managed keys)
     - SSE-KMS (KMS-managed keys)
     - SSE-C (Customer-provided keys)
   - Client-side encryption
   - Default encryption
   - Bucket policies for encryption

2. **Amazon RDS/Aurora Encryption**
   - Encryption at rest
   - TLS for connections
   - Transparent Data Encryption (TDE)
   - Key management
   - Performance considerations

3. **Amazon Redshift Encryption**
   - Cluster encryption
   - Database encryption
   - Load/unload encryption
   - Key rotation
   - HSM integration

4. **Amazon DynamoDB Encryption**
   - Table encryption
   - DAX encryption
   - Backup encryption
   - Client-side encryption libraries
   - Key management

5. **AWS Glue Encryption**
   - Data catalog encryption
   - ETL job bookmarks encryption
   - Connection password encryption
   - S3 encryption settings
   - CloudWatch log encryption

6. **Amazon Kinesis Encryption**
   - Server-side encryption
   - KMS integration
   - Producer/consumer encryption
   - Key management
   - Performance considerations

#### Data Protection Techniques

1. **Data Loss Prevention (DLP)**
   - Sensitive data discovery
   - Content inspection
   - Policy enforcement
   - Remediation actions
   - Monitoring and alerting

2. **Data Masking**
   - Dynamic data masking
   - Static data masking
   - Format-preserving masking
   - Tokenization
   - Redaction

3. **Data Anonymization**
   - Pseudonymization
   - Generalization
   - Perturbation
   - k-anonymity
   - Differential privacy

4. **Secure Data Sharing**
   - Cross-account access
   - Temporary credentials
   - Pre-signed URLs
   - VPC endpoints
   - Private connections

### Best Practices

1. **Encrypt sensitive data** at rest and in transit
2. **Use appropriate key management** based on security requirements
3. **Implement key rotation** for long-term data protection
4. **Document encryption requirements** and implementations
5. **Use envelope encryption** for large datasets
6. **Implement defense in depth** with multiple security controls
7. **Regularly audit encryption configurations** and key access
8. **Consider performance implications** of encryption options

### AWS Services to Focus On

- AWS Key Management Service (KMS)
- AWS CloudHSM
- AWS Certificate Manager
- AWS Secrets Manager
- Encryption features of data services (S3, RDS, Redshift, DynamoDB, etc.)

### Related Labs

- [Lab 4.1: Data Governance with AWS Lake Formation](../labs/security-governance/lab-4.1-lake-formation.md) (includes encryption)
- [Lab 4.2: Column-Level Security](../labs/security-governance/lab-4.2-column-security.md) (includes data protection)

### References

- [AWS Encryption and PKI Services](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/security-services.html#encryption-and-pki)
- [AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
- [Protecting Data Using Encryption in Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingEncryption.html)
- [Encryption in Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html)
- [Amazon Redshift Database Encryption](https://docs.aws.amazon.com/redshift/latest/mgmt/working-with-db-encryption.html)
- [Encryption at Rest in Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/EncryptionAtRest.html)

## Task Statement 3.2: Implement access control for data

### Description

This task involves implementing access control mechanisms to secure data resources. You need to understand different access control models, permission management strategies, and authentication mechanisms for various AWS data services.

### Key Knowledge Areas

#### Access Control Fundamentals

1. **Access Control Models**
   - Discretionary Access Control (DAC)
   - Mandatory Access Control (MAC)
   - Role-Based Access Control (RBAC)
   - Attribute-Based Access Control (ABAC)
   - Policy-Based Access Control

2. **Authentication vs. Authorization**
   - Authentication methods
   - Authorization mechanisms
   - Multi-factor authentication
   - Federation and single sign-on
   - Temporary credentials

3. **Principle of Least Privilege**
   - Minimum necessary permissions
   - Just-in-time access
   - Permission boundaries
   - Privilege escalation prevention
   - Regular access reviews

4. **Access Control Granularity**
   - Resource-level access
   - Action-level access
   - Attribute-level access
   - Row-level access
   - Column-level access

#### AWS Identity and Access Management (IAM)

1. **IAM Components**
   - Users
   - Groups
   - Roles
   - Policies
   - Identity providers

2. **IAM Policies**
   - Identity-based policies
   - Resource-based policies
   - Permission boundaries
   - Service control policies
   - Session policies

3. **IAM Policy Evaluation Logic**
   - Policy evaluation order
   - Explicit deny
   - Default deny
   - Policy conditions
   - Policy variables

4. **IAM Best Practices**
   - Root account protection
   - MFA enforcement
   - Least privilege principle
   - Regular credential rotation
   - Access key management

#### Access Control in AWS Data Services

1. **Amazon S3 Access Control**
   - Bucket policies
   - Access Control Lists (ACLs)
   - S3 Block Public Access
   - Presigned URLs
   - VPC endpoints

2. **AWS Lake Formation**
   - Database, table, and column-level permissions
   - Tag-based access control
   - Cross-account access
   - Data location registration
   - Integration with IAM

3. **Amazon Redshift Access Control**
   - Database users and groups
   - Schema-level permissions
   - Table and column-level permissions
   - Stored procedure execution
   - Row-level security

4. **Amazon RDS/Aurora Access Control**
   - Database authentication
   - IAM database authentication
   - Master user management
   - Database user permissions
   - Proxy authentication

5. **Amazon DynamoDB Access Control**
   - Table-level permissions
   - Item-level permissions
   - Attribute-level permissions
   - Condition expressions
   - Fine-grained access control

6. **AWS Glue Access Control**
   - Resource-level permissions
   - Tag-based access control
   - Lake Formation integration
   - Cross-account access
   - Service role permissions

#### Fine-Grained Access Control

1. **Column-Level Security**
   - Lake Formation column permissions
   - Redshift column-level grants
   - View-based access control
   - Dynamic data masking
   - Column filtering

2. **Row-Level Security**
   - Lake Formation row filters
   - Redshift row-level security
   - RDS/Aurora row-level security
   - Policy-based filtering
   - Query rewriting

3. **Cell-Level Security**
   - Combined row and column restrictions
   - Dynamic data masking
   - Value-based filtering
   - Attribute-based access control
   - Data transformation

4. **Tag-Based Access Control**
   - LF-Tags in Lake Formation
   - Resource tagging
   - Tag-based IAM policies
   - Tag enforcement
   - Tag propagation

#### Cross-Account Access Patterns

1. **Resource-Based Policies**
   - S3 bucket policies
   - KMS key policies
   - SNS topic policies
   - SQS queue policies
   - Lambda resource policies

2. **IAM Roles**
   - Cross-account role assumption
   - External ID usage
   - Role chaining
   - Role session policies
   - Role trust relationships

3. **AWS Resource Access Manager (RAM)**
   - Resource sharing
   - Principal-based sharing
   - Permission management
   - Shared resource access
   - Sharing with AWS Organizations

4. **Lake Formation Cross-Account Access**
   - Resource links
   - Cross-account grants
   - Named resource method
   - LF-Tag method
   - Cross-account data catalog access

### Best Practices

1. **Implement least privilege** for all data access
2. **Use IAM roles** instead of IAM users for applications
3. **Implement fine-grained access control** for sensitive data
4. **Regularly review and audit** access permissions
5. **Use temporary credentials** when possible
6. **Implement attribute-based access control** for scalable permissions
7. **Document access control requirements** and implementations
8. **Use service-specific access controls** in addition to IAM

### AWS Services to Focus On

- AWS Identity and Access Management (IAM)
- AWS Lake Formation
- Amazon S3 access control features
- Access control features of database services (Redshift, RDS, DynamoDB)
- AWS Resource Access Manager (RAM)

### Related Labs

- [Lab 4.1: Data Governance with AWS Lake Formation](../labs/security-governance/lab-4.1-lake-formation.md)
- [Lab 4.2: Column-Level Security](../labs/security-governance/lab-4.2-column-security.md)
- [Lab 4.3: Cross-Account Data Sharing](../labs/security-governance/lab-4.3-cross-account.md)

### References

- [AWS Identity and Access Management User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [AWS Lake Formation Developer Guide](https://docs.aws.amazon.com/lake-formation/latest/dg/what-is-lake-formation.html)
- [Amazon S3 Access Control](https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-access-control.html)
- [Amazon Redshift Database Developer Guide - Managing Database Security](https://docs.aws.amazon.com/redshift/latest/dg/r_Database_objects.html)
- [Fine-Grained Access Control in Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/specifying-conditions.html)
- [AWS Resource Access Manager User Guide](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html)

## Task Statement 3.3: Implement network security for data services

### Description

This task involves implementing network security measures to protect data services and control data access over the network. You need to understand different network security controls, VPC configurations, and connectivity options for AWS data services.

### Key Knowledge Areas

#### Network Security Fundamentals

1. **Defense in Depth**
   - Multiple security layers
   - Complementary controls
   - Redundant protections
   - Comprehensive security strategy
   - Failure resilience

2. **Network Segmentation**
   - Security zones
   - Network isolation
   - Micro-segmentation
   - Traffic control
   - Blast radius limitation

3. **Secure Network Architecture**
   - Perimeter security
   - Zero trust architecture
   - Least privilege networking
   - Traffic filtering
   - Secure connectivity

4. **Network Monitoring**
   - Traffic analysis
   - Intrusion detection
   - Anomaly detection
   - Flow logging
   - Security analytics

#### AWS Virtual Private Cloud (VPC)

1. **VPC Components**
   - Subnets
   - Route tables
   - Internet gateways
   - NAT gateways
   - Security groups and NACLs

2. **VPC Design for Data Services**
   - Public vs. private subnets
   - Multi-AZ deployment
   - Subnet sizing
   - CIDR allocation
   - Service placement

3. **Security Groups**
   - Stateful filtering
   - Allow rules only
   - Instance-level security
   - Reference other security groups
   - Default deny

4. **Network ACLs**
   - Stateless filtering
   - Allow and deny rules
   - Subnet-level security
   - Rule evaluation order
   - Ephemeral ports

#### VPC Connectivity Options

1. **VPC Endpoints**
   - Interface endpoints
   - Gateway endpoints
   - Endpoint policies
   - Private connectivity
   - Service integration

2. **AWS PrivateLink**
   - Private connectivity to services
   - Service endpoints
   - Endpoint services
   - Network load balancers
   - Service consumer/provider model

3. **VPC Peering**
   - Direct VPC-to-VPC connectivity
   - Non-transitive peering
   - Inter-region peering
   - Routing configuration
   - Security group referencing

4. **AWS Transit Gateway**
   - Hub-and-spoke connectivity
   - Transitive routing
   - Cross-account sharing
   - Route tables and propagation
   - Multi-region transit

5. **AWS Direct Connect**
   - Dedicated network connection
   - Private virtual interfaces
   - Public virtual interfaces
   - Transit virtual interfaces
   - Direct Connect gateways

#### Network Security for AWS Data Services

1. **Amazon S3 Network Security**
   - VPC endpoints for S3
   - Bucket policies with network conditions
   - Access points with VPC restrictions
   - Interface endpoints vs. gateway endpoints
   - Cross-region access considerations

2. **Amazon RDS/Aurora Network Security**
   - VPC deployment
   - Subnet groups
   - Security groups
   - No public access option
   - Database proxy

3. **Amazon Redshift Network Security**
   - VPC deployment
   - Cluster subnet groups
   - Enhanced VPC routing
   - Publicly accessible option
   - VPC endpoints

4. **Amazon DynamoDB Network Security**
   - VPC endpoints
   - Endpoint policies
   - DAX cluster placement
   - Cross-region replication
   - Global tables networking

5. **AWS Glue Network Security**
   - VPC connectivity
   - Development endpoints in VPC
   - Elastic network interfaces
   - Security groups
   - Connection options

6. **Amazon Kinesis Network Security**
   - VPC endpoints
   - Private connectivity
   - Interface endpoints
   - Security group configuration
   - Cross-account access

#### Network Traffic Encryption

1. **Transport Layer Security (TLS)**
   - Certificate management
   - Protocol versions
   - Cipher suites
   - Perfect forward secrecy
   - Certificate validation

2. **VPN Connections**
   - Site-to-site VPN
   - Client VPN
   - VPN tunnels
   - IKE and IPsec
   - Routing and failover

3. **AWS PrivateLink Encryption**
   - Automatic TLS encryption
   - Service-to-service communication
   - No public internet exposure
   - Simplified certificate management
   - Integration with ACM

### Best Practices

1. **Use private subnets** for data services when possible
2. **Implement VPC endpoints** for AWS service access
3. **Apply least privilege** in security groups and NACLs
4. **Encrypt all network traffic** using TLS
5. **Implement network segmentation** for different data sensitivity levels
6. **Use VPC flow logs** for network monitoring and troubleshooting
7. **Implement defense in depth** with multiple network controls
8. **Regularly audit network configurations** for security gaps

### AWS Services to Focus On

- Amazon VPC
- VPC Endpoints
- AWS PrivateLink
- Security Groups and NACLs
- AWS Direct Connect
- AWS Transit Gateway
- Network security features of data services

### Related Labs

- [Lab 4.1: Data Governance with AWS Lake Formation](../labs/security-governance/lab-4.1-lake-formation.md) (includes network security)
- [Lab 4.3: Cross-Account Data Sharing](../labs/security-governance/lab-4.3-cross-account.md) (includes network considerations)

### References

- [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-endpoints.html)
- [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [Security Best Practices for Your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- [Protecting Data in Transit with Encryption](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/security-services.html)
- [Network-to-Amazon VPC Connectivity Options](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/network-to-amazon-vpc-connectivity-options.html)

## Task Statement 3.4: Monitor and audit data access

### Description

This task involves implementing monitoring and auditing mechanisms to track data access and detect security issues. You need to understand logging, monitoring, and auditing capabilities for AWS data services to ensure compliance and security.

### Key Knowledge Areas

#### Monitoring and Auditing Fundamentals

1. **Monitoring vs. Auditing**
   - Real-time monitoring
   - Historical auditing
   - Proactive vs. reactive approaches
   - Continuous monitoring
   - Compliance auditing

2. **Logging Fundamentals**
   - Log types and formats
   - Log storage and retention
   - Log analysis techniques
   - Log integrity protection
   - Log aggregation

3. **Security Information and Event Management (SIEM)**
   - Log correlation
   - Event detection
   - Incident response
   - Security analytics
   - Threat intelligence

4. **Compliance Requirements**
   - Regulatory frameworks (GDPR, HIPAA, PCI DSS)
   - Industry standards
   - Internal policies
   - Evidence collection
   - Audit trails

#### AWS Monitoring and Auditing Services

1. **AWS CloudTrail**
   - API activity logging
   - Management events
   - Data events
   - Insight events
   - Multi-account logging

2. **Amazon CloudWatch**
   - Metrics collection
   - Logs collection
   - Alarms
   - Dashboards
   - Events and EventBridge

3. **AWS Config**
   - Resource configuration tracking
   - Configuration history
   - Compliance rules
   - Remediation actions
   - Multi-account aggregation

4. **Amazon GuardDuty**
   - Threat detection
   - Continuous monitoring
   - Anomaly detection
   - Integrated intelligence
   - Automated response

5. **Amazon Macie**
   - Sensitive data discovery
   - Data classification
   - PII detection
   - Automated scanning
   - Finding management

6. **AWS Security Hub**
   - Security findings aggregation
   - Compliance standards
   - Security scores
   - Cross-account visibility
   - Integrated insights

#### Monitoring and Auditing AWS Data Services

1. **Amazon S3 Monitoring**
   - Server access logging
   - CloudTrail data events
   - S3 access logs
   - Object-level logging
   - Replication metrics

2. **Amazon RDS/Aurora Monitoring**
   - Database logs
   - Enhanced monitoring
   - Performance Insights
   - Audit logging
   - CloudWatch integration

3. **Amazon Redshift Monitoring**
   - Audit logging
   - Database activity streams
   - Query logging
   - Connection logging
   - User activity tracking

4. **Amazon DynamoDB Monitoring**
   - CloudTrail integration
   - CloudWatch metrics
   - Contributor Insights
   - Stream records
   - Point-in-time recovery

5. **AWS Glue Monitoring**
   - Job run monitoring
   - Data Catalog activity
   - ETL metrics
   - Visual job monitoring
   - CloudWatch integration

6. **Amazon Kinesis Monitoring**
   - Stream monitoring
   - Shard-level metrics
   - Consumer metrics
   - Enhanced monitoring
   - CloudWatch integration

#### Implementing Monitoring and Auditing

1. **Centralized Logging**
   - Log aggregation
   - Log storage
   - Log analysis
   - Log retention
   - Log protection

2. **Automated Alerting**
   - Threshold-based alerts
   - Anomaly detection
   - Pattern matching
   - Correlation rules
   - Alert prioritization

3. **Access Analysis**
   - Access pattern analysis
   - Unusual activity detection
   - Privilege usage monitoring
   - Cross-account access tracking
   - Service-to-service access

4. **Compliance Reporting**
   - Automated report generation
   - Compliance dashboards
   - Evidence collection
   - Audit preparation
   - Continuous compliance

### Best Practices

1. **Enable comprehensive logging** for all data services
2. **Implement centralized log collection** and analysis
3. **Set up automated alerting** for security events
4. **Establish log retention policies** based on compliance requirements
5. **Regularly review access logs** for unusual patterns
6. **Implement automated compliance checks** with AWS Config
7. **Use CloudTrail for API activity monitoring** across accounts
8. **Protect log integrity** with appropriate controls

### AWS Services to Focus On

- AWS CloudTrail
- Amazon CloudWatch
- AWS Config
- Amazon GuardDuty
- Amazon Macie
- AWS Security Hub
- Logging and monitoring features of data services

### Related Labs

- [Lab 5.2: Monitoring and Alerting](../labs/operations-optimization/lab-5.2-monitoring.md)

### References

- [AWS CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [AWS Config Developer Guide](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)
- [Amazon GuardDuty User Guide](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
- [Amazon Macie User Guide](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [AWS Security Hub User Guide](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html)
- [Logging and Monitoring in Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/dev/logging-with-S3.html)

## Domain 3 Summary

The Data Security and Access Control domain covers the essential skills and knowledge required to secure data resources on AWS. Key takeaways include:

1. **Implementing encryption** for data at rest and in transit using AWS KMS and service-specific encryption features
2. **Designing and implementing access controls** using IAM, Lake Formation, and service-specific mechanisms
3. **Securing network access** to data services using VPC endpoints, security groups, and other network controls
4. **Monitoring and auditing data access** using CloudTrail, CloudWatch, and service-specific logging features

To prepare for this domain:
- Complete the related labs to gain hands-on experience
- Study the AWS documentation for key security services
- Understand the security features of each data service
- Practice implementing defense-in-depth security strategies

Next, we'll explore Domain 4: Data Operations and Optimization.
