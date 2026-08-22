"""
AI Data Analyst Chatbot - Main Application
Professional entry point with clean architecture

Architecture:
- config/     : Centralized configuration
- services/   : Business logic orchestration
- components/ : Reusable UI components
- utils/      : Core utilities (memory, LLM, data analysis)
"""

import streamlit as st
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import AppConfig
from services import AnalyzerService
from components import (
    render_chat_interface,
    render_data_explorer,
    render_data_quality,
    render_charts,
    render_advanced_analysis
)


# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title=AppConfig.APP_TITLE,
    page_icon=AppConfig.APP_ICON,
    layout=AppConfig.LAYOUT,
    initial_sidebar_state=AppConfig.SIDEBAR_STATE
)

st.title(AppConfig.APP_TITLE)
st.caption(AppConfig.APP_DESCRIPTION)


# ============================================================================
# Initialize Session State
# ============================================================================

@st.cache_resource
def get_analyzer_service():
    """Initialize the analyzer service (cached for session)"""
    try:
        return AnalyzerService()
    except ValueError as e:
        st.error(f"❌ {str(e)}")
        st.stop()


# Get service
service = get_analyzer_service()


# ============================================================================
# Sidebar - File Upload & Controls
# ============================================================================

with st.sidebar:
    st.header("📁 Data Upload")
    
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=AppConfig.ALLOWED_FILE_TYPES
    )
    
    if uploaded_file is not None:
        try:
            # Load the data
            df = service.load_data(uploaded_file.name, uploaded_file.getvalue())
            
            st.success(f"✅ Loaded: {uploaded_file.name}")
            
            # Display dataset stats
            st.metric("Rows", f"{len(df):,}")
            st.metric("Columns", len(df.columns))
            
            # Data quality score
            quality = service.get_data_quality_metrics()
            st.metric("Quality Score", f"{quality['quality_score']:.1f}%")
            
            # Store in session state that file is loaded
            st.session_state.file_loaded = True
        
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.session_state.file_loaded = False
    
    # Conversation controls
    st.divider()
    st.header("💬 Conversation")
    
    if st.button("🔄 Clear Chat History"):
        service.clear_conversation()
        st.success("✅ Chat history cleared!")
        st.rerun()
    
    if st.session_state.get("file_loaded", False):
        summary = service.get_conversation_summary()
        st.caption(f"📊 Messages in chat: {summary['total_messages']}")


# ============================================================================
# Main Content Area
# ============================================================================

# Check if file is loaded
file_loaded = st.session_state.get("file_loaded", False)

if not file_loaded:
    # Welcome screen
    st.info("👈 Upload a CSV or Excel file from the sidebar to begin")
    
    st.markdown("""
    ### ✨ Features
    - 🤖 **Multi-turn AI Conversations** - Ask follow-up questions with context
    - 💬 **Streaming Responses** - See AI answers appear in real-time
    - 📚 **Conversation Memory** - AI remembers previous questions
    - 📊 **Data Exploration** - Preview and explore your dataset
    - 🧹 **Data Quality** - Check data health metrics
    - 📈 **Custom Charts** - Create pie, bar, scatter, and line charts
    
 
    """)

else:
    # Create tabs for different features
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 AI Chat", "📊 Data Explorer", "🧹 Data Quality", "📈 Charts", "🔬 Advanced Analysis"])
    
    # Render components
    with tab1:
        render_chat_interface(service)
    
    with tab2:
        render_data_explorer(service)
    
    with tab3:
        render_data_quality(service)
    
    with tab4:
        render_charts(service)
    
    with tab5:
        render_advanced_analysis(service)


# ============================================================================
# Footer
# ============================================================================

st.divider()
st.caption("🤖 AI Data Analyst Chatbot | Built with Streamlit & OpenAI | Version 2.0")
