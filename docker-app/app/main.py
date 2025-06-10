import streamlit as st
import os
import sys

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
        if st.button("Domain 1: Data Ingestion", use_container_width=True):
            st.session_state.current_page = "domain1"
            st.rerun()
        if st.button("Domain 2: Storage & Management", use_container_width=True):
            st.session_state.current_page = "domain2"
            st.rerun()
        if st.button("Domain 3: Security & Access", use_container_width=True):
            st.session_state.current_page = "domain3"
            st.rerun()
        if st.button("Domain 4: Operations & Optimization", use_container_width=True):
            st.session_state.current_page = "domain4"
            st.rerun()
        if st.button("Exam Preparation Tips", use_container_width=True):
            st.session_state.current_page = "exam_tips"
            st.rerun()
        
        st.subheader("Labs")
        # Data Ingestion Labs
        if st.button("Lab 1.1: Batch Ingestion", use_container_width=True):
            st.session_state.current_page = "lab1_1"
            st.rerun()
        if st.button("Lab 1.2: Streaming Data", use_container_width=True):
            st.session_state.current_page = "lab1_2"
            st.rerun()
        if st.button("Lab 1.3: Database Migration", use_container_width=True):
            st.session_state.current_page = "lab1_3"
            st.rerun()
        
        # Add more labs as needed...

# Render markdown content
def render_markdown(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            st.markdown(content)
    except Exception as e:
        st.error(f"Error loading content: {e}")

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
        render_markdown("content/study-guide/00-introduction.md")
        
    elif st.session_state.current_page == "domain1":
        st.title("Domain 1: Data Ingestion and Transformation")
        render_markdown("content/study-guide/01-data-ingestion-transformation.md")
        
    elif st.session_state.current_page == "domain2":
        st.title("Domain 2: Storage and Data Management")
        render_markdown("content/study-guide/02-storage-data-management.md")
        
    elif st.session_state.current_page == "domain3":
        st.title("Domain 3: Data Security and Access Control")
        render_markdown("content/study-guide/03-data-security-access-control.md")
        
    elif st.session_state.current_page == "domain4":
        st.title("Domain 4: Data Operations and Optimization")
        render_markdown("content/study-guide/04-data-operations-optimization.md")
        
    elif st.session_state.current_page == "exam_tips":
        st.title("Exam Preparation Tips")
        render_markdown("content/study-guide/05-exam-preparation-tips.md")
        
    elif st.session_state.current_page == "lab1_1":
        st.title("Lab 1.1: Batch Data Ingestion with AWS Glue")
        render_markdown("content/labs/data-ingestion/lab-1.1-batch-ingestion-glue.md")
        
    elif st.session_state.current_page == "lab1_2":
        st.title("Lab 1.2: Streaming Data with Amazon Kinesis")
        render_markdown("content/labs/data-ingestion/lab-1.2-streaming-kinesis.md")
        
    elif st.session_state.current_page == "lab1_3":
        st.title("Lab 1.3: Database Migration with AWS DMS")
        render_markdown("content/labs/data-ingestion/lab-1.3-database-migration-dms.md")
        
    # Add other pages as needed...

# Main app layout
sidebar_navigation()
main_content()

# Display app info in footer
st.sidebar.markdown("---")
st.sidebar.info("AWS Data Engineer Course v1.0")
