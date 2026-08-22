"""
Chat Interface Component
Handles multi-turn conversation UI with streaming responses
"""

import streamlit as st
from services import AnalyzerService


def render_chat_interface(service: AnalyzerService):
    """
    Render the chat interface tab
    
    Args:
        service: AnalyzerService instance
    """
    st.subheader("💬 Chat with Your Data")
    
    # Container for conversation history
    chat_container = st.container()
    
    with chat_container:
        # Display conversation history
        if len(service.get_conversation_history()) == 0:
            st.info("👋 Start a conversation! Ask questions about your data and I'll analyze it for you.")
        else:
            for msg in service.get_conversation_history():
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
    
    # Divider
    st.divider()
    
    # Chat input (ChatGPT style - at the bottom)
    question = st.chat_input(
        "Ask a question about your data...",
        key="chat_input"
    )
    
    if question:
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(question)
        
        # Stream AI response
        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""
            
            try:
                # Stream the response
                for chunk in service.stream_chat_response(question):
                    full_response += chunk
                    response_container.markdown(full_response + "▌")  # Cursor effect
                
                # Final response without cursor
                response_container.markdown(full_response)
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        # Auto-scroll to bottom
        st.rerun()
