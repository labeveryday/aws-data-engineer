"""
Progress Tools for AWS Data Engineer Agents

This module implements tools for tracking and updating user progress through the course.
"""

from typing import Dict, List, Any, Tuple
from strands import tool
from app.utils.progress_tracker import ProgressTracker


@tool
def get_progress_tool() -> str:
    """
    Retrieves the user's current progress through the course.
    
    Returns:
        Formatted progress information including completion percentages and sections completed
    """
    try:
        tracker = ProgressTracker()
        
        # Get overall progress
        overall_progress = tracker.get_completion_percentage()
        study_guide_progress = tracker.get_completion_percentage("study_guide")
        labs_progress = tracker.get_completion_percentage("labs")
        
        # Get completed sections
        completed_study = tracker.get_completed_sections("study_guide")
        completed_labs = tracker.get_completed_sections("labs")
        
        # Get last visited section
        last_section_type, last_section_id = tracker.get_last_visited()
        
        progress_info = f"""**Current Progress Summary:**

**Overall Progress:** {overall_progress:.1f}%
**Study Guide Progress:** {study_guide_progress:.1f}%
**Labs Progress:** {labs_progress:.1f}%

**Completed Study Guide Sections:**
{', '.join(completed_study) if completed_study else 'None completed yet'}

**Completed Labs:**
{', '.join(completed_labs) if completed_labs else 'None completed yet'}

**Last Visited Section:**
{f"{last_section_type}: {last_section_id}" if last_section_type and last_section_id else "No previous activity"}
"""
        
        return progress_info
        
    except Exception as e:
        return f"Error retrieving progress: {str(e)}"


@tool
def update_progress_tool(section_type: str, section_id: str, completed: bool = True) -> str:
    """
    Updates the user's progress when they complete sections.
    
    Args:
        section_type: Type of section ('study_guide' or 'labs')
        section_id: ID of the section (e.g., 'domain1', 'lab1_1')
        completed: Whether the section is completed (default: True)
        
    Returns:
        Confirmation message about the progress update
    """
    try:
        tracker = ProgressTracker()
        
        if completed:
            tracker.mark_complete(section_type, section_id)
            return f"✅ Marked {section_type} section '{section_id}' as completed!"
        else:
            tracker.mark_incomplete(section_type, section_id)
            return f"⏳ Marked {section_type} section '{section_id}' as incomplete."
            
    except Exception as e:
        return f"Error updating progress: {str(e)}"


@tool
def get_recommendations_tool() -> str:
    """
    Suggests next sections based on current progress and learning path.
    
    Returns:
        Personalized recommendations for what to study next
    """
    try:
        tracker = ProgressTracker()
        
        # Get current progress
        completed_study = set(tracker.get_completed_sections("study_guide"))
        completed_labs = set(tracker.get_completed_sections("labs"))
        
        # Define learning path
        study_sections = ["intro", "domain1", "domain2", "domain3", "domain4", "exam_tips"]
        lab_sections = ["lab1_1", "lab1_2", "lab1_3", "lab2_1", "lab2_2", "lab2_3", 
                       "lab3_1", "lab3_2", "lab3_3", "lab4_1", "lab4_2", "lab4_3",
                       "lab5_1", "lab5_2", "lab5_3"]
        
        recommendations = []
        
        # Study guide recommendations
        for section in study_sections:
            if section not in completed_study:
                section_names = {
                    "intro": "Introduction to AWS Data Engineering",
                    "domain1": "Data Ingestion and Transformation",
                    "domain2": "Storage and Data Management", 
                    "domain3": "Data Security and Access Control",
                    "domain4": "Data Operations and Optimization",
                    "exam_tips": "Exam Preparation Tips"
                }
                recommendations.append(f"📚 Study Guide: {section_names.get(section, section)}")
                break  # Recommend next incomplete section
        
        # Lab recommendations based on completed study sections
        if "domain1" in completed_study:
            domain1_labs = ["lab1_1", "lab1_2", "lab1_3", "lab3_1", "lab3_2", "lab3_3"]
            for lab in domain1_labs:
                if lab not in completed_labs:
                    lab_names = {
                        "lab1_1": "Batch Data Ingestion with AWS Glue",
                        "lab1_2": "Streaming Data with Amazon Kinesis",
                        "lab1_3": "Database Migration with AWS DMS",
                        "lab3_1": "ETL with AWS Glue",
                        "lab3_2": "Stream Processing with Kinesis Analytics",
                        "lab3_3": "Data Quality and Validation"
                    }
                    recommendations.append(f"🧪 Lab: {lab_names.get(lab, lab)}")
                    break
        
        if "domain2" in completed_study:
            domain2_labs = ["lab2_1", "lab2_2", "lab2_3"]
            for lab in domain2_labs:
                if lab not in completed_labs:
                    lab_names = {
                        "lab2_1": "S3 Data Lake Organization",
                        "lab2_2": "Amazon Redshift Data Warehouse Setup",
                        "lab2_3": "DynamoDB NoSQL Database Design"
                    }
                    recommendations.append(f"🧪 Lab: {lab_names.get(lab, lab)}")
                    break
        
        if "domain3" in completed_study:
            domain3_labs = ["lab4_1", "lab4_2", "lab4_3"]
            for lab in domain3_labs:
                if lab not in completed_labs:
                    lab_names = {
                        "lab4_1": "Data Governance with AWS Lake Formation",
                        "lab4_2": "Column-Level Security",
                        "lab4_3": "Cross-Account Data Sharing"
                    }
                    recommendations.append(f"🧪 Lab: {lab_names.get(lab, lab)}")
                    break
        
        if "domain4" in completed_study:
            domain4_labs = ["lab5_1", "lab5_2", "lab5_3"]
            for lab in domain4_labs:
                if lab not in completed_labs:
                    lab_names = {
                        "lab5_1": "Pipeline Orchestration with AWS Step Functions",
                        "lab5_2": "Monitoring and Alerting",
                        "lab5_3": "Cost Optimization Strategies"
                    }
                    recommendations.append(f"🧪 Lab: {lab_names.get(lab, lab)}")
                    break
        
        # General recommendations
        overall_progress = tracker.get_completion_percentage()
        
        if overall_progress < 25:
            recommendations.append("💡 Focus on completing the Introduction and Domain 1 first")
        elif overall_progress < 50:
            recommendations.append("💡 Great progress! Continue with Domain 2 and related labs")
        elif overall_progress < 75:
            recommendations.append("💡 You're halfway there! Focus on Domains 3 and 4")
        else:
            recommendations.append("💡 Almost done! Complete remaining sections and review exam tips")
        
        if not recommendations:
            recommendations.append("🎉 Congratulations! You've completed all sections. Review and prepare for your exam!")
        
        return "**Recommended Next Steps:**\n\n" + '\n'.join(f"- {rec}" for rec in recommendations[:5])
        
    except Exception as e:
        return f"Error generating recommendations: {str(e)}"


