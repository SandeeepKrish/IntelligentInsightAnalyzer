"""
Application Configuration Settings
"""

import os
from dotenv import load_dotenv

# Load environment variables ONCE at startup
load_dotenv()


class AppConfig:
    """Centralized application configuration"""
    
    # App metadata
    APP_TITLE = "🔬 IntelligentInsightAnalyzer"
    APP_ICON = "🔬"
    APP_DESCRIPTION = "AI-powered multi-domain data analysis with advanced temporal, aggregation, and filtering capabilities"
    
    # Streamlit config
    LAYOUT = "wide"
    SIDEBAR_STATE = "expanded"
    
    # OpenAI config
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-3.5-turbo"
    OPENAI_TEMPERATURE = 0.7
    OPENAI_MAX_TOKENS = 1000
    
    # Conversation config
    MAX_CONVERSATION_MESSAGES = 20
    RECENT_CONTEXT_WINDOW = 6
    
    # Data config
    ALLOWED_FILE_TYPES = ["csv", "xlsx", "xls"]
    MAX_FILE_SIZE_MB = 100
    
    # UI config
    CHART_TYPES = ["Pie Chart", "Bar Chart", "Scatter Plot", "Line Chart", "Box Plot"]
    HISTOGRAM_BINS = 30
    
    # System prompts
    SYSTEM_PROMPT = """You are an expert data analyst AI assistant. Your role is to analyze the provided dataset and answer user questions about it.

IMPORTANT INSTRUCTIONS:
1. ALWAYS reference the actual data provided in the dataset context
2. Use specific numbers, percentages, and statistics from the data
3. Never say you don't have access to data - analyze what's provided
4. Focus on answering the user's specific question about their data
5. If data is missing for a specific metric, explain what you DO see in the data
6. Provide actionable insights based on the actual dataset
7. Be concise but thorough in your analysis"""
    
    @staticmethod
    def validate_config():
        """Validate critical configuration"""
        if not AppConfig.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return True
