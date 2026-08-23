"""
Chat Interface Component
Handles multi-turn conversation UI with streaming responses
"""

import streamlit as st
from services import AnalyzerService


def render_chat_interface(service: AnalyzerService):
    """
    Render the chat interface tab with professional styling
    
    Args:
        service: AnalyzerService instance
    """
    st.subheader("💬 Chat with Your Data")
    
    # Apply custom chat styling
    apply_chat_styling()
    
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


def apply_chat_styling():
    """
    Apply professional chat UI styling with custom CSS
    """
    # Get current theme
    theme = "dark" if st.session_state.get("theme") == "dark" else "light"
    
    if theme == "dark":
        # Dark mode styling - AGGRESSIVE BLACK INPUT BOX
        chat_css = """
        <style>
            /* ===== CHAT INPUT CONTAINER - ALL BLACK ===== */
            .stChatInput {
                background-color: transparent !important;
            }
            
            /* Input wrapper */
            .stChatInput > div {
                background-color: #0e1117 !important;
                padding: 12px !important;
                border-radius: 10px !important;
                border: 1px solid #30363d !important;
            }
            
            /* ===== INPUT BOX - COMPLETELY BLACK ===== */
            .stChatInput input,
            [data-testid="stChatInputTextArea"] input {
                background-color: #0a0e13 !important;
                color: #e6edf3 !important;
                border: none !important;
                caret-color: #58a6ff !important;
                font-size: 16px !important;
                padding: 12px 16px !important;
                border-radius: 8px !important;
            }
            
            /* Focus state */
            .stChatInput input:focus,
            [data-testid="stChatInputTextArea"] input:focus {
                background-color: #161b22 !important;
                color: #e6edf3 !important;
                border: 2px solid #58a6ff !important;
                outline: none !important;
            }
            
            /* Placeholder text - white */
            .stChatInput input::placeholder,
            [data-testid="stChatInputTextArea"] input::placeholder {
                color: #8b949e !important;
                opacity: 1 !important;
            }
            
            /* Text area styling */
            textarea {
                background-color: #0a0e13 !important;
                color: #e6edf3 !important;
                caret-color: #58a6ff !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 12px 16px !important;
            }
            
            textarea:focus {
                background-color: #161b22 !important;
                border: 2px solid #58a6ff !important;
                outline: none !important;
            }
            
            textarea::placeholder {
                color: #8b949e !important;
                opacity: 1 !important;
            }
            
            /* ===== SEND BUTTON - PROFESSIONAL GREEN ARROW ===== */
            [data-testid="chatInputSubmitButton"] {
                background-color: transparent !important;
                border: none !important;
                padding: 8px 12px !important;
            }
            
            [data-testid="chatInputSubmitButton"] button {
                background-color: #238636 !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 10px 14px !important;
                cursor: pointer !important;
                transition: all 0.2s ease !important;
            }
            
            [data-testid="chatInputSubmitButton"] button:hover {
                background-color: #2ea043 !important;
                transform: scale(1.05) !important;
            }
            
            [data-testid="chatInputSubmitButton"] button:active {
                background-color: #1f6feb !important;
            }
            
            /* Arrow icon styling */
            [data-testid="chatInputSubmitButton"] svg {
                fill: white !important;
                stroke: white !important;
                width: 20px !important;
                height: 20px !important;
            }
            
            /* ===== CURSOR STYLING ===== */
            input::selection,
            textarea::selection {
                background-color: #58a6ff !important;
                color: #0a0e13 !important;
            }
        </style>
        """
    else:
        # Light mode styling
        chat_css = """
        <style>
            /* ===== CHAT INPUT CONTAINER - LIGHT ===== */
            .stChatInput {
                background-color: transparent !important;
            }
            
            /* Input wrapper */
            .stChatInput > div {
                background-color: #ffffff !important;
                padding: 12px !important;
                border-radius: 10px !important;
                border: 1px solid #d3d3d3 !important;
            }
            
            /* ===== INPUT BOX - WHITE WITH DARK TEXT ===== */
            .stChatInput input,
            [data-testid="stChatInputTextArea"] input {
                background-color: #ffffff !important;
                color: #262730 !important;
                border: none !important;
                caret-color: #0066cc !important;
                font-size: 16px !important;
                padding: 12px 16px !important;
                border-radius: 8px !important;
            }
            
            /* Focus state */
            .stChatInput input:focus,
            [data-testid="stChatInputTextArea"] input:focus {
                background-color: #f0f2f6 !important;
                color: #262730 !important;
                border: 2px solid #0066cc !important;
                outline: none !important;
            }
            
            /* Placeholder text */
            .stChatInput input::placeholder,
            [data-testid="stChatInputTextArea"] input::placeholder {
                color: #8b949e !important;
                opacity: 1 !important;
            }
            
            /* Text area styling */
            textarea {
                background-color: #ffffff !important;
                color: #262730 !important;
                caret-color: #0066cc !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 12px 16px !important;
            }
            
            textarea:focus {
                background-color: #f0f2f6 !important;
                border: 2px solid #0066cc !important;
                outline: none !important;
            }
            
            textarea::placeholder {
                color: #8b949e !important;
                opacity: 1 !important;
            }
            
            /* ===== SEND BUTTON - GREEN ===== */
            [data-testid="chatInputSubmitButton"] {
                background-color: transparent !important;
                border: none !important;
                padding: 8px 12px !important;
            }
            
            [data-testid="chatInputSubmitButton"] button {
                background-color: #28a745 !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 10px 14px !important;
                cursor: pointer !important;
                transition: all 0.2s ease !important;
            }
            
            [data-testid="chatInputSubmitButton"] button:hover {
                background-color: #218838 !important;
                transform: scale(1.05) !important;
            }
            
            [data-testid="chatInputSubmitButton"] button:active {
                background-color: #0066cc !important;
            }
            
            /* Arrow icon styling */
            [data-testid="chatInputSubmitButton"] svg {
                fill: white !important;
                stroke: white !important;
                width: 20px !important;
                height: 20px !important;
            }
            
            /* ===== CURSOR STYLING ===== */
            input::selection,
            textarea::selection {
                background-color: #0066cc !important;
                color: white !important;
            }
        </style>
        """
    
    st.markdown(chat_css, unsafe_allow_html=True)
