"""
OpenAI LLM Interface with Streaming Support
"""

import os
from typing import Generator, List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class StreamingLLM:
    """Wrapper for OpenAI API with streaming capabilities"""
    
    def __init__(self, model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens: int = 500, api_key: str = None):
        """
        Initialize LLM client
        
        Args:
            model: OpenAI model name
            temperature: Response creativity (0-1)
            max_tokens: Maximum response length
            api_key: OpenAI API key (optional, will try environment if not provided)
        """
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def stream_response(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        """
        Stream response from OpenAI API
        
        Args:
            messages: Conversation messages
            
        Yields:
            Chunks of response text as they arrive
        """
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def get_full_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Get full response without streaming (for non-streaming use)
        
        Args:
            messages: Conversation messages
            
        Returns:
            Full response text
        """
        full_response = ""
        for chunk in self.stream_response(messages):
            full_response += chunk
        return full_response
    
    def analyze_data(self, data_context: str, question: str, messages: List[Dict[str, str]], pdf_content: str = None) -> Generator[str, None, None]:
        """
        Analyze data and stream response
        
        Args:
            data_context: Dataset summary/context
            question: User's question about the data
            messages: Conversation history
            pdf_content: Optional PDF document content for analysis
            
        Yields:
            Streamed response chunks
        """
        # Enhance the prompt with data context
        enhanced_messages = messages.copy()
        
        # Build the system prompt with data and PDF context
        system_prompt = """You are an expert data analyst AI assistant. Your role is to analyze the provided dataset and documents, and answer user questions comprehensively.

IMPORTANT INSTRUCTIONS:
1. ALWAYS reference the actual data provided in the context below
2. Use specific numbers, percentages, and statistics from the data
3. Never say you don't have access to data - analyze what's provided
4. Focus on answering the user's specific question
5. If data is missing for a specific metric, explain what you DO see in the data
6. Provide actionable insights based on the actual dataset and documents
7. When analyzing PDF content, extract relevant information and relate it to the user's question
8. Be thorough and cite specific information from the documents"""
        
        # Add dataset context
        if data_context:
            system_prompt += f"\n\nDataset Context:\n{data_context}"
        
        # Add PDF content if provided
        if pdf_content:
            system_prompt += f"\n\nDocument Content:\n{pdf_content}"
        
        system_prompt += f"\n\nUser Question: {question}\n\nAnalyze this information thoroughly and provide specific insights based on what's actually provided."
        
        # Replace or add system message
        if enhanced_messages and enhanced_messages[0]["role"] == "system":
            enhanced_messages[0]["content"] = system_prompt
        else:
            enhanced_messages.insert(0, {
                "role": "system",
                "content": system_prompt
            })
        
        yield from self.stream_response(enhanced_messages)
