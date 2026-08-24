"""
Advanced Analysis Component
Provides UI for temporal analysis, grouping, aggregations, and custom analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import AnalysisEngine
from services import AnalyzerService


def render_advanced_analysis(service: AnalyzerService):
    """
    Render the advanced analysis tab with multiple analysis types
    
    Args:
        service: AnalyzerService instance
    """
    df = service.get_dataframe()
    
    # Check if a dataframe is loaded
    if df is None or df.empty:
        st.subheader("🔬 Advanced Analysis")
        st.info("🚧 **Under Construction** - Upload a CSV or Excel file for advanced analysis")
        return
    
    analysis_engine = AnalysisEngine(df)
    
    # Main analysis selector
    st.subheader("🔬 Advanced Analysis")
    
    analysis_type = st.selectbox(
        "Select Analysis Type",
        [
            "📊 Group & Aggregate",
            "📅 Temporal Analysis (Time Series)",
            "📈 Percentage Distribution",
            "🔗 Cross-Tabulation",
            "🔍 Filtered Analysis",
            "📋 Multi-Group Analysis",
            "📊 Summary Statistics",
            "⭐ Custom Multi-Dimensional Analysis",
            "🚗 Car Sales by Type & Year"
        ]
    )
    
    # ====================================================================
    # CUSTOM MULTI-DIMENSIONAL ANALYSIS (NEW)
    # ====================================================================
    
    if analysis_type == "⭐ Custom Multi-Dimensional Analysis":
        st.markdown("### ⭐ Custom Multi-Dimensional Analysis")
        st.write("Create custom analysis by selecting dimensions and metrics")
        
        # Main controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            group_cols = st.multiselect(
                "Select Dimension(s) to Group By",
                analysis_engine.categorical_cols,
                max_selections=3,
                help="Pick 1-3 columns to group your data",
                key="custom_group_cols"
            )
        
        with col2:
            metric_col = st.selectbox(
                "Select Metric Column",
                analysis_engine.numeric_cols,
                help="The numeric column to analyze",
                key="custom_metric_col"
            )
        
        with col3:
            aggregation = st.selectbox(
                "Aggregation Method",
                ["sum", "count", "mean", "min", "max", "median"],
                help="How to aggregate the metric",
                key="custom_agg"
            )
        
        st.divider()
        
        # Additional filters
        st.markdown("### 🔍 Optional Filters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            filter_columns = st.multiselect(
                "Filter by (Optional)",
                analysis_engine.categorical_cols,
                max_selections=2,
                key="custom_filter_cols"
            )
        
        with col2:
            sort_by = st.selectbox(
                "Sort Results By",
                ["Value (High to Low)", "Value (Low to High)", "Group Name (A-Z)", "Group Name (Z-A)"],
                key="custom_sort"
            )
        
        # Build filter dictionary
        filters = {}
        if filter_columns:
            for col in filter_columns:
                unique_vals = df[col].unique()
                selected_vals = st.multiselect(
                    f"Select values for {col}",
                    unique_vals,
                    key=f"custom_filter_{col}"
                )
                if selected_vals:
                    filters[col] = selected_vals
        
        st.divider()
        
        # Analyze button
        if st.button("🔍 Run Analysis", key="custom_analyze_btn", use_container_width=True):
            if not group_cols:
                st.error("❌ Please select at least one dimension to group by")
            else:
                try:
                    # Apply filters
                    filtered_df = df.copy()
                    for col, values in filters.items():
                        filtered_df = filtered_df[filtered_df[col].isin(values)]
                    
                    # Group and aggregate
                    if aggregation == "count":
                        result = filtered_df.groupby(group_cols).size().reset_index(name='value')
                    else:
                        result = filtered_df.groupby(group_cols)[metric_col].agg(aggregation).reset_index()
                        result.columns = group_cols + ['value']
                    
                    # Sort results
                    if "High to Low" in sort_by:
                        result = result.sort_values('value', ascending=False)
                    elif "Low to High" in sort_by:
                        result = result.sort_values('value', ascending=True)
                    elif "Z-A" in sort_by:
                        result = result.sort_values(group_cols[0], ascending=False)
                    else:  # A-Z
                        result = result.sort_values(group_cols[0], ascending=True)
                    
                    # Display results
                    st.markdown(f"### 📊 Results - {' + '.join(group_cols)} by {aggregation.upper()} of {metric_col}")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("#### Results Table")
                        st.dataframe(result, use_container_width=True, height=400)
                    
                    with col2:
                        st.markdown("#### Summary Stats")
                        st.metric("Total Groups", len(result))
                        st.metric("Max Value", f"{result['value'].max():.2f}")
                        st.metric("Min Value", f"{result['value'].min():.2f}")
                        st.metric("Avg Value", f"{result['value'].mean():.2f}")
                    
                    # Chart
                    st.markdown("#### Visualization")
                    
                    if len(group_cols) == 1:
                        fig = px.bar(
                            result,
                            x=group_cols[0],
                            y='value',
                            title=f"{aggregation.title()} of {metric_col} by {group_cols[0]}",
                            labels={'value': f'{aggregation.title()} Value'},
                            color='value',
                            color_continuous_scale='Viridis'
                        )
                    else:
                        fig = px.bar(
                            result,
                            x=group_cols[0],
                            y='value',
                            color=group_cols[1] if len(group_cols) > 1 else None,
                            title=f"{aggregation.title()} of {metric_col} by {' + '.join(group_cols)}",
                            labels={'value': f'{aggregation.title()} Value'},
                            barmode='group'
                        )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Export button
                    csv = result.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"analysis_{' + '.join(group_cols)}.csv",
                        mime="text/csv",
                        key="custom_download"
                    )
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # ====================================================================
    # CAR SALES BY TYPE & YEAR
    # ====================================================================
    
    elif analysis_type == "🚗 Car Sales by Type & Year":
        st.markdown("### 🚗 Car Sales by Type & Year Analysis")
        st.write("Analyze car sales by type and year with two flexible options")
        
        # Allow manual selection for all columns
        st.markdown("#### Step 1: Configure Columns")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            car_type_col = st.selectbox(
                "Select Car Type Column",
                analysis_engine.categorical_cols,
                key="car_type_col_select"
            )
        
        with col2:
            year_col = st.selectbox(
                "Select Year Column",
                analysis_engine.categorical_cols + analysis_engine.numeric_cols,
                key="year_col_select"
            )
        
        with col3:
            units_col = st.selectbox(
                "Select Numeric Column (Units/Price/etc)",
                analysis_engine.numeric_cols,
                key="units_col_select"
            )
        
        st.divider()
        
        # Get unique years from data
        unique_years = sorted(df[year_col].unique())
        
        st.markdown("#### Step 2: Choose Analysis Type")
        
        analysis_mode = st.radio(
            "What do you want to analyze?",
            ["📊 By Car Type (All Years)", "📅 By Year (Select Specific Year)"],
            horizontal=True,
            key="car_analysis_mode"
        )
        
        if analysis_mode == "📊 By Car Type (All Years)":
            st.markdown("### Analysis: Units Sold by Car Type (All Years Combined)")
            
            if st.button("📊 Generate Car Type Analysis", key="btn_car_type_analysis"):
                try:
                    # Group by car type and sum units
                    result = df.groupby(car_type_col)[units_col].sum().reset_index()
                    result.columns = [car_type_col, 'Units Sold']
                    result = result.sort_values('Units Sold', ascending=False)
                    
                    # Display results
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("#### Results Table")
                        st.dataframe(result, use_container_width=True)
                    
                    with col2:
                        st.markdown("#### Summary")
                        st.metric("Total Car Types", len(result))
                        st.metric("Total Units Sold", int(result['Units Sold'].sum()))
                        st.metric("Avg Units per Type", int(result['Units Sold'].mean()))
                    
                    # Bar chart
                    st.markdown("#### Bar Chart")
                    fig = px.bar(
                        result,
                        x=car_type_col,
                        y='Units Sold',
                        title=f"Total Units Sold by {car_type_col}",
                        labels={'Units Sold': 'Units Sold'},
                        color='Units Sold',
                        color_continuous_scale='Blues'
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Export
                    csv = result.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"car_sales_by_type.csv",
                        mime="text/csv",
                        key="car_type_download"
                    )
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        else:  # By Year
            st.markdown("### Analysis: Units Sold by Car Type in a Specific Year")
            st.write(f"Available years: {', '.join(map(str, unique_years))}")
            
            selected_year = st.selectbox(
                "Select Year",
                unique_years,
                key="year_selection"
            )
            
            if st.button("📅 Generate Year Analysis", key="btn_year_analysis"):
                try:
                    # Filter by year and group by car type
                    year_data = df[df[year_col] == selected_year]
                    result = year_data.groupby(car_type_col)[units_col].sum().reset_index()
                    result.columns = [car_type_col, 'Units Sold']
                    result = result.sort_values('Units Sold', ascending=False)
                    
                    # Display results
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("#### Results Table")
                        st.dataframe(result, use_container_width=True)
                    
                    with col2:
                        st.markdown("#### Summary for Year {0}".format(selected_year))
                        st.metric("Car Types Sold", len(result))
                        st.metric("Total Units Sold", int(result['Units Sold'].sum()))
                        st.metric("Avg Units per Type", int(result['Units Sold'].mean()))
                    
                    # Bar chart
                    st.markdown("#### Bar Chart")
                    fig = px.bar(
                        result,
                        x=car_type_col,
                        y='Units Sold',
                        title=f"Units Sold by {car_type_col} in {selected_year}",
                        labels={'Units Sold': 'Units Sold'},
                        color='Units Sold',
                        color_continuous_scale='Greens'
                    )
                    fig.update_layout(xaxis_tickangle=-45)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Export
                    csv = result.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"car_sales_{selected_year}.csv",
                        mime="text/csv",
                        key="year_download"
                    )
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # ====================================================================
    # 1. GROUP & AGGREGATE
    # ====================================================================
    
    elif analysis_type == "📊 Group & Aggregate":
        st.subheader("📊 Group & Aggregate Analysis")
        st.write("Group your data by a column and aggregate using different methods")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            group_col = st.selectbox("Group By", analysis_engine.categorical_cols, key="group_col_1")
        
        with col2:
            metric_col = st.selectbox(
                "Metric (Optional)",
                [None] + analysis_engine.numeric_cols,
                key="metric_col_1"
            )
        
        with col3:
            aggregation = st.selectbox(
                "Aggregation",
                ["count", "sum", "mean", "min", "max", "median"],
                key="agg_1"
            )
        
        with col4:
            sort_by = st.selectbox("Sort By", ["value", "group"], key="sort_1")
        
        if st.button("🔍 Analyze", key="btn_group"):
            result = analysis_engine.group_by_analysis(group_col, metric_col, aggregation, sort_by)
            
            # Display table
            st.markdown("### Results Table")
            st.dataframe(result, use_container_width=True)
            
            # Display chart
            st.markdown("### Visualization")
            fig = px.bar(
                result,
                x=group_col,
                y='value',
                title=f"{aggregation.upper()} by {group_col}",
                labels={'value': f'{aggregation.title()} Value'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Groups", len(result))
            with col2:
                st.metric("Max Value", result['value'].max())
            with col3:
                st.metric("Mean Value", result['value'].mean().round(2))
    
    # ====================================================================
    # 2. TEMPORAL ANALYSIS
    # ====================================================================
    
    elif analysis_type == "📅 Temporal Analysis (Time Series)":
        st.subheader("📅 Temporal Analysis (Time Series)")
        st.write("Analyze your data over time with monthly, yearly, or custom periods")
        
        datetime_cols = analysis_engine.get_datetime_columns()
        
        if not datetime_cols:
            st.warning("⚠️ No datetime columns found in your dataset. Please ensure you have a date column.")
            st.info("💡 Tip: You can ask the AI to help identify date columns in your data")
            return
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_col = st.selectbox("Date Column", datetime_cols, key="date_col")
        
        with col2:
            period = st.selectbox(
                "Time Period",
                ["month", "year", "quarter", "week", "day"],
                key="period"
            )
        
        with col3:
            aggregation = st.selectbox(
                "Aggregation",
                ["count", "sum", "mean", "min", "max", "median"],
                key="agg_temporal"
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            metric_col = st.selectbox(
                "Metric (Optional)",
                [None] + analysis_engine.numeric_cols,
                key="metric_temporal"
            )
        
        with col2:
            group_col = st.selectbox(
                "Group By (Optional)",
                [None] + analysis_engine.categorical_cols,
                key="group_temporal"
            )
        
        if st.button("📈 Generate Time Series", key="btn_temporal"):
            try:
                result = analysis_engine.temporal_analysis(
                    date_col, metric_col, group_col, period, aggregation
                )
                
                # Display table
                st.markdown("### Time Series Data")
                st.dataframe(result, use_container_width=True)
                
                # Display chart
                st.markdown("### Trend Visualization")
                if group_col:
                    fig = px.line(
                        result,
                        x='period',
                        y='value',
                        color='group',
                        markers=True,
                        title=f"{aggregation.title()} {period.title()} Trend by {group_col}"
                    )
                else:
                    fig = px.line(
                        result,
                        x='period',
                        y='value',
                        markers=True,
                        title=f"{aggregation.title()} {period.title()} Trend"
                    )
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # ====================================================================
    # 3. PERCENTAGE DISTRIBUTION
    # ====================================================================
    
    elif analysis_type == "📈 Percentage Distribution":
        st.subheader("📈 Percentage Distribution")
        st.write("See what percentage each category represents")
        
        col1, col2 = st.columns(2)
        
        with col1:
            group_col = st.selectbox("Group By", analysis_engine.categorical_cols, key="group_pct")
        
        with col2:
            metric_col = st.selectbox(
                "Metric (Optional)",
                [None] + analysis_engine.numeric_cols,
                key="metric_pct"
            )
        
        if st.button("📊 Calculate Percentages", key="btn_pct"):
            result = analysis_engine.calculate_percentages(group_col, metric_col)
            
            # Display table
            st.markdown("### Percentage Breakdown")
            st.dataframe(result, use_container_width=True)
            
            # Pie chart
            st.markdown("### Pie Chart")
            fig = px.pie(
                result,
                names=group_col,
                values='count',
                title=f"Distribution by {group_col}",
                hover_data=['percentage']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Bar chart with percentages
            st.markdown("### Percentage Bar Chart")
            fig = px.bar(
                result,
                x=group_col,
                y='percentage',
                title=f"Percentage Distribution by {group_col}",
                labels={'percentage': 'Percentage (%)'},
                color='percentage',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ====================================================================
    # 4. CROSS-TABULATION
    # ====================================================================
    
    elif analysis_type == "🔗 Cross-Tabulation":
        st.subheader("🔗 Cross-Tabulation Analysis")
        st.write("Compare two categorical variables in a table format")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            row_col = st.selectbox("Row Categories", analysis_engine.categorical_cols, key="row_cross")
        
        with col2:
            col_col = st.selectbox(
                "Column Categories",
                [c for c in analysis_engine.categorical_cols if c != row_col],
                key="col_cross"
            )
        
        with col3:
            aggregation = st.selectbox(
                "Aggregation",
                ["count", "sum", "mean"],
                key="agg_cross"
            )
        
        values_col = st.selectbox(
            "Values Column (Optional for sum/mean)",
            [None] + analysis_engine.numeric_cols,
            key="values_cross"
        )
        
        if st.button("🔗 Create Cross-Tab", key="btn_cross"):
            result = analysis_engine.crosstab_analysis(row_col, col_col, values_col, aggregation)
            
            st.markdown("### Cross-Tabulation Table")
            st.dataframe(result, use_container_width=True)
            
            # Heatmap
            st.markdown("### Heatmap Visualization")
            pivot_result = result.set_index(row_col).iloc[:, 1:]
            fig = go.Figure(data=go.Heatmap(
                z=pivot_result.values,
                x=pivot_result.columns,
                y=pivot_result.index,
                colorscale='Blues'
            ))
            fig.update_layout(
                title=f"Cross-Tabulation: {row_col} vs {col_col}",
                xaxis_title=col_col,
                yaxis_title=row_col
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # ====================================================================
    # 5. FILTERED ANALYSIS
    # ====================================================================
    
    elif analysis_type == "🔍 Filtered Analysis":
        st.subheader("🔍 Filtered Analysis")
        st.write("Apply filters and then analyze the filtered data")
        
        # Build filters
        st.markdown("### Step 1: Apply Filters")
        filters = {}
        
        filter_cols = st.multiselect("Select columns to filter", analysis_engine.categorical_cols)
        
        for col in filter_cols:
            unique_vals = analysis_engine.get_unique_values(col)
            selected_vals = st.multiselect(
                f"Select values for {col}",
                unique_vals,
                key=f"filter_{col}"
            )
            if selected_vals:
                filters[col] = selected_vals
        
        if filters:
            st.markdown("### Step 2: Aggregate Filtered Data")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                group_col = st.selectbox("Group By", analysis_engine.categorical_cols, key="group_filter")
            
            with col2:
                metric_col = st.selectbox(
                    "Metric (Optional)",
                    [None] + analysis_engine.numeric_cols,
                    key="metric_filter"
                )
            
            with col3:
                aggregation = st.selectbox(
                    "Aggregation",
                    ["count", "sum", "mean"],
                    key="agg_filter"
                )
            
            if st.button("🔍 Analyze Filtered Data", key="btn_filter"):
                result = analysis_engine.filter_and_aggregate(filters, group_col, metric_col, aggregation)
                
                st.markdown("### Filtered Results")
                st.dataframe(result, use_container_width=True)
                
                fig = px.bar(
                    result,
                    x=group_col,
                    y='value',
                    title=f"Analysis of Filtered Data",
                    labels={'value': f'{aggregation.title()} Value'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.info(f"📊 Filtered data: {len(result)} groups found")
        else:
            st.info("👈 Select columns and values to filter")
    
    # ====================================================================
    # 6. MULTI-GROUP ANALYSIS
    # ====================================================================
    
    elif analysis_type == "📋 Multi-Group Analysis":
        st.subheader("📋 Multi-Group Analysis")
        st.write("Group by multiple columns simultaneously")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            group_cols = st.multiselect(
                "Select columns to group by",
                analysis_engine.categorical_cols,
                max_selections=3,
                key="multigroup_cols"
            )
        
        with col2:
            metric_col = st.selectbox(
                "Metric (Optional)",
                [None] + analysis_engine.numeric_cols,
                key="metric_multi"
            )
        
        with col3:
            aggregation = st.selectbox(
                "Aggregation",
                ["count", "sum", "mean"],
                key="agg_multi"
            )
        
        if st.button("📋 Multi-Group Analysis", key="btn_multi"):
            if not group_cols:
                st.warning("⚠️ Please select at least one column to group by")
            else:
                result = analysis_engine.multi_group_analysis(group_cols, metric_col, aggregation)
                
                st.markdown("### Multi-Group Results")
                st.dataframe(result, use_container_width=True)
                
                # Summary statistics
                st.markdown("### Summary")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Groups", len(result))
                with col2:
                    st.metric("Max Value", result['value'].max() if 'value' in result.columns else 0)
                with col3:
                    st.metric("Mean Value", result['value'].mean().round(2) if 'value' in result.columns else 0)
    
    # ====================================================================
    # 7. SUMMARY STATISTICS
    # ====================================================================
    
    elif analysis_type == "📊 Summary Statistics":
        st.subheader("📊 Summary Statistics")
        st.write("Get detailed statistics for a numeric column")
        
        col1, col2 = st.columns(2)
        
        with col1:
            col = st.selectbox("Select numeric column", analysis_engine.numeric_cols, key="stats_col")
        
        with col2:
            group_col = st.selectbox(
                "Group By (Optional)",
                [None] + analysis_engine.categorical_cols,
                key="stats_group"
            )
        
        if st.button("📊 Calculate Stats", key="btn_stats"):
            stats = analysis_engine.get_summary_stats(col, group_col)
            
            if isinstance(stats, dict):
                # Display as metrics
                st.markdown("### Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Count", stats.get('count', 0))
                with col2:
                    st.metric("Mean", f"{stats.get('mean', 0):.2f}")
                with col3:
                    st.metric("Median", f"{stats.get('median', 0):.2f}")
                with col4:
                    st.metric("Std Dev", f"{stats.get('std', 0):.2f}")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Min", f"{stats.get('min', 0):.2f}")
                with col2:
                    st.metric("Max", f"{stats.get('max', 0):.2f}")
                with col3:
                    st.metric("Q25", f"{stats.get('q25', 0):.2f}")
                with col4:
                    st.metric("Q75", f"{stats.get('q75', 0):.2f}")
                
                # Box plot
                st.markdown("### Distribution Visualization")
                fig = px.box(df, y=col, title=f"Distribution of {col}")
                st.plotly_chart(fig, use_container_width=True)
