"""
Data Ingestion Agent for AWS Data Engineer Course

This module implements the specialist agent for data ingestion topics including
AWS Glue, Kinesis, DMS, and related data ingestion services.
"""

from strands import Agent
from app.tools import (
    content_retrieval_tool,
    content_search_tool,
    lab_retrieval_tool,
    aws_service_info_tool,
    aws_best_practices_tool,
    aws_architecture_patterns_tool
)


class DataIngestionAgent:
    """Specialist agent for AWS data ingestion services and concepts."""
    
    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        """
        Initialize the Data Ingestion Agent.
        
        Args:
            model_id: The Claude model ID to use
        """
        self.system_prompt = """You are a specialist AWS Data Engineer focused on data ingestion and transformation services. 

Your expertise includes:
- AWS Glue (ETL, Data Catalog, Crawlers, Jobs)
- Amazon Kinesis (Data Streams, Data Firehose, Analytics)
- AWS Database Migration Service (DMS)
- Data transformation patterns and best practices
- Batch vs streaming ingestion strategies
- Data quality and validation techniques

When answering questions:
1. Provide practical, hands-on guidance
2. Include specific AWS service recommendations
3. Mention relevant labs when applicable
4. Consider cost and performance implications
5. Reference best practices and common patterns

Use your tools to:
- Retrieve relevant study materials and lab content
- Get detailed AWS service information
- Provide architecture patterns and best practices
- Search for specific concepts in the course materials

Always be specific about AWS services, configurations, and implementation details."""

        self.agent = Agent(
            model=f"bedrock:{model_id}",
            tools=[
                content_retrieval_tool,
                content_search_tool,
                lab_retrieval_tool,
                aws_service_info_tool,
                aws_best_practices_tool,
                aws_architecture_patterns_tool
            ],
            system_prompt=self.system_prompt
        )
    
    def process_question(self, question: str, context: str = "") -> str:
        """
        Process a question related to data ingestion.
        
        Args:
            question: The user's question
            context: Additional context from the conversation
            
        Returns:
            Response from the agent
        """
        try:
            # Add context if provided
            full_prompt = question
            if context:
                full_prompt = f"Context: {context}\n\nQuestion: {question}"
            
            response = self.agent.run(full_prompt)
            return response
            
        except Exception as e:
            return f"Error processing question: {str(e)}"
    
    def get_capabilities(self) -> list:
        """Return a list of this agent's capabilities."""
        return [
            "AWS Glue ETL jobs and data catalog",
            "Amazon Kinesis streaming data ingestion",
            "AWS DMS database migration",
            "Data transformation patterns",
            "Batch vs streaming architecture decisions",
            "Data quality and validation strategies",
            "Performance optimization for ingestion pipelines",
            "Cost optimization for data ingestion"
        ]
