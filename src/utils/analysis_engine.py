"""
Advanced Analysis Engine
Provides temporal analysis, aggregations, grouping, and custom analytics
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta


class AnalysisEngine:
    """Advanced data analysis with temporal and aggregation features"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize analysis engine with dataframe
        
        Args:
            df: Source dataframe for analysis
        """
        self.df = df
        self.numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        self.datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # ========================================================================
    # Date/Time Analysis
    # ========================================================================
    
    def get_datetime_columns(self) -> List[str]:
        """Get available datetime columns"""
        return self.datetime_cols
    
    def extract_datetime_parts(self, date_col: str) -> pd.DataFrame:
        """
        Extract datetime components from a column
        
        Args:
            date_col: Column name with datetime data
            
        Returns:
            DataFrame with extracted components
        """
        if date_col not in self.df.columns:
            return pd.DataFrame()
        
        try:
            df_copy = self.df.copy()
            date_series = pd.to_datetime(df_copy[date_col])
            
            df_copy['year'] = date_series.dt.year
            df_copy['month'] = date_series.dt.month
            df_copy['month_name'] = date_series.dt.strftime('%B')
            df_copy['quarter'] = date_series.dt.quarter
            df_copy['week'] = date_series.dt.isocalendar().week
            df_copy['day_of_week'] = date_series.dt.day_name()
            df_copy['day'] = date_series.dt.day
            
            return df_copy
        except Exception as e:
            raise ValueError(f"Error extracting datetime: {str(e)}")
    
    def temporal_analysis(
        self,
        date_col: str,
        metric_col: Optional[str] = None,
        group_col: Optional[str] = None,
        period: str = "month",
        aggregation: str = "count"
    ) -> pd.DataFrame:
        """
        Perform temporal analysis (by month, year, quarter, etc.)
        
        Args:
            date_col: Column with datetime data
            metric_col: Column to aggregate (None for count)
            group_col: Optional grouping column
            period: 'month', 'year', 'quarter', 'week', 'day'
            aggregation: 'count', 'sum', 'mean', 'min', 'max', 'median'
            
        Returns:
            Aggregated temporal dataframe
        """
        df_copy = self.df.copy()
        
        # Convert to datetime
        df_copy[date_col] = pd.to_datetime(df_copy[date_col])
        
        # Extract period
        if period == "month":
            df_copy['period'] = df_copy[date_col].dt.to_period('M')
        elif period == "year":
            df_copy['period'] = df_copy[date_col].dt.to_period('Y')
        elif period == "quarter":
            df_copy['period'] = df_copy[date_col].dt.to_period('Q')
        elif period == "week":
            df_copy['period'] = df_copy[date_col].dt.to_period('W')
        elif period == "day":
            df_copy['period'] = df_copy[date_col].dt.to_period('D')
        else:
            df_copy['period'] = df_copy[date_col].dt.to_period('M')
        
        # Group by
        if group_col:
            grouped = df_copy.groupby(['period', group_col])
        else:
            grouped = df_copy.groupby('period')
        
        # Aggregate
        if metric_col and metric_col in self.numeric_cols:
            if aggregation == "sum":
                result = grouped[metric_col].sum()
            elif aggregation == "mean":
                result = grouped[metric_col].mean()
            elif aggregation == "min":
                result = grouped[metric_col].min()
            elif aggregation == "max":
                result = grouped[metric_col].max()
            elif aggregation == "median":
                result = grouped[metric_col].median()
            else:  # count
                result = grouped[metric_col].count()
        else:
            result = grouped.size()
        
        result_df = result.reset_index()
        result_df.columns = ['period', 'group', 'value'] if group_col else ['period', 'value']
        
        return result_df
    
    # ========================================================================
    # Grouping & Aggregation
    # ========================================================================
    
    def group_by_analysis(
        self,
        group_col: str,
        metric_col: Optional[str] = None,
        aggregation: str = "count",
        sort_by: str = "value"
    ) -> pd.DataFrame:
        """
        Group data by column and aggregate
        
        Args:
            group_col: Column to group by
            metric_col: Column to aggregate (None for count)
            aggregation: 'count', 'sum', 'mean', 'min', 'max', 'median'
            sort_by: 'value' or 'group'
            
        Returns:
            Aggregated dataframe
        """
        if group_col not in self.df.columns:
            return pd.DataFrame()
        
        if metric_col and metric_col in self.numeric_cols:
            if aggregation == "sum":
                result = self.df.groupby(group_col)[metric_col].sum()
            elif aggregation == "mean":
                result = self.df.groupby(group_col)[metric_col].mean()
            elif aggregation == "min":
                result = self.df.groupby(group_col)[metric_col].min()
            elif aggregation == "max":
                result = self.df.groupby(group_col)[metric_col].max()
            elif aggregation == "median":
                result = self.df.groupby(group_col)[metric_col].median()
            else:  # count
                result = self.df.groupby(group_col)[metric_col].count()
        else:
            result = self.df.groupby(group_col).size()
        
        result_df = result.reset_index()
        result_df.columns = [group_col, 'value']
        
        # Sort
        if sort_by == "value":
            result_df = result_df.sort_values('value', ascending=False)
        else:
            result_df = result_df.sort_values(group_col)
        
        return result_df
    
    def multi_group_analysis(
        self,
        group_cols: List[str],
        metric_col: Optional[str] = None,
        aggregation: str = "count"
    ) -> pd.DataFrame:
        """
        Group by multiple columns
        
        Args:
            group_cols: List of columns to group by
            metric_col: Column to aggregate
            aggregation: Aggregation method
            
        Returns:
            Multi-level aggregated dataframe
        """
        if metric_col and metric_col in self.numeric_cols:
            if aggregation == "sum":
                result = self.df.groupby(group_cols)[metric_col].sum()
            elif aggregation == "mean":
                result = self.df.groupby(group_cols)[metric_col].mean()
            elif aggregation == "count":
                result = self.df.groupby(group_cols)[metric_col].count()
            else:
                result = self.df.groupby(group_cols).size()
        else:
            result = self.df.groupby(group_cols).size()
        
        return result.reset_index().rename(columns={0: 'value'} if not metric_col else {})
    
    # ========================================================================
    # Percentage & Ratio Analysis
    # ========================================================================
    
    def calculate_percentages(
        self,
        group_col: str,
        metric_col: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Calculate percentages by group
        
        Args:
            group_col: Column to group by
            metric_col: Column to sum/count
            
        Returns:
            DataFrame with counts and percentages
        """
        if metric_col and metric_col in self.numeric_cols:
            grouped = self.df.groupby(group_col)[metric_col].sum()
        else:
            grouped = self.df.groupby(group_col).size()
        
        result_df = grouped.reset_index()
        result_df.columns = [group_col, 'count']
        result_df['percentage'] = (result_df['count'] / result_df['count'].sum() * 100).round(2)
        result_df = result_df.sort_values('count', ascending=False)
        
        return result_df
    
    # ========================================================================
    # Cross-Tabulation Analysis
    # ========================================================================
    
    def crosstab_analysis(
        self,
        row_col: str,
        col_col: str,
        values_col: Optional[str] = None,
        aggregation: str = "count"
    ) -> pd.DataFrame:
        """
        Create cross-tabulation between two columns
        
        Args:
            row_col: Column for rows
            col_col: Column for columns
            values_col: Column to aggregate (None for count)
            aggregation: 'count', 'sum', 'mean', etc.
            
        Returns:
            Cross-tabulated dataframe
        """
        if values_col and values_col in self.numeric_cols:
            if aggregation == "sum":
                result = pd.crosstab(self.df[row_col], self.df[col_col], values=self.df[values_col], aggfunc='sum')
            elif aggregation == "mean":
                result = pd.crosstab(self.df[row_col], self.df[col_col], values=self.df[values_col], aggfunc='mean')
            elif aggregation == "count":
                result = pd.crosstab(self.df[row_col], self.df[col_col], values=self.df[values_col], aggfunc='count')
            else:
                result = pd.crosstab(self.df[row_col], self.df[col_col])
        else:
            result = pd.crosstab(self.df[row_col], self.df[col_col])
        
        return result.reset_index()
    
    # ========================================================================
    # Conditional Analysis
    # ========================================================================
    
    def filter_and_aggregate(
        self,
        filters: Dict[str, Any],
        group_col: str,
        metric_col: Optional[str] = None,
        aggregation: str = "count"
    ) -> pd.DataFrame:
        """
        Apply filters and then aggregate
        
        Args:
            filters: Dictionary of column: value for filtering
            group_col: Column to group by after filtering
            metric_col: Column to aggregate
            aggregation: Aggregation method
            
        Returns:
            Filtered and aggregated dataframe
        """
        df_filtered = self.df.copy()
        
        for col, value in filters.items():
            if isinstance(value, list):
                df_filtered = df_filtered[df_filtered[col].isin(value)]
            else:
                df_filtered = df_filtered[df_filtered[col] == value]
        
        # Now aggregate
        if metric_col and metric_col in self.numeric_cols:
            if aggregation == "sum":
                result = df_filtered.groupby(group_col)[metric_col].sum()
            elif aggregation == "mean":
                result = df_filtered.groupby(group_col)[metric_col].mean()
            else:
                result = df_filtered.groupby(group_col)[metric_col].count()
            # Rename the metric column to 'value' for consistency
            return result.reset_index().rename(columns={metric_col: 'value'})
        else:
            result = df_filtered.groupby(group_col).size()
            return result.reset_index().rename(columns={0: 'value'})
    
    # ========================================================================
    # Summary Statistics
    # ========================================================================
    
    def get_summary_stats(
        self,
        col: str,
        group_col: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive summary statistics
        
        Args:
            col: Column to analyze
            group_col: Optional grouping column
            
        Returns:
            Dictionary with statistics
        """
        if col not in self.numeric_cols:
            return {}
        
        if group_col and group_col in self.df.columns:
            stats = self.df.groupby(group_col)[col].agg(['count', 'mean', 'median', 'std', 'min', 'max']).to_dict()
        else:
            stats = {
                'count': self.df[col].count(),
                'mean': self.df[col].mean(),
                'median': self.df[col].median(),
                'std': self.df[col].std(),
                'min': self.df[col].min(),
                'max': self.df[col].max(),
                'q25': self.df[col].quantile(0.25),
                'q75': self.df[col].quantile(0.75)
            }
        
        return stats
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def get_unique_values(self, col: str, limit: int = 100) -> List[Any]:
        """Get unique values from a column"""
        if col not in self.df.columns:
            return []
        return self.df[col].dropna().unique()[:limit].tolist()
