# Multi-Agent Collaboration System for AWS Data Engineer Course

This directory contains the implementation of a multi-agent collaboration system using Strands Agents to provide interactive assistance for the AWS Data Engineer certification course.

## Architecture Overview

The system uses a team of specialized agents coordinated by a main agent:

1. **Coordinator Agent**: The main interface that routes questions and synthesizes responses
2. **Domain-Specific Agents**:
   - **Data Ingestion Agent**: Expert in AWS data ingestion services (Kinesis, Glue, DMS)
   - **Storage Agent**: Specialist in AWS storage solutions (S3, Redshift, DynamoDB)
   - **Security Agent**: Focused on AWS data security and governance (IAM, Lake Formation)
   - **Operations Agent**: Handles optimization and monitoring (CloudWatch, Step Functions)

## File Structure

```
agents/
├── __init__.py             # Exports the main coordinator agent
├── coordinator.py          # Main agent that coordinates others
├── ingestion_agent.py      # Data ingestion specialist
├── storage_agent.py        # Storage solutions specialist
├── security_agent.py       # Security and governance specialist
├── operations_agent.py     # Operations and optimization specialist
└── README.md               # This file
```

## Implementation Plan

### Phase 1: Setup and Basic Implementation (1-2 days)

1. **Environment Setup**
   - Install required packages: `strands-agents`, `strands-agents-tools`
   - Configure AWS credentials for Bedrock access

2. **Create Agent Files**
   - Implement basic versions of all agent files
   - Define system prompts for each specialist agent
   - Create the coordinator agent with routing logic

3. **Basic Integration**
   - Connect agents to the Streamlit app
   - Implement simple chat interface

### Phase 2: Custom Tools Development (2-3 days)

1. **Content Retrieval Tool**
   - Create tool to access study materials
   - Implement context-aware retrieval from markdown files

2. **Progress Tracking Tool**
   - Create tool to update and retrieve user progress
   - Integrate with existing progress tracking system

3. **AWS Documentation Tool**
   - Implement tool to fetch AWS documentation
   - Use AWS Documentation MCP server

### Phase 3: Advanced Agent Coordination (2-3 days)

1. **Implement Sophisticated Routing**
   - Create logic to determine which agent(s) should handle each question
   - Implement confidence scoring for agent responses

2. **Response Synthesis**
   - Develop methods to combine responses from multiple agents
   - Ensure coherent, non-repetitive final responses

3. **Conversation Context Management**
   - Maintain conversation history
   - Provide context to agents for follow-up questions

### Phase 4: Integration and Testing (2-3 days)

1. **Streamlit Integration**
   - Create chat interface components
   - Implement streaming responses
   - Add agent selection UI (optional)

2. **Testing and Refinement**
   - Test with various AWS data engineering questions
   - Refine agent prompts and routing logic
   - Optimize response times

3. **Documentation**
   - Update documentation with usage instructions
   - Document agent capabilities and limitations

## Usage

The multi-agent system can be accessed through the main coordinator:

```python
from app.agents import coordinator

# Get a response from the appropriate specialist agent(s)
response = coordinator("How does AWS Kinesis integrate with Glue for real-time ETL?")
```

## Dependencies

- Python 3.9+
- strands-agents>=0.1.0
- strands-agents-tools>=0.1.0
- boto3
- streamlit

## AWS Configuration

The agents require access to Amazon Bedrock for Claude models. Ensure your AWS credentials are properly configured with permissions for:

- Amazon Bedrock (Claude 3.7 Sonnet)
- Amazon S3 (for storing conversation history, optional)
- AWS Documentation MCP server (for documentation retrieval)
