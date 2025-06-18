"""
Components for displaying progress information in the UI.
"""

import streamlit as st
from datetime import datetime
import pandas as pd
from app.utils.progress_tracker import ProgressTracker

def display_progress_sidebar(tracker, domains, labs):
    """
    Display progress information in the sidebar.
    
    Args:
        tracker (ProgressTracker): The progress tracker instance
        domains (dict): Dictionary of domain information
        labs (dict): Dictionary of lab information
    """
    with st.sidebar:
        st.subheader("Your Progress")
        
        # Overall progress
        overall_progress = tracker.get_completion_percentage()
        st.progress(overall_progress / 100, f"Overall: {overall_progress:.1f}%")
        
        # Study guide progress
        study_guide_progress = tracker.get_completion_percentage("study_guide")
        st.progress(study_guide_progress / 100, f"Study Guide: {study_guide_progress:.1f}%")
        
        # Labs progress
        labs_progress = tracker.get_completion_percentage("labs")
        st.progress(labs_progress / 100, f"Labs: {labs_progress:.1f}%")
        
        # Last updated
        if "last_updated" in st.session_state.progress:
            try:
                last_updated = datetime.fromisoformat(st.session_state.progress["last_updated"])
                st.caption(f"Last updated: {last_updated.strftime('%Y-%m-%d %H:%M')}")
            except:
                pass
        
        # Reset progress button
        if st.button("Reset Progress", key="reset_progress_sidebar"):
            st.warning("Are you sure you want to reset all progress?")
            if st.button("Yes, reset all progress", key="confirm_reset"):
                tracker.reset_progress()
                st.success("Progress reset successfully!")
                st.rerun()

def display_progress_dashboard(tracker, domains, labs):
    """
    Display a comprehensive progress dashboard.
    
    Args:
        tracker (ProgressTracker): The progress tracker instance
        domains (dict): Dictionary of domain information
        labs (dict): Dictionary of lab information
    """
    st.title("Progress Dashboard")
    
    # Overall progress
    overall_progress = tracker.get_completion_percentage()
    st.subheader(f"Overall Progress: {overall_progress:.1f}%")
    st.progress(overall_progress / 100)
    
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["Study Guide Progress", "Labs Progress"])
    
    with tab1:
        st.subheader("Study Guide Progress")
        
        # Create a dataframe for study guide progress
        study_guide_data = []
        
        # Add introduction
        intro_complete = tracker.is_complete("study_guide", "intro")
        study_guide_data.append({
            "Section": "Introduction",
            "Status": "✅ Complete" if intro_complete else "❌ Incomplete",
            "Weight": "N/A"
        })
        
        # Add domains
        for domain_id, domain_info in domains.items():
            domain_complete = tracker.is_complete("study_guide", domain_id)
            study_guide_data.append({
                "Section": f"Domain {domain_id[-1]}: {domain_info['title']}",
                "Status": "✅ Complete" if domain_complete else "❌ Incomplete",
                "Weight": domain_info['weight']
            })
        
        # Add exam tips
        exam_tips_complete = tracker.is_complete("study_guide", "exam_tips")
        study_guide_data.append({
            "Section": "Exam Preparation Tips",
            "Status": "✅ Complete" if exam_tips_complete else "❌ Incomplete",
            "Weight": "N/A"
        })
        
        # Display as a dataframe
        df = pd.DataFrame(study_guide_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Labs Progress")
        
        # Group labs by domain
        domain_labs = {}
        for lab_id, lab_info in labs.items():
            domain = lab_info["domain"]
            if domain not in domain_labs:
                domain_labs[domain] = []
            domain_labs[domain].append((lab_id, lab_info))
        
        # Create a dataframe for labs progress
        labs_data = []
        
        for domain_id in sorted(domain_labs.keys()):
            domain_num = domain_id[-1]
            domain_title = domains[domain_id]["title"]
            
            # Add a header row for the domain
            labs_data.append({
                "Lab": f"Domain {domain_num}: {domain_title}",
                "Title": "",
                "Status": ""
            })
            
            # Add rows for each lab in the domain
            for lab_id, lab_info in sorted(domain_labs[domain_id]):
                lab_complete = tracker.is_complete("labs", lab_id)
                labs_data.append({
                    "Lab": lab_id.upper(),
                    "Title": lab_info["title"],
                    "Status": "✅ Complete" if lab_complete else "❌ Incomplete"
                })
        
        # Display as a dataframe
        df = pd.DataFrame(labs_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Last visited section
    last_section_type, last_section_id = tracker.get_last_visited()
    if last_section_type and last_section_id:
        st.subheader("Continue Where You Left Off")
        
        if last_section_type == "study_guide":
            if last_section_id == "intro":
                section_title = "Introduction"
            elif last_section_id == "exam_tips":
                section_title = "Exam Preparation Tips"
            else:
                domain_info = domains.get(last_section_id, {})
                section_title = f"Domain {last_section_id[-1]}: {domain_info.get('title', '')}"
        else:  # labs
            lab_info = labs.get(last_section_id, {})
            section_title = f"{last_section_id.upper()}: {lab_info.get('title', '')}"
        
        if st.button(f"Continue with: {section_title}", use_container_width=True):
            st.session_state.current_page = last_section_id
            st.rerun()

def display_section_progress(tracker, section_type, section_id, section_title):
    """
    Display progress information for a specific section with completion checkbox.
    
    Args:
        tracker (ProgressTracker): The progress tracker instance
        section_type (str): Type of section ('study_guide' or 'labs')
        section_id (str): ID of the section
        section_title (str): Title of the section
    """
    is_complete = tracker.is_complete(section_type, section_id)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        st.subheader(section_title)
    
    with col2:
        if st.checkbox("Mark Complete", value=is_complete, key=f"complete_{section_type}_{section_id}"):
            tracker.mark_complete(section_type, section_id, True)
        else:
            if is_complete:  # Only update if it was previously complete
                tracker.mark_complete(section_type, section_id, False)
