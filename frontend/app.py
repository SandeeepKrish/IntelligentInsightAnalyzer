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

# ============================================================================
# Authentication Check - Initialize State
# ============================================================================

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "session_token" not in st.session_state:
    st.session_state.session_token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Add backend src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend/src'))

from config import AppConfig
from services import AnalyzerService
from components import (
    render_chat_interface,
    render_data_explorer,
    render_data_quality,
    render_charts,
    render_advanced_analysis,
    render_theme_toggle,
    apply_custom_theme
)


# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="IntelligentInsightAnalyzer",
    page_icon="🤖",
    layout=AppConfig.LAYOUT,
    initial_sidebar_state=AppConfig.SIDEBAR_STATE
)

st.title("🔬 IntelligentInsightAnalyzer")
st.caption("AI-powered multi-domain data analysis with advanced temporal and aggregation analytics")

# ============================================================================
# Show Login Banner if Not Authenticated
# ============================================================================

if not st.session_state.authenticated:
    st.error("""
    🔐 **Please Login to Continue**
    
    Go to the **Login** page in the sidebar to authenticate with your email and OTP.
    """)
else:
    # Show logout option
    col1, col2, col3 = st.columns([10, 1, 1])
    with col3:
        if st.button("🚪 Logout"):
            import requests
            API_URL = "https://intelligentinsightanalyzer.onrender.com"  # Production backend
            try:
                requests.post(
                    f"{API_URL}/auth/logout",
                    json={"session_token": st.session_state.session_token},
                    timeout=10
                )
            except:
                pass
            st.session_state.authenticated = False
            st.session_state.session_token = None
            st.session_state.user_email = None
            st.success("✅ Logged out!")
            import time
            time.sleep(1)
            st.rerun()
    with col1:
        st.caption(f"👤 Logged in as: **{st.session_state.user_email}**")


# ============================================================================
# Initialize Session State
# ============================================================================

# Initialize session state variables for persistent file storage
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None  # Store DataFrame
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None  # Store filename
if "uploaded_pdfs" not in st.session_state:
    st.session_state.uploaded_pdfs = {}  # Store PDFs

@st.cache_resource
def get_analyzer_service():
    """Initialize the analyzer service (cached for session)"""
    return AnalyzerService()


# Get service with better error handling
try:
    service = get_analyzer_service()
except SystemExit:
    # SystemExit is raised by st.stop() - let it pass through
    st.stop()
