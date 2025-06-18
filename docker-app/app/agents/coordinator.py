"""
Coordinator Agent for AWS Data Engineer Course

This module implements the main coordinator agent that routes questions to specialist agents
and synthesizes their responses into coherent answers for the user.
"""

import re
from typing import Dict, List, Tuple, Any
from strands import Agent
from app.tools import (
    get_progress_tool,
    update_progress_tool,
    get_recommendations_tool,
    get_study_stats_tool,
    content_search_tool,
    get_section_content
)
from .ingestion_agent import DataIngestionAgent
from .storage_agent import StorageAgent
from .security_agent import SecurityAgent
from .operations_agent import OperationsAgent


class CoordinatorAgent:
    """Main coordinator agent that routes questions and synthesizes responses."""
    
    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        """
        Initialize the Coordinator Agent and all specialist agents.
        
        Args:
            model_id: The Claude model ID to use
        """
        self.model_id = model_id
        
        # Initialize specialist agents
        self.ingestion_agent = DataIngestionAgent(model_id)
        self.storage_agent = StorageAgent(model_id)
        self.security_agent = SecurityAgent(model_id)
        self.operations_agent = OperationsAgent(model_id)
        
        # Coordinator system prompt
        self.system_prompt = """You are the main coordinator for an AWS Data Engineer certification course assistant.

Your role is to:
1. Analyze user questions and determine which specialist agent(s) should handle them
2. Route questions to appropriate specialists
3. Synthesize responses from multiple agents when needed
4. Provide general course guidance and progress tracking
5. Handle meta-questions about the course structure and navigation

Available specialist agents:
- Data Ingestion Agent: AWS Glue, Kinesis, DMS, ETL, streaming
- Storage Agent: S3, Redshift, DynamoDB, data lakes, storage optimization
- Security Agent: Lake Formation, IAM, encryption, compliance, governance
- Operations Agent: Step Functions, CloudWatch, monitoring, cost optimization

Use your tools to:
- Track and update user progress
- Provide study recommendations
- Search course content
- Get section-specific content

When routing questions:
1. Identify the primary domain(s) involved
2. Route to the most appropriate specialist(s)
3. Synthesize responses if multiple agents are involved
4. Always provide actionable, practical guidance"""

        self.coordinator = Agent(
            model=f"bedrock:{model_id}",
            tools=[
                get_progress_tool,
                update_progress_tool,
                get_recommendations_tool,
                get_study_stats_tool,
                content_search_tool,
                get_section_content
            ],
            system_prompt=self.system_prompt
        )
        
        # Keywords for routing decisions
        self.routing_keywords = {
            'ingestion': [
                'glue', 'kinesis', 'dms', 'etl', 'streaming', 'batch', 'ingestion', 
                'data migration', 'crawler', 'firehose', 'data streams', 'transformation'
            ],
            'storage': [
                's3', 'redshift', 'dynamodb', 'storage', 'data lake', 'warehouse', 
                'nosql', 'database', 'partition', 'compression', 'lifecycle'
            ],
            'security': [
                'security', 'iam', 'lake formation', 'encryption', 'permissions', 
                'governance', 'compliance', 'access control', 'masking', 'audit'
            ],
            'operations': [
                'step functions', 'cloudwatch', 'monitoring', 'optimization', 'cost', 
                'orchestration', 'alerting', 'performance', 'operations', 'eventbridge'
            ]
        }
    
    def analyze_question(self, question: str) -> List[str]:
        """
        Analyze a question to determine which specialist agent(s) should handle it.
        
        Args:
            question: The user's question
            
        Returns:
            List of agent types that should handle the question
        """
        question_lower = question.lower()
        relevant_agents = []
        
        # Check for keywords in each domain
        for domain, keywords in self.routing_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                relevant_agents.append(domain)
        
        # If no specific domain detected, try to infer from context
        if not relevant_agents:
            # General AWS data engineering questions go to ingestion by default
            if any(word in question_lower for word in ['aws', 'data', 'pipeline', 'architecture']):
                relevant_agents.append('ingestion')
            else:
                # For course-related questions, handle with coordinator
                relevant_agents.append('coordinator')
        
        return relevant_agents
    
    def route_question(self, question: str, context: str = "") -> str:
        """
        Route a question to the appropriate specialist agent(s) and return the response.
        
        Args:
            question: The user's question
            context: Additional context from the conversation
            
        Returns:
            Response from the appropriate agent(s)
        """
        try:
            # Check if this is a course/progress related question
            course_keywords = ['progress', 'recommendation', 'next', 'complete', 'stats', 'course']
            if any(keyword in question.lower() for keyword in course_keywords):
                return self.coordinator.run(question)
            
            # Analyze which agents should handle the question
            relevant_agents = self.analyze_question(question)
            
            if 'coordinator' in relevant_agents:
                return self.coordinator.run(question)
            
            responses = []
            
            # Route to appropriate specialist agents
            if 'ingestion' in relevant_agents:
                response = self.ingestion_agent.process_question(question, context)
                responses.append(('Data Ingestion', response))
            
            if 'storage' in relevant_agents:
                response = self.storage_agent.process_question(question, context)
                responses.append(('Storage', response))
            
            if 'security' in relevant_agents:
                response = self.security_agent.process_question(question, context)
                responses.append(('Security', response))
            
            if 'operations' in relevant_agents:
                response = self.operations_agent.process_question(question, context)
                responses.append(('Operations', response))
            
            # Synthesize responses if multiple agents were involved
            if len(responses) > 1:
                return self._synthesize_responses(question, responses)
            elif len(responses) == 1:
                return responses[0][1]
            else:
                # Fallback to ingestion agent for general questions
                return self.ingestion_agent.process_question(question, context)
                
        except Exception as e:
            return f"Error processing question: {str(e)}"
    
    def _synthesize_responses(self, question: str, responses: List[Tuple[str, str]]) -> str:
        """
        Synthesize responses from multiple specialist agents.
        
        Args:
            question: The original question
            responses: List of (agent_name, response) tuples
            
        Returns:
            Synthesized response
        """
        try:
            synthesis_prompt = f"""Question: {question}

I received responses from multiple specialist agents. Please synthesize these into a coherent, comprehensive answer:

"""
            for agent_name, response in responses:
                synthesis_prompt += f"**{agent_name} Agent Response:**\n{response}\n\n"
            
            synthesis_prompt += """Please provide a unified response that:
1. Combines the relevant information from all agents
2. Eliminates redundancy
3. Provides a clear, actionable answer
4. Maintains the practical, hands-on focus"""
            
            return self.coordinator.run(synthesis_prompt)
            
        except Exception as e:
            # Fallback: return all responses with headers
            result = f"Here are responses from multiple specialists:\n\n"
            for agent_name, response in responses:
                result += f"**{agent_name} Perspective:**\n{response}\n\n"
            return result
    
    def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """Return capabilities of all agents."""
        return {
            'Data Ingestion': self.ingestion_agent.get_capabilities(),
            'Storage': self.storage_agent.get_capabilities(),
            'Security': self.security_agent.get_capabilities(),
            'Operations': self.operations_agent.get_capabilities()
        }
    
    def handle_course_navigation(self, request: str) -> str:
        """
        Handle course navigation and progress-related requests.
        
        Args:
            request: Navigation or progress request
            
        Returns:
            Response with navigation guidance or progress information
        """
        try:
            return self.coordinator.run(request)
        except Exception as e:
            return f"Error handling course navigation: {str(e)}"
