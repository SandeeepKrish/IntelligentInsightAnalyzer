"""
Analyzer Service - Orchestrates data analysis and LLM interactions
Business logic layer that coordinates between utils and UI components
"""

import pandas as pd
import io
import os
import streamlit as st
from typing import Dict, Any, Generator

from config import AppConfig
from utils import ConversationMemory, StreamingLLM, DataAnalyzer, PDFHandler


class AnalyzerService:
    """High-level service for data analysis and AI interactions"""
    
    def __init__(self):
        """Initialize the analyzer service"""
        self.conversation_memory = ConversationMemory(
            max_messages=AppConfig.MAX_CONVERSATION_MESSAGES,
            system_context=AppConfig.SYSTEM_PROMPT
        )
        
        # Check multiple sources for API key
        api_key = None
        
        # 1. Try Streamlit secrets first (for deployment - PREFERRED)
        try:
            api_key = st.secrets.get("OPENAI_API_KEY")
        except (AttributeError, KeyError, FileNotFoundError):
            # st.secrets not available or key not found
            pass
        
        # 2. Try environment variables (for local development)
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            st.error("❌ OPENAI_API_KEY not found. Please add it to Streamlit Cloud Secrets or environment variables.")
            st.info("""
            ### ⚙️ Setup Required
            
            1. **Add your OpenAI API key** to Streamlit Cloud Secrets:
               - Click the menu (⋯) → Settings → Secrets
               - Add: `OPENAI_API_KEY = "sk-proj-..."`
               - Click Save and wait 1 minute
               - Refresh this page
            
            2. **Get an OpenAI API key:**
               - Visit: https://platform.openai.com/api-keys
               - Create a new API key
               - Copy the key starting with `sk-proj-`
            """)
            st.stop()
        
        try:
            self.llm = StreamingLLM(
                model=AppConfig.OPENAI_MODEL,
                temperature=AppConfig.OPENAI_TEMPERATURE,
                max_tokens=AppConfig.OPENAI_MAX_TOKENS,
                api_key=api_key  # Pass key directly
            )
        except ValueError as e:
            st.error(f"❌ LLM initialization failed: {str(e)}")
            st.stop()
        
        self.data_analyzer = DataAnalyzer()
        self.current_dataframe = None
        self.data_context = ""
        
        # PDF document storage
        self.pdf_documents = {}  # {filename: {content, text, metadata}}
        self.current_pdf = None  # Currently selected PDF for chat
    
    def load_data(self, filename: str, file_data: bytes) -> pd.DataFrame:
        """
        Load CSV or Excel file
        
        Args:
            filename: Name of the file
            file_data: File content as bytes
            
        Returns:
            Loaded DataFrame
        """
        if filename.lower().endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_data))
        else:
            df = pd.read_excel(io.BytesIO(file_data))
        
        self.current_dataframe = df
        self.data_context = self.data_analyzer.get_data_summary(df)
        
        return df
    
    def stream_chat_response(self, question: str) -> Generator[str, None, None]:
        """
        Stream AI response for a user question
        
        Args:
            question: User's question about the data
            
        Yields:
            Response chunks as they arrive from the LLM
        """
        # Add user message to memory
        self.conversation_memory.add_message("user", question)
        
        # Get conversation context
        messages = self.conversation_memory.get_recent_context(
            window_size=AppConfig.RECENT_CONTEXT_WINDOW
        )
        
        # Get PDF content if a PDF is selected
        pdf_content = None
        if self.current_pdf:
            pdf_text = self.get_pdf_text()
            if pdf_text:
                # Limit PDF content to first 3000 characters to avoid token limits
                pdf_content = pdf_text[:3000] if len(pdf_text) > 3000 else pdf_text
        
        # Stream response
        full_response = ""
        try:
            for chunk in self.llm.analyze_data(
                data_context=self.data_context,
                question=question,
                messages=messages,
                pdf_content=pdf_content
            ):
                full_response += chunk
                yield chunk
            
            # Add assistant message to memory after streaming completes
            self.conversation_memory.add_message("assistant", full_response)
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            yield error_msg
            self.conversation_memory.add_message("assistant", error_msg)
    
    def get_conversation_history(self) -> list:
        """Get current conversation history"""
        return self.conversation_memory.messages
    
    def clear_conversation(self) -> None:
        """Clear conversation history"""
        self.conversation_memory.clear_history()
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get conversation metadata"""
        return self.conversation_memory.get_summary()
    
    # ========================================================================
    # Data Analysis Methods
    # ========================================================================
    
    def get_data_quality_metrics(self) -> Dict[str, Any]:
        """Get data quality metrics"""
        if self.current_dataframe is None:
            return {}
        return self.data_analyzer.get_quality_metrics(self.current_dataframe)
    
    def get_column_types(self) -> Dict[str, list]:
        """Get columns grouped by data type"""
        if self.current_dataframe is None:
            return {}
        return self.data_analyzer.get_column_types(self.current_dataframe)
    
    def get_data_insights(self, num_insights: int = 5) -> list:
        """Get top data insights"""
        if self.current_dataframe is None:
            return []
        return self.data_analyzer.get_top_insights(self.current_dataframe, num_insights)
    
    def get_dataframe(self) -> pd.DataFrame:
        """Get current dataframe"""
        return self.current_dataframe
    
    def get_dataframe_preview(self, rows: int = 100) -> pd.DataFrame:
        """Get dataframe preview"""
        if self.current_dataframe is None:
            return pd.DataFrame()
        return self.current_dataframe.head(rows)
    
    def get_numeric_columns(self) -> list:
        """Get list of numeric columns"""
        if self.current_dataframe is None:
            return []
        col_types = self.get_column_types()
        return col_types.get("numeric", [])
    
    def get_categorical_columns(self) -> list:
        """Get list of categorical columns"""
        if self.current_dataframe is None:
            return []
        col_types = self.get_column_types()
        return col_types.get("categorical", [])

    # ========================================================================
    # PDF Document Handling Methods
    # ========================================================================
    
    def load_pdf(self, filename: str, file_data: bytes) -> Dict[str, Any]:
        """
        Load and process a PDF document
        
        Args:
            filename: Name of the PDF file
            file_data: PDF file content as bytes
            
        Returns:
            Dictionary with PDF metadata and extraction status
        """
        try:
            # Validate PDF
            is_valid, message = PDFHandler.validate_pdf(file_data)
            if not is_valid:
                return {"success": False, "error": message}
            
            # Get metadata
            metadata = PDFHandler.get_pdf_metadata(file_data)
            
            # Extract text
            text = PDFHandler.extract_text_from_pdf(file_data)
            
            # Store in documents dict
            self.pdf_documents[filename] = {
                "content": file_data,
                "text": text,
                "metadata": metadata
            }
            
            # Set as current PDF
            self.current_pdf = filename
            
            return {
                "success": True,
                "filename": filename,
                "pages": metadata.get("num_pages", 0),
                "message": f"✅ Loaded: {filename} ({metadata.get('num_pages', 0)} pages)"
            }
        
        except Exception as e:
            return {"success": False, "error": f"Error loading PDF: {str(e)}"}
    
    def get_pdf_names(self) -> list:
        """Get list of loaded PDF filenames"""
        return list(self.pdf_documents.keys())
    
    def set_current_pdf(self, filename: str = None) -> None:
        """Set the current PDF for chat analysis"""
        if filename is None or filename in self.pdf_documents:
            self.current_pdf = filename
    
    def get_current_pdf(self) -> str:
        """Get currently selected PDF filename"""
        return self.current_pdf
    
    def get_pdf_text(self, filename: str = None) -> str:
        """
        Get text content of a PDF
        
        Args:
            filename: PDF filename (None = current PDF)
            
        Returns:
            Extracted PDF text
        """
        if filename is None:
            filename = self.current_pdf
        
        if filename and filename in self.pdf_documents:
            return self.pdf_documents[filename]["text"]
        
        return ""
    
    def get_pdf_metadata(self, filename: str = None) -> Dict[str, Any]:
        """
        Get metadata of a PDF
        
        Args:
            filename: PDF filename (None = current PDF)
            
        Returns:
            PDF metadata dictionary
        """
        if filename is None:
            filename = self.current_pdf
        
        if filename and filename in self.pdf_documents:
            return self.pdf_documents[filename]["metadata"]
        
        return {}
    
    def clear_pdfs(self) -> None:
        """Clear all loaded PDF documents"""
        self.pdf_documents = {}
        self.current_pdf = None
