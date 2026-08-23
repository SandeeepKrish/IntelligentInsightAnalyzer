"""
Theme Configuration Module
Manages light and dark mode themes for the application
"""

from typing import Dict, Any


class Theme:
    """Theme configuration for light and dark modes"""
    
    LIGHT = {
        "name": "light",
        "primary_color": "#0066cc",
        "background_color": "#ffffff",
        "secondary_background_color": "#f0f2f6",
        "text_color": "#262730",
        "border_color": "#d3d3d3",
        "chat_user_bg": "#e3f2fd",
        "chat_assistant_bg": "#f5f5f5",
        "success_color": "#28a745",
        "error_color": "#dc3545",
        "warning_color": "#ffc107",
        "info_color": "#17a2b8",
    }
    
    DARK = {
        "name": "dark",
        "primary_color": "#1f77ff",
        "background_color": "#0e1117",
        "secondary_background_color": "#161b22",
        "text_color": "#e6edf3",
        "border_color": "#30363d",
        "chat_user_bg": "#1f6feb",
        "chat_assistant_bg": "#21262d",
        "success_color": "#3fb950",
        "error_color": "#f85149",
        "warning_color": "#d29922",
        "info_color": "#79c0ff",
    }
    
    @staticmethod
    def get_theme(mode: str = "light") -> Dict[str, Any]:
        """
        Get theme configuration
        
        Args:
            mode: "light" or "dark"
            
        Returns:
            Theme configuration dictionary
        """
        if mode.lower() == "dark":
            return Theme.DARK
        return Theme.LIGHT
    
    @staticmethod
    def get_streamlit_config(mode: str = "light") -> str:
        """
        Get Streamlit config.toml format for theme
        
        Args:
            mode: "light" or "dark"
            
        Returns:
            TOML configuration string
        """
        theme = Theme.get_theme(mode)
        
        config = f"""[theme]
primaryColor = "{theme['primary_color']}"
backgroundColor = "{theme['background_color']}"
secondaryBackgroundColor = "{theme['secondary_background_color']}"
textColor = "{theme['text_color']}"
font = "sans serif"

[client]
showErrorDetails = true
toolbarMode = "viewer"

[logger]
level = "info"

[server]
maxUploadSize = 200
enableCORS = false
headless = true
"""
        return config


def apply_theme_styles(theme_name: str) -> str:
    """
    Generate custom CSS for theme
    
    Args:
        theme_name: "light" or "dark"
        
    Returns:
        CSS string for custom styling
    """
    theme = Theme.get_theme(theme_name)
    
    css = f"""
    <style>
        :root {{
            --primary-color: {theme['primary_color']};
            --background-color: {theme['background_color']};
            --text-color: {theme['text_color']};
            --border-color: {theme['border_color']};
        }}
        
        body {{
            background-color: {theme['background_color']};
            color: {theme['text_color']};
        }}
        
        .stChatMessage {{
            background-color: {theme['secondary_background_color']};
        }}
        
        .user-message {{
            background-color: {theme['chat_user_bg']};
            color: white;
        }}
        
        .assistant-message {{
            background-color: {theme['chat_assistant_bg']};
            color: {theme['text_color']};
        }}
        
        .stButton > button {{
            background-color: {theme['primary_color']};
            color: white;
            border: none;
        }}
        
        .stButton > button:hover {{
            opacity: 0.8;
        }}
        
        .stDataFrame {{
            border-color: {theme['border_color']};
        }}
        
        .success {{
            color: {theme['success_color']};
        }}
        
        .error {{
            color: {theme['error_color']};
        }}
        
        .warning {{
            color: {theme['warning_color']};
        }}
        
        .info {{
            color: {theme['info_color']};
        }}
    </style>
    """
    return css
