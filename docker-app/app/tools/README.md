# Custom Tools for AWS Data Engineer Agents

This directory contains custom tools that extend the capabilities of the Strands Agents used in the AWS Data Engineer course application.

## Tool Overview

The tools in this directory provide specialized functionality for the multi-agent system:

1. **Content Tools**: Access and retrieve information from study materials
2. **Progress Tools**: Track and update user progress through the course
3. **AWS Tools**: Fetch and process AWS documentation and service information

## File Structure

```
tools/
├── __init__.py           # Exports all tools
├── content_tools.py      # Tools for accessing study materials
├── progress_tools.py     # Tools for tracking user progress
├── aws_tools.py          # Tools for AWS service information
└── README.md             # This file
```

## Implementation Details

### Content Tools

The `content_tools.py` file implements tools for accessing and retrieving information from the study materials:

- `content_retrieval_tool`: Retrieves relevant content from markdown files based on user queries
- `content_search_tool`: Searches across all study materials for specific terms or concepts
- `lab_retrieval_tool`: Fetches lab instructions and resources

### Progress Tools

The `progress_tools.py` file implements tools for tracking user progress:

- `get_progress_tool`: Retrieves the user's current progress through the course
- `update_progress_tool`: Updates the user's progress when they complete sections
- `get_recommendations_tool`: Suggests next sections based on current progress

### AWS Tools

The `aws_tools.py` file implements tools for accessing AWS documentation and service information:

- `aws_documentation_tool`: Fetches relevant AWS documentation using the AWS Documentation MCP server
- `aws_service_info_tool`: Provides information about specific AWS services
- `aws_best_practices_tool`: Retrieves best practices for AWS data engineering

## Usage

These tools are designed to be used with Strands Agents. Here's an example of how to use them:

```python
from strands import Agent
from app.tools.content_tools import content_retrieval_tool
from app.tools.progress_tools import get_progress_tool
from app.tools.aws_tools import aws_documentation_tool

# Create an agent with custom tools
agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[content_retrieval_tool, get_progress_tool, aws_documentation_tool],
    system_prompt="You are an assistant for AWS Data Engineer certification preparation."
)

# The agent can now use these tools to provide better responses
response = agent("Tell me about AWS Glue and show my progress in the Data Ingestion section.")
```

## Development

To add a new tool:

1. Create a function with appropriate parameters and return types
2. Add the `@tool` decorator from Strands
3. Include detailed docstrings explaining the tool's purpose and usage
4. Import and export the tool in `__init__.py`

Example:

```python
from strands import tool

@tool
def new_custom_tool(parameter: str) -> str:
    """
    Description of what this tool does.
    
    Args:
        parameter: Description of the parameter
        
    Returns:
        Description of the return value
    """
    # Tool implementation
    return f"Processed: {parameter}"
```
