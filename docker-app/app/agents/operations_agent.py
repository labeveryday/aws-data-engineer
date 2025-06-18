"""
Operations Agent for AWS Data Engineer Course

This module implements the specialist agent for data operations and optimization topics
including monitoring, orchestration, and performance optimization.
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


class OperationsAgent:
    """Specialist agent for AWS data operations and optimization services."""
    
    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        """
        Initialize the Operations Agent.
        
        Args:
            model_id: The Claude model ID to use
        """
        self.system_prompt = """You are a specialist AWS Data Engineer focused on data operations, monitoring, and optimization.

Your expertise includes:
- AWS Step Functions (workflow orchestration)
- Amazon CloudWatch (monitoring, logging, alerting)
- AWS EventBridge (event-driven architectures)
- Performance optimization and tuning
- Cost optimization strategies
- Operational excellence best practices
- Disaster recovery and business continuity
- Infrastructure as Code (CloudFormation, CDK)

When answering questions:
1. Focus on operational efficiency and reliability
2. Provide monitoring and alerting recommendations
3. Include cost optimization strategies
4. Address scalability and performance considerations
5. Emphasize automation and Infrastructure as Code

Use your tools to:
- Retrieve operations-focused study materials and labs
- Get detailed information about operational services
- Provide cost optimization recommendations
- Search for specific operational concepts in course materials

Always consider the operational lifecycle from deployment to monitoring to optimization."""

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
        Process a question related to data operations.
        
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
            "AWS Step Functions workflow orchestration",
            "CloudWatch monitoring and alerting setup",
            "Performance optimization and tuning",
            "Cost optimization strategies and implementation",
            "Disaster recovery and business continuity planning",
            "Infrastructure as Code best practices",
            "Operational excellence framework implementation",
            "Event-driven architecture design"
        ]
