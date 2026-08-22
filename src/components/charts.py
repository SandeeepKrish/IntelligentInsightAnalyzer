"""
Charts Component
Creates custom visualizations for data analysis
"""

import streamlit as st
import plotly.express as px
from config import AppConfig
from services import AnalyzerService


def render_charts(service: AnalyzerService):
    """
    Render the charts tab
    
    Args:
        service: AnalyzerService instance
    """
    st.subheader("📈 Create Custom Visualizations")
    
    chart_type = st.selectbox("Chart Type", AppConfig.CHART_TYPES)
    
    nums = service.get_numeric_columns()
    cats = service.get_categorical_columns()
    df = service.get_dataframe()
    
    if chart_type == "Pie Chart":
        if cats:
            col = st.selectbox("Select category column", cats, key="pie_cat")
            if nums:
                values_col = st.selectbox("Select values column (for size)", nums, key="pie_val")
                pie_data = df.groupby(col)[values_col].sum().reset_index()
                fig = px.pie(
                    pie_data,
                    names=col,
                    values=values_col,
                    title=f"Distribution by {col}"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ No categorical columns for pie chart")
    
    elif chart_type == "Bar Chart":
        if cats and nums:
            cat_col = st.selectbox("Select category column", cats, key="bar_cat")
            num_col = st.selectbox("Select numeric column", nums, key="bar_num")
            bar_data = df.groupby(cat_col)[num_col].sum().reset_index()
            fig = px.bar(
                bar_data,
                x=cat_col,
                y=num_col,
                title=f"{num_col} by {cat_col}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Need categorical and numeric columns for bar chart")
    
    elif chart_type == "Scatter Plot":
        if len(nums) >= 2:
            x_col = st.selectbox("X-axis", nums, key="scatter_x")
            y_col = st.selectbox("Y-axis", nums, key="scatter_y")
            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                title=f"{x_col} vs {y_col}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Need at least 2 numeric columns for scatter plot")
    
    elif chart_type == "Line Chart":
        if len(nums) >= 2:
            x_col = st.selectbox("X-axis", nums, key="line_x")
            y_col = st.selectbox("Y-axis", nums, key="line_y")
            fig = px.line(
                df,
                x=x_col,
                y=y_col,
                title=f"{x_col} vs {y_col}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Need at least 2 numeric columns for line chart")
    
    elif chart_type == "Box Plot":
        if cats and nums:
            cat_col = st.selectbox("Category column", cats, key="box_cat")
            num_col = st.selectbox("Numeric column", nums, key="box_num")
            fig = px.box(
                df,
                x=cat_col,
                y=num_col,
                title=f"{num_col} by {cat_col}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Need categorical and numeric columns for box plot")
