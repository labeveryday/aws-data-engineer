"""
Content Tools for AWS Data Engineer Agents

This module implements tools for accessing and retrieving information from study materials.
"""

import os
import glob
from typing import List, Dict, Any
from strands import tool
import markdown
import re


@tool
def content_retrieval_tool(topic: str, domain: str = "") -> str:
    """
    Retrieves relevant content from study materials based on topic and optional domain.
    
    Args:
        topic: The topic or concept to search for
        domain: Optional domain filter (domain1, domain2, domain3, domain4)
        
    Returns:
        Relevant content from study materials
    """
    try:
        content_path = "content/study-guide"
        results = []
        
        # Get all markdown files
        if domain:
            # Map domain to file pattern
            domain_files = {
                "domain1": "*data-ingestion*",
                "domain2": "*storage*",
                "domain3": "*security*",
                "domain4": "*operations*"
            }
            pattern = domain_files.get(domain, "*")
            files = glob.glob(f"{content_path}/{pattern}.md")
        else:
            files = glob.glob(f"{content_path}/*.md")
        
        # Search through files
        for file_path in files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Simple keyword search (case-insensitive)
                if topic.lower() in content.lower():
                    # Extract relevant sections
                    lines = content.split('\n')
                    relevant_lines = []
                    
                    for i, line in enumerate(lines):
                        if topic.lower() in line.lower():
                            # Include context around the match
                            start = max(0, i - 3)
                            end = min(len(lines), i + 4)
                            context = '\n'.join(lines[start:end])
                            relevant_lines.append(context)
                    
                    if relevant_lines:
                        file_name = os.path.basename(file_path)
                        results.append(f"From {file_name}:\n" + '\n---\n'.join(relevant_lines))
        
        if results:
            return '\n\n'.join(results)
        else:
            return f"No specific content found for '{topic}'. You may want to browse the study materials or ask a more general question."
            
    except Exception as e:
        return f"Error retrieving content: {str(e)}"


@tool
def content_search_tool(query: str) -> str:
    """
    Searches across all study materials for specific terms or concepts.
    
    Args:
        query: Search query
        
    Returns:
        Search results with file names and relevant excerpts
    """
    try:
        content_path = "content/study-guide"
        results = []
        
        # Get all markdown files
        files = glob.glob(f"{content_path}/*.md")
        
        for file_path in files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Search for query (case-insensitive)
                if query.lower() in content.lower():
                    file_name = os.path.basename(file_path).replace('.md', '').replace('-', ' ').title()
                    
                    # Find all occurrences with context
                    lines = content.split('\n')
                    matches = []
                    
                    for i, line in enumerate(lines):
                        if query.lower() in line.lower():
                            # Get surrounding context
                            start = max(0, i - 2)
                            end = min(len(lines), i + 3)
                            context = '\n'.join(lines[start:end]).strip()
                            matches.append(context)
                    
                    if matches:
                        results.append(f"**{file_name}**:\n" + '\n\n'.join(matches[:3]))  # Limit to 3 matches per file
        
        if results:
            return '\n\n---\n\n'.join(results)
        else:
            return f"No results found for '{query}'. Try different keywords or browse the study materials."
            
    except Exception as e:
        return f"Error searching content: {str(e)}"


@tool
def lab_retrieval_tool(lab_id: str = "") -> str:
    """
    Fetches lab instructions and resources.
    
    Args:
        lab_id: Specific lab ID (e.g., 'lab1_1') or empty for all labs
        
    Returns:
        Lab instructions and resources
    """
    try:
        labs_path = "content/labs"
        
        if lab_id:
            # Map lab_id to file path (this would need to match your config.py)
            lab_mapping = {
                "lab1_1": "data-ingestion/lab-1.1-batch-ingestion-glue.md",
                "lab1_2": "data-ingestion/lab-1.2-streaming-kinesis.md",
                "lab1_3": "data-ingestion/lab-1.3-database-migration-dms.md",
                "lab2_1": "data-storage/lab-2.1-s3-data-lake.md",
                "lab2_2": "data-storage/lab-2.2-redshift-warehouse.md",
                "lab2_3": "data-storage/lab-2.3-dynamodb-nosql.md",
                "lab3_1": "data-transformation/lab-3.1-etl-glue.md",
                "lab3_2": "data-transformation/lab-3.2-stream-processing.md",
                "lab3_3": "data-transformation/lab-3.3-data-quality.md",
                "lab4_1": "security-governance/lab-4.1-lake-formation.md",
                "lab4_2": "security-governance/lab-4.2-column-security.md",
                "lab4_3": "security-governance/lab-4.3-cross-account.md",
                "lab5_1": "operations-optimization/lab-5.1-step-functions.md",
                "lab5_2": "operations-optimization/lab-5.2-monitoring.md",
                "lab5_3": "operations-optimization/lab-5.3-cost-optimization.md"
            }
            
            file_path = lab_mapping.get(lab_id)
            if file_path:
                full_path = f"{labs_path}/{file_path}"
                if os.path.exists(full_path):
                    with open(full_path, 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    return f"Lab file not found: {full_path}"
            else:
                return f"Unknown lab ID: {lab_id}"
        else:
            # Return list of available labs
            available_labs = []
            for root, dirs, files in os.walk(labs_path):
                for file in files:
                    if file.endswith('.md'):
                        rel_path = os.path.relpath(os.path.join(root, file), labs_path)
                        available_labs.append(rel_path)
            
            return f"Available labs:\n" + '\n'.join(f"- {lab}" for lab in sorted(available_labs))
            
    except Exception as e:
        return f"Error retrieving lab: {str(e)}"


@tool
def get_section_content(section: str) -> str:
    """
    Gets the full content of a specific study guide section.
    
    Args:
        section: Section identifier (intro, domain1, domain2, domain3, domain4, exam_tips)
        
    Returns:
        Full content of the specified section
    """
    try:
        content_path = "content/study-guide"
        
        # Map sections to files
        section_files = {
            "intro": "00-introduction.md",
            "domain1": "01-data-ingestion-transformation.md",
            "domain2": "02-storage-data-management.md",
            "domain3": "03-data-security-access-control.md",
            "domain4": "04-data-operations-optimization.md",
            "exam_tips": "05-exam-preparation-tips.md"
        }
        
        file_name = section_files.get(section)
        if not file_name:
            return f"Unknown section: {section}. Available sections: {', '.join(section_files.keys())}"
        
        file_path = f"{content_path}/{file_name}"
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"Section file not found: {file_path}"
            
    except Exception as e:
        return f"Error retrieving section content: {str(e)}"
