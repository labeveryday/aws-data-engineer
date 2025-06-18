# AWS Data Engineer Interactive Course

An interactive application for AWS Certified Data Engineer - Associate (DEA-C01) exam preparation, combining comprehensive study materials with hands-on labs and progress tracking.

## What This App Does

This application provides a structured learning environment for AWS Certified Data Engineer - Associate exam preparation:

- **Interactive Study Materials**: Access comprehensive guides covering all exam domains
- **Hands-on Labs**: Follow step-by-step instructions for practical experience with AWS data services
- **Progress Tracking**: Monitor your advancement through the course materials
- **Visual Dashboard**: See your progress and continue where you left off
- **Coming Soon**: Claude AI assistant integration for interactive Q&A and guidance

## How to Use the App

### Prerequisites
- Docker and Docker Compose installed on your system
- AWS credentials configured locally (for Claude integration in later phases)

### Getting Started
1. Clone this repository:
   ```bash
   git clone https://github.com/labeveryday/aws-data-engineer
   cd aws-data-engineer
   ```

2. Build and start the Docker container:
   ```bash
   cd docker-app
   docker-compose up --build
   ```

3. Open http://localhost:8501 in your browser to access the application

4. To stop the application:
   ```bash
   docker-compose down
   ```

### Navigation
- Use the sidebar to navigate between different sections of the course
- Track your progress through the checkboxes in each section
- View your overall progress in the dashboard

## Implementation Status

The application is being developed in phases:

- **Phase 1**: ✅ Basic setup with Docker and content navigation
- **Phase 2**: ✅ Core Streamlit app with progress tracking
- **Phase 3**: 🔄 Claude on Amazon Bedrock integration (In Progress)
- **Phase 4**: ⏳ Interactive lab features (Planned)
- **Phase 5**: ⏳ Testing and refinement (Planned)
- **Phase 6**: ⏳ Documentation and deployment instructions (Planned)

## What's Next

We're currently working on Phase 3, which includes:
- Integration with Claude on Amazon Bedrock for AI-assisted learning
- Interactive Q&A capabilities based on study materials
- Contextual assistance for labs and exercises

## Repository Structure

```
aws-data-engineer/
├── docker-app/            # Streamlit application with Docker configuration
├── study-guide/           # Comprehensive study materials by domain
├── labs/                  # Hands-on lab instructions and resources
└── AWS-Certified-Data-Engineer-Associate_Exam-Guide.pdf  # Official exam guide
```

## Study Materials

The study materials are organized by exam domains:

1. **Data Ingestion and Transformation (30-35%)**
2. **Storage and Data Management (30-35%)**
3. **Data Security and Access Control (15-20%)**
4. **Data Operations and Optimization (15-20%)**

## Hands-on Labs

Practical exercises are organized into categories matching the exam domains:
- Data Ingestion labs (Glue, Kinesis, DMS)
- Data Storage labs (S3, Redshift, DynamoDB)
- Data Transformation labs (ETL, Stream Processing, Data Quality)
- Security and Governance labs (Lake Formation, Column Security)
- Operations and Optimization labs (Step Functions, Monitoring)

## About the AWS Certified Data Engineer - Associate Exam

The AWS Certified Data Engineer - Associate exam validates your technical expertise in designing, building, securing, and maintaining analytics solutions on AWS. It focuses on data ingestion, storage, processing, and security using AWS services like Glue, Kinesis, Redshift, Lake Formation, and more.

### Exam Details
- **Format**: Multiple choice and multiple answer questions
- **Duration**: 130 minutes
- **Cost**: $150 USD
- **Passing Score**: 750/1000
- **Delivery Method**: Testing center or online proctored exam

## Contributing

Contributions to improve the application or study materials are welcome. Please feel free to submit pull requests or open issues for any bugs or enhancement suggestions.

## License

[Specify your license information here]