except Exception as e:
    st.error(f"❌ Initialization Error: {str(e)}")
    st.info("""
    ### ⚙️ Setup Required
    
    To use IntelligentInsightAnalyzer, you need to configure your OpenAI API key:
    
    **For Streamlit Cloud Deployment:**
    1. Click the menu (⋯) → Settings → Secrets
    2. Add: `OPENAI_API_KEY = "sk-proj-..."`
    3. Click Save and wait 1 minute
    4. Refresh this page
    
    **Get an OpenAI API key:**
    - Visit: https://platform.openai.com/api-keys
    - Create a new API key (starts with `sk-proj-`)
    - Copy the complete key
    
    **Format for Streamlit Secrets:**
    ```
    OPENAI_API_KEY = "sk-proj-your-key-here"
    ```
    """)
    st.stop()


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
        # Check if PDF is already loaded
        if len(service.get_pdf_names()) > 0:
            st.error("⚠️ PDF file is already selected!")
            st.warning("""
            You cannot load both Excel/CSV and PDF files simultaneously.
            
            **To load an Excel/CSV file:**
            1. Click "🗑️ Clear All PDFs" below to remove PDF files
            2. Then upload your Excel/CSV file
            """)
        else:
            try:
                # Load the data
                df = service.load_data(uploaded_file.name, uploaded_file.getvalue())
                
                # Store in session_state for persistence across refreshes
                st.session_state.uploaded_data = df
                st.session_state.uploaded_filename = uploaded_file.name
                
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
    
    # If file was previously loaded, restore it from session_state
    elif st.session_state.uploaded_data is not None:
        st.success(f"✅ Loaded: {st.session_state.uploaded_filename}")
        df = st.session_state.uploaded_data
        service.current_dataframe = df
        service.data_context = service.data_analyzer.get_data_summary(df)
        
        # Display dataset stats
        st.metric("Rows", f"{len(df):,}")
        st.metric("Columns", len(df.columns))
        
        # Data quality score
        quality = service.get_data_quality_metrics()
        st.metric("Quality Score", f"{quality['quality_score']:.1f}%")
        
        st.session_state.file_loaded = True
    
    # PDF Upload Section
    st.divider()
    st.header("📄 PDF Documents")
    
    uploaded_pdf = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key="pdf_uploader"
    )
    
    if uploaded_pdf:
        # Check if Excel/CSV is already loaded
        if service.get_dataframe() is not None and not service.get_dataframe().empty:
            st.error("⚠️ Excel/CSV file is already selected!")
            st.warning("""
            You cannot load both Excel/CSV and PDF files simultaneously.
            
            **To load PDF files:**
            1. There's currently an Excel/CSV file loaded
            2. The chat interface will use the Excel/CSV data
            3. To use PDFs instead, you need to reload the page or clear the data
            """)
        else:
            for pdf_file in uploaded_pdf:
                try:
                    # Load the PDF
                    result = service.load_pdf(pdf_file.name, pdf_file.getvalue())
                    
                    if result["success"]:
                        st.success(result["message"])
                        # Set file_loaded flag so chat interface appears
                        st.session_state.file_loaded = True
                    else:
                        st.error(f"❌ {result['error']}")
                
                except Exception as e:
                    st.error(f"❌ Error loading PDF: {str(e)}")
    
    # Display loaded PDFs info
    pdf_count = len(service.get_pdf_names())
    if pdf_count > 0:
        st.info(f"📄 {pdf_count} PDF(s) loaded and ready for analysis")
        
        if st.button("🗑️ Clear All PDFs"):
            service.clear_pdfs()
            st.success("✅ All PDFs cleared!")
            st.rerun()
    
    # Display loaded Excel/CSV info
    if service.get_dataframe() is not None and not service.get_dataframe().empty:
        st.info("📊 Excel/CSV file is loaded")
        
        if st.button("🗑️ Clear Data File"):
            service.current_dataframe = None
            service.data_context = ""
            st.session_state.file_loaded = False
            st.session_state.uploaded_data = None
            st.session_state.uploaded_filename = None
            st.success("✅ Data file cleared!")
            st.rerun()
            st.success("✅ Data file cleared!")
            st.rerun()
    
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
    
    # Theme toggle at the bottom of sidebar
    render_theme_toggle()


# ============================================================================
# Apply Theme (Must be after theme toggle in sidebar)
# ============================================================================

if "theme" not in st.session_state:
    st.session_state.theme = "light"
apply_custom_theme(st.session_state.theme)

# Check if file is loaded
file_loaded = st.session_state.get("file_loaded", False)

if not file_loaded:
    # Welcome screen
    st.info("👈 Upload a CSV, Excel file, or PDF from the sidebar to begin")
    
    st.markdown("""
    ### ✨ Features
    - 🤖 **Multi-turn AI Conversations** - Ask follow-up questions with context
    - 💬 **Streaming Responses** - See AI answers appear in real-time
    - 📚 **Conversation Memory** - AI remembers previous questions
    - 📊 **Data Exploration** - Preview and explore your dataset
    - 🧹 **Data Quality** - Check data health metrics
    - 📈 **Custom Charts** - Create pie, bar, scatter, and line charts
    - 📄 **PDF Analysis** - Upload and analyze PDF documents with AI
    
 
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
st.caption("🔬 IntelligentInsightAnalyzer | Built with Streamlit & OpenAI | Version 2.0")
