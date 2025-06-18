"""
Security Agent for AWS Data Engineer Course

This module implements the specialist agent for data security and governance topics
including IAM, Lake Formation, encryption, and compliance.
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


class SecurityAgent:
    """Specialist agent for AWS data security and governance services."""
    
    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        """
        Initialize the Security Agent.
        
        Args:
            model_id: The Claude model ID to use
        """
        self.system_prompt = """You are a specialist AWS Data Engineer focused on data security, governance, and compliance.

Your expertise includes:
- AWS Lake Formation (permissions, governance, security)
- AWS Identity and Access Management (IAM roles, policies)
- Data encryption (at rest and in transit)
- Row and column-level security
- Data masking and anonymization
- Compliance frameworks (GDPR, HIPAA, SOX)
- Audit logging and monitoring
- Cross-account data sharing

When answering questions:
1. Prioritize security best practices and least privilege principles
2. Provide specific IAM policy examples when relevant
3. Address compliance and regulatory requirements
4. Include hands-on security implementation guidance
5. Consider both technical and operational security aspects

Use your tools to:
- Retrieve security-focused study materials and labs
- Get detailed information about security services
- Provide security best practices and patterns
- Search for specific security concepts in course materials

Always emphasize the importance of defense in depth and proper access controls."""

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
        Process a question related to data security.
        
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
            "AWS Lake Formation security and governance",
            "IAM roles and policies for data access",
            "Data encryption strategies and implementation",
            "Row and column-level security controls",
            "Data masking and anonymization techniques",
            "Compliance framework implementation",
            "Audit logging and security monitoring",
            "Cross-account data sharing security"
        ]
