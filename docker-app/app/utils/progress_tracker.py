"""
Utility for tracking user progress through the course.
"""

import json
import os
import streamlit as st
from datetime import datetime

class ProgressTracker:
    """
    Tracks user progress through the course content.
    """
    
    def __init__(self, save_to_file=True, file_path="progress.json"):
        """
        Initialize the progress tracker.
        
        Args:
            save_to_file (bool): Whether to save progress to a file
            file_path (str): Path to save the progress file
        """
        self.save_to_file = save_to_file
        self.file_path = file_path
        
        # Initialize progress in session state if not already present
        if "progress" not in st.session_state:
            st.session_state.progress = {
                "study_guide": {},
                "labs": {},
                "last_updated": datetime.now().isoformat()
            }
            
            # Load progress from file if it exists
            if save_to_file and os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        saved_progress = json.load(f)
                        st.session_state.progress = saved_progress
                except Exception as e:
                    st.error(f"Error loading progress: {e}")
    
    def mark_complete(self, section_type, section_id, status=True):
        """
        Mark a section as complete or incomplete.
        
        Args:
            section_type (str): Type of section ('study_guide' or 'labs')
            section_id (str): ID of the section
            status (bool): Whether the section is complete
        """
        if section_type not in st.session_state.progress:
            st.session_state.progress[section_type] = {}
            
        st.session_state.progress[section_type][section_id] = {
            "complete": status,
            "timestamp": datetime.now().isoformat()
        }
        
        # Update last updated timestamp
        st.session_state.progress["last_updated"] = datetime.now().isoformat()
        
        # Save to file if enabled
        if self.save_to_file:
            self._save_progress()
    
    def is_complete(self, section_type, section_id):
        """
        Check if a section is marked as complete.
        
        Args:
            section_type (str): Type of section ('study_guide' or 'labs')
            section_id (str): ID of the section
            
        Returns:
            bool: True if the section is complete, False otherwise
        """
        if section_type not in st.session_state.progress:
            return False
            
        if section_id not in st.session_state.progress[section_type]:
            return False
            
        return st.session_state.progress[section_type][section_id].get("complete", False)
    
    def get_completion_percentage(self, section_type=None):
        """
        Get the percentage of sections that are complete.
        
        Args:
            section_type (str, optional): Type of section to calculate percentage for.
                                         If None, calculates for all sections.
                                         
        Returns:
            float: Percentage of sections that are complete (0-100)
        """
        if section_type:
            if section_type not in st.session_state.progress:
                return 0
                
            sections = st.session_state.progress[section_type]
            if not sections:
                return 0
                
            complete = sum(1 for s in sections.values() if s.get("complete", False))
            return (complete / len(sections)) * 100
        else:
            # Calculate for all sections
            all_sections = []
            for s_type in ["study_guide", "labs"]:
                if s_type in st.session_state.progress:
                    all_sections.extend(st.session_state.progress[s_type].values())
            
            if not all_sections:
                return 0
                
            complete = sum(1 for s in all_sections if s.get("complete", False))
            return (complete / len(all_sections)) * 100
    
    def get_last_visited(self):
        """
        Get the last visited section.
        
        Returns:
            tuple: (section_type, section_id) of the last visited section,
                  or (None, None) if no sections have been visited
        """
        last_timestamp = None
        last_section = (None, None)
        
        for section_type in ["study_guide", "labs"]:
            if section_type not in st.session_state.progress:
                continue
                
            for section_id, data in st.session_state.progress[section_type].items():
                if "timestamp" in data:
                    timestamp = datetime.fromisoformat(data["timestamp"])
                    if last_timestamp is None or timestamp > last_timestamp:
                        last_timestamp = timestamp
                        last_section = (section_type, section_id)
        
        return last_section
    
    def reset_progress(self):
        """
        Reset all progress.
        """
        st.session_state.progress = {
            "study_guide": {},
            "labs": {},
            "last_updated": datetime.now().isoformat()
        }
        
        # Save to file if enabled
        if self.save_to_file:
            self._save_progress()
    
    def _save_progress(self):
        """
        Save progress to file.
        """
        try:
            with open(self.file_path, 'w') as f:
                json.dump(st.session_state.progress, f, indent=2)
        except Exception as e:
            st.error(f"Error saving progress: {e}")
