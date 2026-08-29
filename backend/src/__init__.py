"""
IntelligentInsightAnalyzer Backend - Main Package
"""

# Only import what's needed for auth service
from .auth import email_service
from .database import db

__version__ = "2.0.0"
__author__ = "IntelligentInsightAnalyzer Team"

__all__ = [
    "email_service",
    "db"
]

