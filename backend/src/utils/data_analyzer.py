"""
Data Analysis Utilities
Provides helper functions for data profiling and analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List


class DataAnalyzer:
    """Helper class for data analysis and profiling"""
    
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> str:
        """Generate a comprehensive summary of the dataset"""
        # Get sample data (first 20 rows)
        sample_data = df.head(20).to_string()
        
        summary = f"""
DATASET OVERVIEW:
- Total Rows: {len(df):,}
- Total Columns: {len(df.columns)}
- Total Size: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
- Total Missing Values: {df.isna().sum().sum():,}
- Total Duplicate Rows: {df.duplicated().sum():,}

COLUMN DETAILS:
"""
        for col in df.columns:
            dtype = str(df[col].dtype)
            missing = df[col].isna().sum()
            unique = df[col].nunique()
            summary += f"\n  Column: {col}"
            summary += f"\n    - Type: {dtype}"
            summary += f"\n    - Unique Values: {unique}"
            summary += f"\n    - Missing Values: {missing}"
            
            # Add sample values for categorical
            if dtype == 'object':
                sample_vals = df[col].dropna().unique()[:5]
                summary += f"\n    - Sample Values: {', '.join(str(v) for v in sample_vals)}"
        
        # Add numeric statistics
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        if numeric_cols:
            summary += "\n\nNUMERIC STATISTICS:\n"
            for col in numeric_cols:
                summary += f"\n  {col}:"
                summary += f"\n    - Mean: {df[col].mean():.2f}"
                summary += f"\n    - Median: {df[col].median():.2f}"
                summary += f"\n    - Std Dev: {df[col].std():.2f}"
                summary += f"\n    - Min: {df[col].min():.2f}"
                summary += f"\n    - Max: {df[col].max():.2f}"
        
        # Add sample data
        summary += f"\n\nSAMPLE DATA (first 20 rows):\n{sample_data}"
        
        return summary
    
    @staticmethod
    def get_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
        """Get columns grouped by data type"""
        return {
            "numeric": df.select_dtypes(include=np.number).columns.tolist(),
            "categorical": df.select_dtypes(include=['object']).columns.tolist(),
            "datetime": df.select_dtypes(include=['datetime64']).columns.tolist(),
            "boolean": df.select_dtypes(include=['bool']).columns.tolist()
        }
    
    @staticmethod
    def get_quality_metrics(df: pd.DataFrame) -> Dict[str, Any]:
        """Get data quality metrics"""
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isna().sum().sum()
        duplicate_rows = df.duplicated().sum()
        
        return {
            "completeness": ((total_cells - missing_cells) / total_cells * 100) if total_cells > 0 else 0,
            "missing_values": missing_cells,
            "duplicate_rows": duplicate_rows,
            "total_cells": total_cells,
            "quality_score": ((total_cells - missing_cells - duplicate_rows) / total_cells * 100) if total_cells > 0 else 0
        }
    
    @staticmethod
    def get_top_insights(df: pd.DataFrame, num_insights: int = 5) -> List[str]:
        """Generate top data insights"""
        insights = []
        
        # Insight 1: Data completeness
        completeness = ((df.size - df.isna().sum().sum()) / df.size * 100)
        insights.append(f"Data Completeness: {completeness:.1f}% of cells have values")
        
        # Insight 2: Duplicates
        duplicate_pct = (df.duplicated().sum() / len(df) * 100)
        insights.append(f"Duplicates: {duplicate_pct:.1f}% of rows are exact duplicates")
        
        # Insight 3: Most common dtype
        dtype_counts = df.dtypes.value_counts()
        insights.append(f"Most Common Type: {dtype_counts.index[0]} ({dtype_counts.values[0]} columns)")
        
        # Insight 4: Numeric stats
        numeric_cols = df.select_dtypes(include=np.number).columns
        if len(numeric_cols) > 0:
            insights.append(f"Numeric Columns: {len(numeric_cols)} columns with {len(numeric_cols)} numeric features")
        
        # Insight 5: Categorical stats
        cat_cols = df.select_dtypes(include=['object']).columns
        if len(cat_cols) > 0:
            insights.append(f"Categorical Columns: {len(cat_cols)} columns for grouping/filtering")
        
        return insights[:num_insights]
