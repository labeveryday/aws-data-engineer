"""
Custom Tools for AWS Data Engineer Agents

This module exports all custom tools for use with Strands Agents.
"""

from .content_tools import (
    content_retrieval_tool,
    content_search_tool,
    lab_retrieval_tool,
    get_section_content
)

from .progress_tools import (
    get_progress_tool,
    update_progress_tool,
    get_recommendations_tool,
    get_study_stats_tool
)

from .aws_tools import (
    aws_service_info_tool,
    aws_best_practices_tool,
    aws_architecture_patterns_tool,
    aws_cost_optimization_tool
)

# Export all tools
__all__ = [
    # Content tools
    'content_retrieval_tool',
    'content_search_tool', 
    'lab_retrieval_tool',
    'get_section_content',
    
    # Progress tools
    'get_progress_tool',
    'update_progress_tool',
    'get_recommendations_tool',
    'get_study_stats_tool',
    
    # AWS tools
    'aws_service_info_tool',
    'aws_best_practices_tool',
    'aws_architecture_patterns_tool',
    'aws_cost_optimization_tool'
]
