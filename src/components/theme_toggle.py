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
    
    # Theme selection using columns for better layout
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        light_clicked = st.button("☀️ Light", use_container_width=True, key="light_theme_btn")
    
    with col2:
        dark_clicked = st.button("🌙 Dark", use_container_width=True, key="dark_theme_btn")
    
    # Handle theme change
    if light_clicked and st.session_state.theme != "light":
        st.session_state.theme = "light"
        st.rerun()
    
    if dark_clicked and st.session_state.theme != "dark":
        st.session_state.theme = "dark"
        st.rerun()
    
    # Show current theme
    current_theme_display = "☀️ Light Mode" if st.session_state.theme == "light" else "🌙 Dark Mode"
    st.sidebar.info(f"Current: {current_theme_display}")
    
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
