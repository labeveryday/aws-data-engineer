# AWS Data Engineer Interactive Course

An interactive Streamlit application for AWS Certified Data Engineer - Associate exam preparation.

## Local Development with Docker

### Prerequisites
- Docker and Docker Compose
- AWS credentials configured locally (for Claude integration in later phases)

### Running Locally
1. Build and start the Docker container:
   ```bash
   docker-compose up --build
   ```

2. Open http://localhost:8501 in your browser

3. To stop the application:
   ```bash
   docker-compose down
   ```

## Project Structure

```
docker-app/
├── app/                  # Application code
│   ├── main.py           # Main Streamlit application
│   ├── config.py         # Configuration settings
│   └── utils/            # Utility functions
│       └── bedrock_client.py  # Amazon Bedrock client (placeholder)
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Features

- **Study Materials**: Comprehensive guides covering all exam domains
- **Hands-on Labs**: Step-by-step instructions for practical experience
- **Navigation**: Easy access to all content through the sidebar
- **Coming Soon**: Claude AI assistant integration, progress tracking, and interactive elements

## Development Phases

This application is being developed in phases:

- **Phase 1**: Basic setup with Docker and content navigation (current)
- **Phase 2**: Core Streamlit app with progress tracking
- **Phase 3**: Claude on Amazon Bedrock integration
- **Phase 4**: Interactive lab features
- **Phase 5**: Testing and refinement
- **Phase 6**: Documentation and deployment instructions

## AWS Credentials (for future phases)

For Claude integration (coming in Phase 3), you'll need AWS credentials with access to Amazon Bedrock.
Configure your credentials using:

```bash
aws configure
```

## Notes

- This is the initial implementation (Phase 1)
- Claude integration is currently a placeholder and will be implemented in Phase 3
