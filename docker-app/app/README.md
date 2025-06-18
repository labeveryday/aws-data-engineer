# AWS Data Engineer Course - Phase Two & Three Implementation

This directory contains the Phase Two and Three implementation of the AWS Data Engineer interactive course application, featuring a complete multi-agent AI assistant system using Claude on Amazon Bedrock.

## Overview

Phase Two and Three extend the application with an intelligent assistant system that uses multiple specialized AI agents working together to provide comprehensive assistance for AWS data engineering concepts.

## Key Features

- **Multi-Agent Architecture**: A team of specialized agents working together to provide comprehensive assistance
- **Content-Aware Responses**: Agents have access to study materials and can provide contextual information
- **Progress Integration**: Assistant is aware of user progress and can provide personalized recommendations
- **AWS Documentation Access**: Integration with AWS documentation for up-to-date information
- **Interactive Chat Interface**: Streamlit-based chat interface for interacting with the agents
- **Specialized Domain Expertise**: Each agent focuses on specific AWS data engineering domains

## Directory Structure

```
app/
├── main.py                # Main Streamlit application
├── config.py              # Configuration settings
├── pages/                 # Additional pages
│   └── dashboard.py       # Progress dashboard
├── components/            # Reusable UI components
│   └── chat_interface.py  # Chat interface for agent interaction
├── agents/                # Multi-agent system implementation
│   ├── coordinator.py     # Main coordinator agent
│   ├── ingestion_agent.py # Data ingestion specialist
│   ├── storage_agent.py   # Storage specialist
│   ├── security_agent.py  # Security specialist
│   └── operations_agent.py # Operations specialist
├── tools/                 # Custom tools for agents
│   ├── content_tools.py   # Tools for accessing study materials
│   ├── progress_tools.py  # Tools for tracking user progress
│   └── aws_tools.py       # Tools for AWS service information
└── utils/                 # Utility functions
    ├── bedrock_client.py  # Amazon Bedrock client
    └── progress_tracker.py # Progress tracking utility
```

## Implementation Status

The Phase Two and Three implementation is now complete with:

1. **✅ Multi-Agent System**
   - Coordinator agent with intelligent question routing
   - 4 specialist agents (Data Ingestion, Storage, Security, Operations)
   - Each agent has domain-specific expertise and system prompts

2. **✅ Custom Tools**
   - Content retrieval and search tools
   - Progress tracking and recommendation tools
   - AWS service information and best practices tools

3. **✅ Streamlit Integration**
   - Chat interface components (embedded and dedicated page)
   - Sidebar integration with existing progress tracking
   - Quick action buttons for common questions
   - Conversation context management

4. **✅ Amazon Bedrock Integration**
   - Claude 3 Sonnet model integration
   - Proper AWS credentials handling
   - Error handling and fallback mechanisms

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure AWS credentials:
   ```bash
   aws configure
   ```

3. Run the application:
   ```bash
   cd docker-app
   docker-compose up --build
   ```

4. Open http://localhost:8501 in your browser

## Usage

The multi-agent system can be accessed through:

1. **Embedded Chat**: Available on the main page and study sections
2. **Dedicated Chat Page**: Full-featured chat interface with quick actions
3. **Sidebar Integration**: Progress tracking and agent capabilities

Users can ask questions about:
- AWS data engineering concepts and services
- Specific AWS service configurations and best practices
- Study guidance and personalized recommendations
- Lab instructions and hands-on guidance
- Architecture patterns and cost optimization
- Their progress through the course

## Dependencies

- Python 3.11+
- strands-agents>=0.1.0
- strands-agents-tools>=0.1.0
- boto3>=1.28.0
- streamlit>=1.22.0
- mcp (Model Context Protocol)

## Next Steps

Phase Four will focus on:
- Frontend/Backend separation
- CloudScape design system implementation
- RESTful API backend for the multi-agent system
- Enhanced user experience with modern UI components
