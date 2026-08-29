"""
Conversation Memory Management System
Handles temporary memory for multi-turn conversations with context awareness
"""

from typing import List, Dict, Any
from datetime import datetime
import json


class ConversationMemory:
    """Manages conversation history and context for multi-turn interactions"""
    
    def __init__(self, max_messages: int = 20, system_context: str = None):
        """
        Initialize conversation memory
        
        Args:
            max_messages: Maximum messages to keep in memory (prevents token overflow)
            system_context: System prompt/context for the conversation
        """
        self.messages: List[Dict[str, str]] = []
        self.max_messages = max_messages
        self.system_context = system_context or "You are a helpful data analyst AI assistant."
        self.conversation_start = datetime.now()
        self.metadata = {
            "messages_count": 0,
            "last_updated": None,
            "conversation_duration": 0
        }
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation memory
        
        Args:
            role: "user" or "assistant"
            content: Message content
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent messages to prevent token overflow
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        
        self.metadata["messages_count"] += 1
        self.metadata["last_updated"] = datetime.now().isoformat()
        self.metadata["conversation_duration"] = (
            datetime.now() - self.conversation_start
        ).total_seconds()
    
    def get_context(self) -> List[Dict[str, str]]:
        """
        Get conversation context formatted for OpenAI API
        
        Returns:
            List of messages ready for API call
        """
        # Include system message at the beginning
        context = [
            {
                "role": "system",
                "content": self.system_context
            }
        ]
        
        # Add conversation history (without timestamps for API)
        for msg in self.messages:
            context.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return context
    
    def get_recent_context(self, window_size: int = 6) -> List[Dict[str, str]]:
        """
        Get recent messages for context (reduces API tokens)
        
        Args:
            window_size: Number of recent messages to include
            
        Returns:
            List of recent messages with system context
        """
        context = [
            {
                "role": "system",
                "content": self.system_context
            }
        ]
        
        # Get last window_size messages
        recent_messages = self.messages[-window_size:] if len(self.messages) > window_size else self.messages
        
        for msg in recent_messages:
            context.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return context
    
    def clear_history(self) -> None:
        """Clear all conversation history but keep system context"""
        self.messages.clear()
        self.conversation_start = datetime.now()
        self.metadata["messages_count"] = 0
    
    def get_summary(self) -> Dict[str, Any]:
        """Get conversation summary/metadata"""
        return {
            "total_messages": len(self.messages),
            "user_messages": sum(1 for m in self.messages if m["role"] == "user"),
            "assistant_messages": sum(1 for m in self.messages if m["role"] == "assistant"),
            "metadata": self.metadata,
            "conversation_start": self.conversation_start.isoformat()
        }
    
    def export_history(self) -> str:
        """Export conversation history as JSON string"""
        return json.dumps(self.messages, indent=2)
    
    def __len__(self) -> int:
        """Get number of messages in history"""
        return len(self.messages)
    
    def __repr__(self) -> str:
        """String representation"""
        return f"ConversationMemory(messages={len(self.messages)}, max={self.max_messages})"
