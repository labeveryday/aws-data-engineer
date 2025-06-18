"""
Progress dashboard page for the AWS Data Engineer Course.
"""

import streamlit as st
from app.utils.progress_tracker import ProgressTracker
from app.components.progress_display import display_progress_dashboard
from app.config import DOMAINS, LABS

# Set page configuration
st.set_page_config(
    page_title="Progress Dashboard - AWS Data Engineer Course",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize progress tracker
tracker = ProgressTracker()

# Display the progress dashboard
display_progress_dashboard(tracker, DOMAINS, LABS)

# Add a link back to the main app
st.markdown("---")
if st.button("← Back to Main Content", use_container_width=True):
    st.switch_page("main.py")
