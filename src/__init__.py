"""
AI Data Analyst Chatbot - Main Package
Professional structure with config, services, components, and utilities
"""

from .config import AppConfig
from .services import AnalyzerService
from .components import (
    render_chat_interface,
    render_data_explorer,
    render_data_quality,
    render_charts
)

__version__ = "2.0.0"
__author__ = "AI Data Analyst Team"

__all__ = [
    "AppConfig",
    "AnalyzerService",
    "render_chat_interface",
    "render_data_explorer",
    "render_data_quality",
    "render_charts"
]
