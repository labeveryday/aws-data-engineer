import streamlit as st
import os
import sys
from config import DOMAINS, LABS, STUDY_GUIDE_PATH, LABS_PATH

# Set page configuration
st.set_page_config(
    page_title="AWS Data Engineer Course",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "progress" not in st.session_state:
    st.session_state.progress = {}

# Define navigation
def sidebar_navigation():
    with st.sidebar:
        st.title("AWS Data Engineer")
        st.subheader("Navigation")
        
        if st.button("Home", use_container_width=True):
            st.session_state.current_page = "Home"
            st.rerun()
            
        st.subheader("Study Guide")
        if st.button("Introduction", use_container_width=True):
            st.session_state.current_page = "intro"
            st.rerun()
            
        # Add domain buttons
        for domain_key, domain_info in DOMAINS.items():
            if st.button(f"Domain {domain_key[-1]}: {domain_info['title']}", use_container_width=True):
                st.session_state.current_page = domain_key
                st.rerun()
                
        if st.button("Exam Preparation Tips", use_container_width=True):
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
                if st.button(f"{lab_key.upper()}: {lab_info['title']}", use_container_width=True, key=lab_key):
                    st.session_state.current_page = lab_key
                    st.rerun()
            
            st.markdown("---")

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
        
        Use the navigation sidebar to explore study materials and labs. Your progress will be tracked as you complete sections.
        
        ## Getting Started
        
        1. Start with the Introduction to understand the exam structure
        2. Work through each domain systematically
        3. Complete the hands-on labs to reinforce concepts
        4. Review the exam preparation tips before your exam
        
        Good luck with your AWS Certified Data Engineer - Associate exam preparation!
        """)
        
    elif st.session_state.current_page == "intro":
        st.title("Introduction")
        render_markdown(f"{STUDY_GUIDE_PATH}/00-introduction.md")
        
    # Handle domain pages
    elif st.session_state.current_page in DOMAINS:
        domain_info = DOMAINS[st.session_state.current_page]
        st.title(f"Domain {st.session_state.current_page[-1]}: {domain_info['title']}")
        render_markdown(f"{STUDY_GUIDE_PATH}/{domain_info['file']}")
        
    elif st.session_state.current_page == "exam_tips":
        st.title("Exam Preparation Tips")
        render_markdown(f"{STUDY_GUIDE_PATH}/05-exam-preparation-tips.md")
        
    # Handle lab pages
    elif st.session_state.current_page in LABS:
        lab_info = LABS[st.session_state.current_page]
        st.title(f"{st.session_state.current_page.upper()}: {lab_info['title']}")
        render_markdown(f"{LABS_PATH}/{lab_info['file']}")
    
    else:
        st.error(f"Page not found: {st.session_state.current_page}")

# Main app layout
sidebar_navigation()
main_content()

# Display app info in footer
st.sidebar.markdown("---")
st.sidebar.info("AWS Data Engineer Course v1.0")
