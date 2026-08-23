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
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
        
        /* Root variables for dynamic theming */
        :root {{
            --primary-color: {theme['primary_color']};
            --background-color: {theme['background_color']};
            --secondary-bg: {theme['secondary_background_color']};
            --text-color: {theme['text_color']};
            --border-color: {theme['border_color']};
            --success-color: {theme['success_color']};
            --error-color: {theme['error_color']};
            --warning-color: {theme['warning_color']};
            --info-color: {theme['info_color']};
        }}
        
        /* Main app background */
        .stApp {{
            background-color: {theme['background_color']} !important;
            color: {theme['text_color']} !important;
        }}
        
        /* Sidebar styling */
        .css-1d391kg {{
            background-color: {theme['secondary_background_color']} !important;
        }}
        
        /* Main content area */
        .main .block-container {{
            background-color: {theme['background_color']} !important;
            color: {theme['text_color']} !important;
        }}
        
        /* Headers and text */
        h1, h2, h3, h4, h5, h6, p, div, span {{
            color: {theme['text_color']} !important;
        }}
        
        /* Streamlit elements */
        .stSelectbox > div > div {{
            background-color: {theme['secondary_background_color']} !important;
            color: {theme['text_color']} !important;
            border-color: {theme['border_color']} !important;
        }}
        
        .stButton > button {{
            background-color: {theme['primary_color']} !important;
            color: white !important;
            border: none !important;
            border-radius: 6px !important;
        }}
        
        .stButton > button:hover {{
            background-color: {theme['primary_color']}CC !important;
            transform: translateY(-1px) !important;
        }}
        
        /* Chat messages */
        .stChatMessage {{
            background-color: {theme['secondary_background_color']} !important;
            border: 1px solid {theme['border_color']} !important;
            border-radius: 10px !important;
            margin: 8px 0 !important;
        }}
        
        /* User message styling */
        .stChatMessage[data-testid="user-message"] {{
            background: linear-gradient(135deg, {theme['chat_user_bg']}, {theme['primary_color']}) !important;
        }}
        
        /* Assistant message styling */
        .stChatMessage[data-testid="assistant-message"] {{
            background-color: {theme['chat_assistant_bg']} !important;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab"] {{
            background-color: {theme['secondary_background_color']} !important;
            color: {theme['text_color']} !important;
            border-radius: 8px 8px 0 0 !important;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            background-color: {theme['primary_color']}22 !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {theme['primary_color']} !important;
            color: white !important;
        }}
        
        /* Metrics */
        .metric-container > div {{
            background-color: {theme['secondary_background_color']} !important;
            border: 1px solid {theme['border_color']} !important;
            border-radius: 8px !important;
        }}
        
        /* Dataframes */
        .stDataFrame {{
            background-color: {theme['secondary_background_color']} !important;
        }}
        
        /* File uploader */
        .stFileUploader > div {{
            background-color: {theme['secondary_background_color']} !important;
            border: 2px dashed {theme['border_color']} !important;
            border-radius: 10px !important;
        }}
        
        /* Success/Error/Warning/Info messages */
        .stSuccess {{
            background-color: {theme['success_color']}22 !important;
            color: {theme['success_color']} !important;
            border-left: 4px solid {theme['success_color']} !important;
        }}
        
        .stError {{
            background-color: {theme['error_color']}22 !important;
            color: {theme['error_color']} !important;
            border-left: 4px solid {theme['error_color']} !important;
        }}
        
        .stWarning {{
            background-color: {theme['warning_color']}22 !important;
            color: {theme['warning_color']} !important;
            border-left: 4px solid {theme['warning_color']} !important;
        }}
        
        .stInfo {{
            background-color: {theme['info_color']}22 !important;
            color: {theme['info_color']} !important;
            border-left: 4px solid {theme['info_color']} !important;
        }}
        
        /* Radio buttons */
        .stRadio > div {{
            background-color: {theme['secondary_background_color']} !important;
            padding: 10px !important;
            border-radius: 8px !important;
            border: 1px solid {theme['border_color']} !important;
        }}
        
        /* Input fields */
        .stTextInput > div > div > input {{
            background-color: {theme['secondary_background_color']} !important;
            color: {theme['text_color']} !important;
            border-color: {theme['border_color']} !important;
        }}
        
        /* Chat input */
        .stChatInput > div {{
            background-color: {theme['secondary_background_color']} !important;
            border-color: {theme['border_color']} !important;
        }}
        
        .stChatInput input {{
            background-color: {theme['secondary_background_color']} !important;
            color: {theme['text_color']} !important;
        }}
        
        /* Plotly charts background */
        .js-plotly-plot {{
            background-color: {theme['background_color']} !important;
        }}
        
        /* Sidebar dividers */
        .css-1d391kg hr {{
            border-color: {theme['border_color']} !important;
        }}
        
        /* Dark mode specific adjustments */
        {'' if theme_name == 'light' else '''
        /* Dark mode scrollbar */
        ::-webkit-scrollbar {{
            background-color: #161b22;
        }}
        ::-webkit-scrollbar-thumb {{
            background-color: #30363d;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background-color: #484f58;
        }}
        '''}
    </style>
    """
    return css
