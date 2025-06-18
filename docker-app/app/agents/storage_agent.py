"""
Storage Agent for AWS Data Engineer Course

This module implements the specialist agent for data storage topics including
S3, Redshift, DynamoDB, and related storage services.
"""

from strands import Agent
from app.tools import (
    content_retrieval_tool,
    content_search_tool,
    lab_retrieval_tool,
    aws_service_info_tool,
    aws_best_practices_tool,
    aws_architecture_patterns_tool,
    aws_cost_optimization_tool
)


class StorageAgent:
    """Specialist agent for AWS data storage services and concepts."""
    
    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        """
        Initialize the Storage Agent.
        
        Args:
            model_id: The Claude model ID to use
        """
        self.system_prompt = """You are a specialist AWS Data Engineer focused on data storage and management services.

Your expertise includes:
- Amazon S3 (storage classes, lifecycle policies, data organization)
- Amazon Redshift (data warehousing, performance optimization)
- Amazon DynamoDB (NoSQL database design, performance)
- Data lake architecture and organization
- Storage optimization and cost management
- Data partitioning and indexing strategies
- Backup and disaster recovery

When answering questions:
1. Recommend appropriate storage solutions based on use case
2. Consider performance, cost, and scalability requirements
3. Provide specific configuration recommendations
4. Include relevant labs and hands-on examples
5. Address data organization and governance aspects

Use your tools to:
- Retrieve relevant study materials and lab content
- Get detailed AWS service information
- Provide cost optimization recommendations
- Search for specific storage concepts in course materials

Focus on practical implementation details and real-world scenarios."""

        self.agent = Agent(
            model=f"bedrock:{model_id}",
            tools=[
                content_retrieval_tool,
                content_search_tool,
                lab_retrieval_tool,
                aws_service_info_tool,
                aws_best_practices_tool,
                aws_architecture_patterns_tool,
                aws_cost_optimization_tool
            ],
            system_prompt=self.system_prompt
        )
    
    def process_question(self, question: str, context: str = "") -> str:
        """
        Process a question related to data storage.
        
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
            "Amazon S3 data lake design and optimization",
            "Amazon Redshift data warehouse architecture",
            "DynamoDB NoSQL database design",
            "Storage class selection and lifecycle management",
            "Data partitioning and organization strategies",
            "Performance optimization for storage systems",
            "Cost optimization for storage solutions",
            "Backup and disaster recovery planning"
        ]
