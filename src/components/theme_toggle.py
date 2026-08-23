"""
Theme Toggle Component
Provides UI controls for switching between light and dark modes
"""

import streamlit as st
from utils import Theme, apply_theme_styles


def render_theme_toggle():
    """
    Render theme toggle button in the sidebar
    
    Returns:
        Selected theme ("light" or "dark")
    """
    # Initialize theme in session state
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    # Create sidebar section
    st.sidebar.divider()
    st.sidebar.markdown("### 🎨 Appearance")
    
    # Theme selection
    theme_options = {"☀️ Light": "light", "🌙 Dark": "dark"}
    selected_label = [k for k, v in theme_options.items() if v == st.session_state.theme][0]
    
    # Radio button for theme selection
    selected_theme = st.sidebar.radio(
        "Theme",
        options=list(theme_options.keys()),
        index=list(theme_options.keys()).index(selected_label),
        key="theme_radio",
        label_visibility="collapsed"
    )
    
    # Update session state
    new_theme = theme_options[selected_theme]
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()
    
    return st.session_state.theme


def apply_custom_theme(theme_name: str):
    """
    Apply custom CSS theme to the entire app
    
    Args:
        theme_name: "light" or "dark"
    """
    # Apply custom CSS
    css = apply_theme_styles(theme_name)
    st.markdown(css, unsafe_allow_html=True)


def get_current_theme() -> dict:
    """
    Get current theme configuration
    
    Returns:
        Theme dictionary with all color settings
    """
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    return Theme.get_theme(st.session_state.theme)


def get_theme_icon(theme_name: str) -> str:
    """
    Get emoji icon for theme
    
    Args:
        theme_name: "light" or "dark"
        
    Returns:
        Theme emoji icon
    """
    return "☀️" if theme_name == "light" else "🌙"
