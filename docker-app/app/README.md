# AWS Data Engineer Course - Phase Two Implementation

This directory contains the Phase Two implementation of the AWS Data Engineer interactive course application, focusing on Claude integration using Strands Agents for multi-agent collaboration.

## Overview

Phase Two extends the application with an intelligent assistant system that uses multiple specialized AI agents to provide contextual help and answer questions about AWS data engineering concepts.

## Key Features

- **Multi-Agent Architecture**: A team of specialized agents working together to provide comprehensive assistance
- **Content-Aware Responses**: Agents have access to study materials and can provide contextual information
- **Progress Integration**: Assistant is aware of user progress and can provide personalized recommendations
- **AWS Documentation Access**: Integration with AWS documentation for up-to-date information
- **Interactive Chat Interface**: Streamlit-based chat interface for interacting with the agents

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

## Implementation Plan

The Phase Two implementation follows this plan:

1. **Setup Environment (Days 1-2)**
   - Install Strands Agents and dependencies
   - Configure AWS credentials for Bedrock access
   - Set up basic agent structure

2. **Implement Agents (Days 3-5)**
   - Create coordinator agent
   - Implement specialist agents
   - Define system prompts and routing logic

3. **Develop Custom Tools (Days 6-8)**
   - Create content retrieval tools
   - Implement progress tracking tools
   - Set up AWS documentation tools

4. **Integrate with Streamlit (Days 9-10)**
   - Build chat interface
   - Connect agents to UI
   - Implement streaming responses

5. **Testing and Refinement (Days 11-12)**
   - Test with various questions
   - Refine agent prompts
   - Optimize performance

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

The multi-agent system can be accessed through the chat interface in the application. Users can ask questions about:

- AWS data engineering concepts
- Specific AWS services
- Best practices and recommendations
- Lab instructions and guidance
- Their progress through the course

## Dependencies

- Python 3.9+
- strands-agents>=0.1.0
- strands-agents-tools>=0.1.0
- boto3>=1.28.0
- streamlit>=1.22.0
- mcp (Model Context Protocol)

## Next Steps

After completing Phase Two:
- Enhance agent capabilities with more specialized knowledge
- Implement conversation memory for better follow-up questions
- Add more interactive features like code execution
- Integrate with AWS services for real-time demonstrations
