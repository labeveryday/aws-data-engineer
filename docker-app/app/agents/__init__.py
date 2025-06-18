"""
Multi-Agent System for AWS Data Engineer Course

This module exports the main coordinator agent and all specialist agents.
"""

from .coordinator import CoordinatorAgent
from .ingestion_agent import DataIngestionAgent
from .storage_agent import StorageAgent
from .security_agent import SecurityAgent
from .operations_agent import OperationsAgent

# Export the main coordinator for easy access
coordinator = None

def get_coordinator(model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> CoordinatorAgent:
    """
    Get or create the main coordinator agent.
    
    Args:
        model_id: The Claude model ID to use
        
    Returns:
        CoordinatorAgent instance
    """
    global coordinator
    if coordinator is None:
        coordinator = CoordinatorAgent(model_id)
    return coordinator

# Export all agent classes
__all__ = [
    'CoordinatorAgent',
    'DataIngestionAgent', 
    'StorageAgent',
    'SecurityAgent',
    'OperationsAgent',
    'get_coordinator'
]