@tool
def get_study_stats_tool() -> str:
    """
    Provides detailed statistics about the user's study progress.
    
    Returns:
        Detailed study statistics and analytics
    """
    try:
        tracker = ProgressTracker()
        
        # Get completion data
        completed_study = tracker.get_completed_sections("study_guide")
        completed_labs = tracker.get_completed_sections("labs")
        
        # Calculate domain-specific progress
        domain_progress = {}
        for domain in ["domain1", "domain2", "domain3", "domain4"]:
            domain_progress[domain] = {
                "study_complete": domain in completed_study,
                "labs_complete": []
            }
        
        # Map labs to domains
        lab_domain_mapping = {
            "lab1_1": "domain1", "lab1_2": "domain1", "lab1_3": "domain1",
            "lab3_1": "domain1", "lab3_2": "domain1", "lab3_3": "domain1",
            "lab2_1": "domain2", "lab2_2": "domain2", "lab2_3": "domain2",
            "lab4_1": "domain3", "lab4_2": "domain3", "lab4_3": "domain3",
            "lab5_1": "domain4", "lab5_2": "domain4", "lab5_3": "domain4"
        }
        
        for lab in completed_labs:
            domain = lab_domain_mapping.get(lab)
            if domain:
                domain_progress[domain]["labs_complete"].append(lab)
        
        # Generate stats
        stats = "**Detailed Study Statistics:**\n\n"
        
        for domain, data in domain_progress.items():
            domain_names = {
                "domain1": "Data Ingestion and Transformation (30-35%)",
                "domain2": "Storage and Data Management (30-35%)",
                "domain3": "Data Security and Access Control (15-20%)",
                "domain4": "Data Operations and Optimization (15-20%)"
            }
            
            study_status = "✅" if data["study_complete"] else "⏳"
            labs_count = len(data["labs_complete"])
            total_labs = len([lab for lab, d in lab_domain_mapping.items() if d == domain])
            
            stats += f"**{domain_names[domain]}**\n"
            stats += f"- Study Guide: {study_status}\n"
            stats += f"- Labs Completed: {labs_count}/{total_labs}\n"
            if data["labs_complete"]:
                stats += f"- Completed Labs: {', '.join(data['labs_complete'])}\n"
            stats += "\n"
        
        # Overall stats
        total_sections = 6  # intro + 4 domains + exam_tips
        total_labs = 15
        
        stats += f"**Overall Statistics:**\n"
        stats += f"- Study Guide: {len(completed_study)}/{total_sections} sections\n"
        stats += f"- Labs: {len(completed_labs)}/{total_labs} completed\n"
        stats += f"- Total Progress: {tracker.get_completion_percentage():.1f}%\n"
        
        return stats
        
    except Exception as e:
        return f"Error generating study statistics: {str(e)}"
