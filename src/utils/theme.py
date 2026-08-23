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
    Generate custom CSS for theme - FULL APP THEMING
    
    Args:
        theme_name: "light" or "dark"
        
    Returns:
        CSS string for custom styling
    """
    theme = Theme.get_theme(theme_name)
    bg_color = theme['background_color']
    sidebar_color = theme['secondary_background_color']
    text_color = theme['text_color']
    primary_color = theme['primary_color']
    border_color = theme['border_color']
    
    css = f"""
    <style>
        /* ===== ENTIRE APP BACKGROUND ===== */
        html, body {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}
        
        .stApp {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}
        
        /* Remove white top bar in dark mode */
        [data-testid="stDecoration"] {{
            background-color: {bg_color} !important;
            display: none !important;
        }}
        
        /* ===== SIDEBAR STYLING - CATCH ALL WHITE BOXES ===== */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_color} !important;
        }}
        
        [data-testid="stSidebar"] > * {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        [data-testid="stSidebar"] * {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* Force all divs in sidebar */
        [data-testid="stSidebar"] div {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* Force all sections in sidebar */
        [data-testid="stSidebar"] section {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* ===== NAVBAR/HEADER BAR - ALL BLACK ===== */
        header {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}
        
        [data-testid="stHeader"] {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}
        
        /* Top bar background */
        .stApp header {{
            background-color: {bg_color} !important;
        }}
        
        /* Streamlit header styling */
        .stApp > [data-testid="stDecoration"] {{
            background-color: {bg_color} !important;
        }}
        
        /* Header elements */
        header svg {{
            fill: {text_color} !important;
            stroke: {text_color} !important;
        }}
        
        header button {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
        }}
        
        header button:hover {{
            background-color: {border_color} !important;
        }}
        .main {{
            background-color: {bg_color} !important;
        }}
        
        .block-container {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}
        
        /* ===== ALL TEXT ELEMENTS ===== */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
        }}
        
        p, span, div, label, th, td {{
            color: {text_color} !important;
        }}
        
        /* ===== FILE UPLOADER - AGGRESSIVE TARGETING ===== */
        .stFileUploader {{
            background-color: {sidebar_color} !important;
        }}
        
        .stFileUploader > div {{
            background-color: {sidebar_color} !important;
        }}
        
        .stFileUploader > div > div {{
            background-color: {sidebar_color} !important;
        }}
        
        .stFileUploader > div > div > div {{
            background-color: {sidebar_color} !important;
        }}
        
        [data-testid="stFileUploadDropzone"] {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* Target all nested elements in file uploader */
        [data-testid="stFileUploadDropzone"] * {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* Shadow DOM piercing attempt */
        .stFileUploader ::shadow {{
            background-color: {sidebar_color} !important;
        }}
        
        /* Direct element styling */
        .uploadedFile {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* ===== CHAT MESSAGES - FLAT DESIGN (NO NESTED BOXES) ===== */
        .stChatMessage {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 12px !important;
            padding: 16px !important;
            margin: 8px 0 !important;
        }}
        
        [data-testid="stChatMessage"] {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 12px !important;
        }}
        
        /* Remove nested container backgrounds */
        [data-testid="stChatMessage"] > div {{
            background-color: transparent !important;
        }}
        
        /* All nested content transparent background */
        [data-testid="stChatMessage"] * {{
            background-color: transparent !important;
            color: {text_color} !important;
        }}
        
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] span {{
            color: {text_color} !important;
        }}
        
        /* ===== BUTTONS - SIMPLE STYLING ===== */
        .stButton > button {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px !important;
            padding: 10px 16px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
        }}
        
        .stButton > button:hover {{
            opacity: 0.85 !important;
            transform: translateY(-1px) !important;
        }}
        
        .stButton > button:active {{
            transform: translateY(0) !important;
            opacity: 0.75 !important;
        }}
        
        /* Remove blue focus outline */
        .stButton > button:focus {{
            outline: none !important;
            border: 1px solid {border_color} !important;
            box-shadow: none !important;
        }}
        
        /* All buttons - remove blue styling */
        button {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px !important;
        }}
        
        button:focus {{
            outline: none !important;
            box-shadow: none !important;
        }}
        
        /* ===== INPUT FIELDS ===== */
        .stTextInput input,
        .stNumberInput input,
        .stSelectbox input {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
        }}
        
        input[type="text"],
        input[type="file"],
        input[type="number"],
        textarea {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
        }}
        
        /* ===== DROPZONE SPECIFIC ===== */
        [data-baseweb="file-uploader"] {{
            background-color: {sidebar_color} !important;
        }}
        
        [data-baseweb="file-uploader"] > div {{
            background-color: {sidebar_color} !important;
        }}
        
        [data-baseweb="file-uploader"] * {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* ===== SELECT & DROPDOWN ===== */
        .stSelectbox > div > div {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}
        
        /* ===== METRICS ===== */
        .stMetric {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* ===== DATAFRAMES ===== */
        .stDataFrame {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* ===== TABS ===== */
        .stTabs [data-baseweb="tab"] {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {primary_color} !important;
            color: white !important;
        }}
        
        /* ===== INFO/SUCCESS/ERROR/WARNING ===== */
        .stAlert {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px !important;
        }}
        
        [data-testid="stAlert"] {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        [data-testid="stAlert"] * {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* ===== DIVIDERS ===== */
        hr {{
            border-color: {border_color} !important;
        }}
        
        /* ===== CHAT INPUT - STYLED IN CHAT COMPONENT ===== */
        /* (Primary styling in chat_interface.py apply_chat_styling) */
        
        /* ===== EXPANDER ===== */
        .streamlit-expanderHeader {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* ===== RADIO BUTTONS ===== */
        .stRadio > div {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* ===== CHECKBOX ===== */
        .stCheckbox > label {{
            color: {text_color} !important;
        }}
        
        /* ===== PLOTS ===== */
        .js-plotly-plot {{
            background-color: {bg_color} !important;
        }}
        
        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {{
            background-color: {sidebar_color} !important;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background-color: {border_color} !important;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background-color: {primary_color} !important;
        }}
        
        /* ===== CODE BLOCKS ===== */
        pre, code {{
            background-color: {sidebar_color} !important;
            color: {text_color} !important;
        }}
        
        /* ===== SIDEBAR CHILDREN ===== */
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            color: {text_color} !important;
        }}
        
        [data-testid="stSidebar"] .stMetric {{
            color: {text_color} !important;
        }}
    </style>
    """
    return css
