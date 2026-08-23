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
        # Dark mode styling
        chat_css = """
        <style>
            /* ===== REMOVE NESTED BOXES - FLAT DESIGN ===== */
            [data-testid="stChatMessage"] {
                background-color: #161b22 !important;
                border: 1px solid #30363d !important;
                border-radius: 12px !important;
                padding: 16px !important;
                margin: 8px 0 !important;
            }
            
            /* Remove inner container backgrounds */
            [data-testid="stChatMessage"] > div {
                background-color: transparent !important;
            }
            
            /* Chat message text - white */
            [data-testid="stChatMessage"] * {
                background-color: transparent !important;
                color: #e6edf3 !important;
            }
            
            /* Ensure text is white */
            [data-testid="stChatMessage"] p,
            [data-testid="stChatMessage"] span,
            [data-testid="stChatMessage"] div {
                color: #e6edf3 !important;
            }
            
            /* ===== CHAT INPUT STYLING ===== */
            .stChatInput {
                background-color: #0e1117 !important;
            }
            
            .stChatInput input {
                background-color: #161b22 !important;
                color: #e6edf3 !important;
                border: 2px solid #30363d !important;
                border-radius: 10px !important;
                padding: 12px 16px !important;
            }
            
            .stChatInput input::placeholder {
                color: #8b949e !important;
            }
            
            /* ===== SEND BUTTON - GREEN ARROW ===== */
            [data-testid="chatInputSubmitButton"] {
                background-color: #238636 !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 10px 12px !important;
            }
            
            [data-testid="chatInputSubmitButton"] button {
                background-color: #238636 !important;
                color: white !important;
                border: none !important;
            }
            
            [data-testid="chatInputSubmitButton"] button:hover {
                background-color: #2ea043 !important;
            }
            
            [data-testid="chatInputSubmitButton"] svg {
                fill: white !important;
                stroke: white !important;
            }
            
            /* ===== ASSISTANT MESSAGE SPECIFIC ===== */
            .stChatMessage[data-testid="assistant-message"] {
                background: linear-gradient(135deg, #161b22, #0d1117) !important;
                border-left: 4px solid #238636 !important;
            }
            
            /* ===== USER MESSAGE SPECIFIC ===== */
            .stChatMessage[data-testid="user-message"] {
                background: linear-gradient(135deg, #1f6feb, #0d47a1) !important;
                border-left: 4px solid #58a6ff !important;
                margin-left: 20px !important;
            }
        </style>
        """
    else:
        # Light mode styling
        chat_css = """
        <style>
            /* ===== REMOVE NESTED BOXES - FLAT DESIGN ===== */
            [data-testid="stChatMessage"] {
                background-color: #f0f2f6 !important;
                border: 1px solid #d3d3d3 !important;
                border-radius: 12px !important;
                padding: 16px !important;
                margin: 8px 0 !important;
            }
            
            /* Remove inner container backgrounds */
            [data-testid="stChatMessage"] > div {
                background-color: transparent !important;
            }
            
            /* Chat message text - dark */
            [data-testid="stChatMessage"] * {
                background-color: transparent !important;
                color: #262730 !important;
            }
            
            /* Ensure text is dark */
            [data-testid="stChatMessage"] p,
            [data-testid="stChatMessage"] span,
            [data-testid="stChatMessage"] div {
                color: #262730 !important;
            }
            
            /* ===== CHAT INPUT STYLING ===== */
            .stChatInput {
                background-color: #ffffff !important;
            }
            
            .stChatInput input {
                background-color: #f0f2f6 !important;
                color: #262730 !important;
                border: 2px solid #d3d3d3 !important;
                border-radius: 10px !important;
                padding: 12px 16px !important;
            }
            
            .stChatInput input::placeholder {
                color: #8b949e !important;
            }
            
            /* ===== SEND BUTTON - GREEN ARROW ===== */
            [data-testid="chatInputSubmitButton"] {
                background-color: #28a745 !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 10px 12px !important;
            }
            
            [data-testid="chatInputSubmitButton"] button {
                background-color: #28a745 !important;
                color: white !important;
                border: none !important;
            }
            
            [data-testid="chatInputSubmitButton"] button:hover {
                background-color: #218838 !important;
            }
            
            [data-testid="chatInputSubmitButton"] svg {
                fill: white !important;
                stroke: white !important;
            }
            
            /* ===== ASSISTANT MESSAGE SPECIFIC ===== */
            .stChatMessage[data-testid="assistant-message"] {
                background: linear-gradient(135deg, #f0f2f6, #ffffff) !important;
                border-left: 4px solid #28a745 !important;
            }
            
            /* ===== USER MESSAGE SPECIFIC ===== */
            .stChatMessage[data-testid="user-message"] {
                background: linear-gradient(135deg, #e3f2fd, #c8e6c9) !important;
                border-left: 4px solid #0066cc !important;
                margin-left: 20px !important;
            }
        </style>
        """
    
    st.markdown(chat_css, unsafe_allow_html=True)
