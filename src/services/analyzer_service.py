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
from utils import ConversationMemory, StreamingLLM, DataAnalyzer


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
        
        # 1. Try Streamlit secrets first (for deployment)
        try:
            api_key = st.secrets.get("OPENAI_API_KEY")
        except:
            pass
        
        # 2. Try environment variables (for local development)
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        
        # 3. Try config file
        if not api_key:
            api_key = AppConfig.OPENAI_API_KEY
        
        if not api_key:
            st.error("❌ OPENAI_API_KEY not found. Please add it to Streamlit Cloud Secrets.")
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
        
        # Stream response
        full_response = ""
        try:
            for chunk in self.llm.analyze_data(
                data_context=self.data_context,
                question=question,
                messages=messages
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
