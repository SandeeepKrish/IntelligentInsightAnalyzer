"""
Data Quality Component
Displays data quality metrics and detailed column analysis
"""

import streamlit as st
import pandas as pd
from services import AnalyzerService


def render_data_quality(service: AnalyzerService):
    """
    Render the data quality tab
    
    Args:
        service: AnalyzerService instance
    """
    st.subheader("🧹 Data Quality Assessment")
    
    quality = service.get_data_quality_metrics()
    
    # Quality metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cells", f"{quality['total_cells']:,}")
    
    with col2:
        st.metric("Missing Values", f"{quality['missing_values']:,}")
    
    with col3:
        st.metric("Duplicate Rows", f"{quality['duplicate_rows']:,}")
    
    with col4:
        st.metric("Quality Score", f"{quality['quality_score']:.1f}%")
    
    # Detailed quality table
    st.markdown("### Column Quality Details")
    
    df = service.get_dataframe()
    quality_df = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[c].dtype) for c in df.columns],
        "missing": [int(df[c].isna().sum()) for c in df.columns],
        "unique": [int(df[c].nunique(dropna=True)) for c in df.columns],
        "missing%": [f"{(df[c].isna().sum() / len(df) * 100):.1f}%" for c in df.columns]
    })
    st.dataframe(quality_df, use_container_width=True)
    
    # Data insights
    st.markdown("### Data Insights")
    insights = service.get_data_insights()
    for i, insight in enumerate(insights, 1):
        st.write(f"{i}. {insight}")
