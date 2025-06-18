"""
Chat Page for AWS Data Engineer Course

This page provides a dedicated interface for interacting with the AI assistant.
"""

import streamlit as st
from app.components.chat_interface import display_chat_page

# Set page configuration
st.set_page_config(
    page_title="AI Assistant - AWS Data Engineer Course",
    page_icon="🤖",
    layout="wide"
)

# Display the chat page
display_chat_page()
