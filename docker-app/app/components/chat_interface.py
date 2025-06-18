"""
Chat Interface Component for AWS Data Engineer Course

This module implements a Streamlit-based chat interface for interacting with the multi-agent system.
"""

import streamlit as st
from typing import Callable, Optional

def initialize_chat_state():
    """Initialize the chat state in the session state if it doesn't exist."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chat_placeholder" not in st.session_state:
        st.session_state.chat_placeholder = None

def display_chat_messages():
    """Display all messages in the chat history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def add_user_message(message: str):
    """Add a user message to the chat history."""
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user"):
        st.markdown(message)

def add_assistant_message(message: str):
    """Add an assistant message to the chat history."""
    st.session_state.messages.append({"role": "assistant", "content": message})
    with st.chat_message("assistant"):
        st.markdown(message)

def chat_interface(process_message_func: Callable[[str], str], placeholder: Optional[st.empty] = None):
    """
    Render a chat interface that processes user input with the provided function.
    
    Args:
        process_message_func: Function that takes a user message and returns an assistant response
        placeholder: Optional streamlit placeholder for the chat interface
    """
    # Initialize chat state
    initialize_chat_state()
    
    # Use provided placeholder or create a new one
    if placeholder:
        st.session_state.chat_placeholder = placeholder
    elif not st.session_state.chat_placeholder:
        st.session_state.chat_placeholder = st.empty()
    
    # Display existing chat messages
    with st.session_state.chat_placeholder.container():
        display_chat_messages()
        
        # Get user input
        if prompt := st.chat_input("Ask about AWS data engineering..."):
            # Add user message to chat history
            add_user_message(prompt)
            
            # Process the message and get a response
            with st.spinner("Thinking..."):
                response = process_message_func(prompt)
            
            # Add assistant response to chat history
            add_assistant_message(response)

def streaming_chat_interface(process_message_stream_func: Callable[[str], str], placeholder: Optional[st.empty] = None):
    """
    Render a chat interface with streaming responses.
    
    Args:
        process_message_stream_func: Function that takes a user message and yields response chunks
        placeholder: Optional streamlit placeholder for the chat interface
    """
    # Initialize chat state
    initialize_chat_state()
    
    # Use provided placeholder or create a new one
    if placeholder:
        st.session_state.chat_placeholder = placeholder
    elif not st.session_state.chat_placeholder:
        st.session_state.chat_placeholder = st.empty()
    
    # Display existing chat messages
    with st.session_state.chat_placeholder.container():
        display_chat_messages()
        
        # Get user input
        if prompt := st.chat_input("Ask about AWS data engineering..."):
            # Add user message to chat history
            add_user_message(prompt)
            
            # Create a placeholder for the assistant's response
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                
                # Process the message and stream the response
                for response_chunk in process_message_stream_func(prompt):
                    full_response += response_chunk
                    response_placeholder.markdown(full_response + "▌")
                
                # Update with the final response
                response_placeholder.markdown(full_response)
            
            # Add the complete assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
