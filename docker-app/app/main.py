import streamlit as st
import os
import sys
from app.config import DOMAINS, LABS, STUDY_GUIDE_PATH, LABS_PATH
from app.utils.progress_tracker import ProgressTracker
from app.components.progress_display import display_progress_sidebar, display_section_progress
from app.components.chat_interface import display_embedded_chat, display_chat_sidebar

# Set page configuration
st.set_page_config(
    page_title="AWS Data Engineer Course",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize progress tracker
tracker = ProgressTracker()

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Define navigation
def sidebar_navigation():
    with st.sidebar:
        st.title("AWS Data Engineer")
        st.subheader("Navigation")
        
        if st.button("Home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()
            
        if st.button("Progress Dashboard", use_container_width=True):
            st.switch_page("pages/dashboard.py")
            
        if st.button("🤖 AI Assistant Chat", use_container_width=True):
            st.switch_page("pages/chat.py")
            
        st.subheader("Study Guide")
        if st.button("Introduction", use_container_width=True):
            st.session_state.current_page = "intro"
            st.rerun()
            
        # Add domain buttons
        for domain_key, domain_info in DOMAINS.items():
            # Add completion indicator
            is_complete = tracker.is_complete("study_guide", domain_key)
            label = f"{'✅ ' if is_complete else ''}Domain {domain_key[-1]}: {domain_info['title']}"
            
            if st.button(label, use_container_width=True):
                st.session_state.current_page = domain_key
                st.rerun()
                
        # Add completion indicator
        exam_tips_complete = tracker.is_complete("study_guide", "exam_tips")
        exam_tips_label = f"{'✅ ' if exam_tips_complete else ''}Exam Preparation Tips"
        
        if st.button(exam_tips_label, use_container_width=True):
            st.session_state.current_page = "exam_tips"
            st.rerun()
        
        # Group labs by domain
        domain_labs = {}
        for lab_key, lab_info in LABS.items():
            domain = lab_info["domain"]
            if domain not in domain_labs:
                domain_labs[domain] = []
            domain_labs[domain].append((lab_key, lab_info))
        
        # Display labs grouped by domain
        st.subheader("Labs")
        for domain_key in sorted(domain_labs.keys()):
            domain_num = domain_key[-1]
            st.markdown(f"**Domain {domain_num} Labs:**")
            
            for lab_key, lab_info in sorted(domain_labs[domain_key]):
                # Add completion indicator
                is_complete = tracker.is_complete("labs", lab_key)
                label = f"{'✅ ' if is_complete else ''}{lab_key.upper()}: {lab_info['title']}"
                
                if st.button(label, use_container_width=True, key=lab_key):
                    st.session_state.current_page = lab_key
                    st.rerun()
            
            st.markdown("---")
        
        # Display progress information
        display_progress_sidebar(tracker, DOMAINS, LABS)
        
        # Display chat sidebar
        display_chat_sidebar()

# Render markdown content
def render_markdown(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            st.markdown(content)
    except Exception as e:
        st.error(f"Error loading content: {e}")
        st.error(f"File path: {file_path}")
        st.error(f"Current working directory: {os.getcwd()}")
        st.error(f"Files in directory: {os.listdir(os.path.dirname(file_path) if os.path.dirname(file_path) else '.')}")

# Main content area
def main_content():
    if st.session_state.current_page == "Home":
        st.title("AWS Certified Data Engineer - Associate")
        st.subheader("Interactive Study Guide & Labs")
        
        st.markdown("""
        Welcome to your interactive AWS Data Engineer certification course! This application provides:
        
        - **Comprehensive study materials** covering all exam domains
        - **Hands-on labs** to build practical skills
        - **Interactive features** to enhance your learning experience
        - **Progress tracking** to monitor your preparation
        
        Use the navigation sidebar to explore study materials and labs. Your progress will be tracked as you complete sections.
        """)
        
        # Display quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            overall_progress = tracker.get_completion_percentage()
            st.metric("Overall Progress", f"{overall_progress:.1f}%")
        
        with col2:
            study_guide_progress = tracker.get_completion_percentage("study_guide")
            st.metric("Study Guide Progress", f"{study_guide_progress:.1f}%")
        
        with col3:
            labs_progress = tracker.get_completion_percentage("labs")
            st.metric("Labs Progress", f"{labs_progress:.1f}%")
        
        st.markdown("""
        ## Getting Started
        
        1. Start with the Introduction to understand the exam structure
        2. Work through each domain systematically
        3. Complete the hands-on labs to reinforce concepts
        4. Review the exam preparation tips before your exam
        5. Track your progress in the Progress Dashboard
        
        Good luck with your AWS Certified Data Engineer - Associate exam preparation!
        """)
        
        # Add embedded chat interface
        display_embedded_chat()
        
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
                    domain_info = DOMAINS.get(last_section_id, {})
                    section_title = f"Domain {last_section_id[-1]}: {domain_info.get('title', '')}"
            else:  # labs
                lab_info = LABS.get(last_section_id, {})
                section_title = f"{last_section_id.upper()}: {lab_info.get('title', '')}"
            
            if st.button(f"Continue with: {section_title}", use_container_width=True):
                st.session_state.current_page = last_section_id
                st.rerun()
        
    elif st.session_state.current_page == "intro":
        display_section_progress(tracker, "study_guide", "intro", "Introduction")
        render_markdown(f"{STUDY_GUIDE_PATH}/00-introduction.md")
        
    # Handle domain pages
    elif st.session_state.current_page in DOMAINS:
        domain_info = DOMAINS[st.session_state.current_page]
        display_section_progress(
            tracker, 
            "study_guide", 
            st.session_state.current_page, 
            f"Domain {st.session_state.current_page[-1]}: {domain_info['title']}"
        )
        render_markdown(f"{STUDY_GUIDE_PATH}/{domain_info['file']}")
        
    elif st.session_state.current_page == "exam_tips":
        display_section_progress(tracker, "study_guide", "exam_tips", "Exam Preparation Tips")
        render_markdown(f"{STUDY_GUIDE_PATH}/05-exam-preparation-tips.md")
        
    # Handle lab pages
    elif st.session_state.current_page in LABS:
        lab_info = LABS[st.session_state.current_page]
        display_section_progress(
            tracker, 
            "labs", 
            st.session_state.current_page, 
            f"{st.session_state.current_page.upper()}: {lab_info['title']}"
        )
        render_markdown(f"{LABS_PATH}/{lab_info['file']}")
    
    else:
        st.error(f"Page not found: {st.session_state.current_page}")

# Main app layout
sidebar_navigation()
main_content()

# Display app info in footer
st.sidebar.markdown("---")
st.sidebar.info("AWS Data Engineer Course v1.0")
