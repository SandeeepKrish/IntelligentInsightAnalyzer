"""
Data Explorer Component
Displays dataset preview and distribution analysis
"""

import streamlit as st
import plotly.express as px
import numpy as np
from services import AnalyzerService


def render_data_explorer(service: AnalyzerService):
    """
    Render the data explorer tab
    
    Args:
        service: AnalyzerService instance
    """
    st.subheader("📊 Dataset Preview & Exploration")
    
    df = service.get_dataframe()
    
    # Check if a dataframe is loaded
    if df is None or df.empty:
        st.info("📄 Upload a CSV or Excel file to explore dataset")
        return
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### First 100 Rows")
        df_preview = service.get_dataframe_preview(100)
        st.dataframe(df_preview, use_container_width=True)
    
    with col2:
        st.markdown("### Column Types")
        col_types = service.get_column_types()
        st.write(f"**Numeric:** {len(col_types.get('numeric', []))}")
        st.write(f"**Categorical:** {len(col_types.get('categorical', []))}")
        st.write(f"**DateTime:** {len(col_types.get('datetime', []))}")
    
    # Distribution analysis
    st.markdown("### Distribution Analysis")
    numeric_cols = service.get_numeric_columns()
    
    if numeric_cols:
        col = st.selectbox("Select numeric column for histogram", numeric_cols)
        df = service.get_dataframe()
        
        fig = px.histogram(
            df,
            x=col,
            nbins=30,
            title=f"Distribution of {col}",
            labels={col: col}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No numeric columns found in dataset")
