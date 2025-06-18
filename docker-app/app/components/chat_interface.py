"""
Chat Interface Component for AWS Data Engineer Course

This module implements the Streamlit chat interface for interacting with the multi-agent system.
"""

import streamlit as st
from typing import List, Dict, Any
from app.agents import get_coordinator
from app.config import BEDROCK_MODEL_ID


def initialize_chat():
    """Initialize chat-related session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "coordinator" not in st.session_state:
        try:
            st.session_state.coordinator = get_coordinator(BEDROCK_MODEL_ID)
        except Exception as e:
            st.error(f"Failed to initialize AI assistant: {str(e)}")
            st.session_state.coordinator = None


def display_chat_interface():
    """Display the main chat interface."""
    st.subheader("🤖 AI Assistant")
    st.markdown("Ask questions about AWS data engineering concepts, get study guidance, or request help with labs.")
    
    # Initialize chat
    initialize_chat()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about AWS data engineering..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            if st.session_state.coordinator:
                try:
                    with st.spinner("Thinking..."):
                        # Get context from recent messages
                        context = get_conversation_context()
                        response = st.session_state.coordinator.route_question(prompt, context)
                    
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                error_msg = "AI assistant is not available. Please check your AWS configuration."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})


def display_chat_sidebar():
    """Display chat-related controls in the sidebar."""
    with st.sidebar:
        st.markdown("---")
        st.subheader("💬 AI Assistant")
        
        # Show agent capabilities
        if st.button("Show Agent Capabilities", use_container_width=True):
            show_agent_capabilities()
        
        # Clear chat history
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        # Chat statistics
        if "messages" in st.session_state and st.session_state.messages:
            total_messages = len(st.session_state.messages)
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.caption(f"💬 {user_messages} questions asked")


def show_agent_capabilities():
    """Display information about agent capabilities."""
    st.subheader("🤖 AI Assistant Capabilities")
    
    if st.session_state.coordinator:
        capabilities = st.session_state.coordinator.get_agent_capabilities()
        
        for agent_name, agent_capabilities in capabilities.items():
            with st.expander(f"**{agent_name} Agent**"):
                for capability in agent_capabilities:
                    st.write(f"• {capability}")
    else:
        st.error("AI assistant not available")


def get_conversation_context(max_messages: int = 4) -> str:
    """
    Get recent conversation context for the AI assistant.
    
    Args:
        max_messages: Maximum number of recent messages to include
        
    Returns:
        Formatted conversation context
    """
    if "messages" not in st.session_state or not st.session_state.messages:
        return ""
    
    # Get recent messages
    recent_messages = st.session_state.messages[-max_messages:]
    
    context_parts = []
    for message in recent_messages:
        role = message["role"]
        content = message["content"]
        context_parts.append(f"{role.title()}: {content}")
    
    return "\n".join(context_parts)


def display_quick_actions():
    """Display quick action buttons for common questions."""
    st.subheader("🚀 Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Show My Progress", use_container_width=True):
            add_quick_question("Show me my current progress through the course")
        
        if st.button("💡 Get Recommendations", use_container_width=True):
            add_quick_question("What should I study next based on my progress?")
    
    with col2:
        if st.button("📚 Explain AWS Glue", use_container_width=True):
            add_quick_question("Explain AWS Glue and its key features for data engineering")
        
        if st.button("🏗️ Data Lake Architecture", use_container_width=True):
            add_quick_question("What are the best practices for designing a data lake architecture on AWS?")


def add_quick_question(question: str):
    """
    Add a quick question to the chat and process it.
    
    Args:
        question: The question to add and process
    """
    # Initialize chat if needed
    initialize_chat()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": question})
    
    # Process the question
    if st.session_state.coordinator:
        try:
            context = get_conversation_context()
            response = st.session_state.coordinator.route_question(question, context)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = f"Error processing question: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Rerun to show the new messages
    st.rerun()


def display_chat_page():
    """Display a dedicated chat page."""
    st.title("🤖 AI Assistant Chat")
    
    # Quick actions at the top
    display_quick_actions()
    
    st.markdown("---")
    
    # Main chat interface
    display_chat_interface()
    
    # Sidebar controls
    display_chat_sidebar()


def display_embedded_chat():
    """Display a compact chat interface for embedding in other pages."""
    with st.expander("🤖 Ask AI Assistant", expanded=False):
        st.markdown("Get instant help with AWS data engineering concepts!")
        
        # Simple chat input
        if prompt := st.text_input("Your question:", key="embedded_chat"):
            if st.button("Ask", key="embedded_ask"):
                initialize_chat()
                
                if st.session_state.coordinator:
                    try:
                        with st.spinner("Getting answer..."):
                            response = st.session_state.coordinator.route_question(prompt)
                        
                        st.success("**Answer:**")
                        st.markdown(response)
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("AI assistant not available")
