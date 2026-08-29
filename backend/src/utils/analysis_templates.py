"""
Analysis Templates - Pre-built analysis patterns for common use cases
Includes: Healthcare, Sales, E-commerce, Operations, etc.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from .analysis_engine import AnalysisEngine


class AnalysisTemplates:
    """Pre-built analysis templates for specific domains"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize templates
        
        Args:
            df: Source dataframe
        """
        self.df = df
        self.engine = AnalysisEngine(df)
    
    # ========================================================================
    # HEALTHCARE TEMPLATES
    # ========================================================================
    
    def hospital_patient_analysis(
        self,
        date_col: str,
        diagnosis_col: str,
        outcome_col: Optional[str] = None,
        period: str = "month"
    ) -> Dict[str, Any]:
        """
        Hospital patient analysis template
        - Patients by diagnosis
        - Admissions over time
        - Mortality/recovery rates
        - Outcomes by diagnosis
        
        Args:
            date_col: Column with admission dates
            diagnosis_col: Column with diagnosis
            outcome_col: Column with patient outcomes (died/recovered/etc)
            period: Time period for temporal analysis
            
        Returns:
            Dictionary with multiple analyses
        """
        results = {}
        
        # 1. Admissions by diagnosis
        results['by_diagnosis'] = self.engine.group_by_analysis(
            diagnosis_col, None, "count", "value"
        )
        
        # 2. Temporal admissions
        results['temporal'] = self.engine.temporal_analysis(
            date_col, None, diagnosis_col, period, "count"
        )
        
        # 3. Outcome analysis
        if outcome_col and outcome_col in self.df.columns:
            results['by_outcome'] = self.engine.group_by_analysis(
                outcome_col, None, "count", "value"
            )
            
            # Outcome by diagnosis
            results['outcome_by_diagnosis'] = self.engine.crosstab_analysis(
                diagnosis_col, outcome_col, None, "count"
            )
            
            # Mortality/Recovery rates
            outcome_stats = self.df.groupby(diagnosis_col)[outcome_col].value_counts().reset_index(name='count')
            results['outcome_stats'] = outcome_stats
        
        # 4. Percentages
        results['diagnosis_percentage'] = self.engine.calculate_percentages(diagnosis_col)
        
        return results
    
    def patient_demographics_analysis(
        self,
        age_col: str,
        gender_col: Optional[str] = None,
        location_col: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Patient demographics analysis
        - Age distribution
        - Gender breakdown
        - Geographic distribution
        """
        results = {}
        
        # Age statistics
        if age_col in self.df.columns:
            results['age_stats'] = self.engine.get_summary_stats(age_col)
            
            # Age groups
            age_bins = [0, 18, 30, 45, 60, 100]
            self.df['age_group'] = pd.cut(self.df[age_col], bins=age_bins, labels=['0-18', '18-30', '30-45', '45-60', '60+'])
            results['age_group_dist'] = self.engine.group_by_analysis('age_group', None, "count")
        
        # Gender
        if gender_col and gender_col in self.df.columns:
            results['gender_dist'] = self.engine.group_by_analysis(gender_col, None, "count")
        
        # Location
        if location_col and location_col in self.df.columns:
            results['location_dist'] = self.engine.group_by_analysis(location_col, None, "count")
        
        return results
    
    # ========================================================================
    # SALES & E-COMMERCE TEMPLATES
    # ========================================================================
    
    def sales_analysis(
        self,
        date_col: str,
        sales_col: str,
        category_col: Optional[str] = None,
        region_col: Optional[str] = None,
        period: str = "month"
    ) -> Dict[str, Any]:
        """
        Sales analysis template
        - Revenue over time
        - Sales by category/region
        - Top performing categories/regions
        - Growth trends
        
        Args:
            date_col: Date column
            sales_col: Sales amount column
            category_col: Product/service category
            region_col: Geographic region
            period: Time period
            
        Returns:
            Dictionary with sales analyses
        """
        results = {}
        
        # 1. Total revenue over time
        results['revenue_trend'] = self.engine.temporal_analysis(
            date_col, sales_col, None, period, "sum"
        )
        
        # 2. Average order value over time
        results['avg_value_trend'] = self.engine.temporal_analysis(
            date_col, sales_col, None, period, "mean"
        )
        
        # 3. Revenue by category
        if category_col and category_col in self.df.columns:
            results['by_category'] = self.engine.group_by_analysis(
                category_col, sales_col, "sum", "value"
            )
            results['category_percentage'] = self.engine.calculate_percentages(category_col, sales_col)
        
        # 4. Revenue by region
        if region_col and region_col in self.df.columns:
            results['by_region'] = self.engine.group_by_analysis(
                region_col, sales_col, "sum", "value"
            )
            results['region_percentage'] = self.engine.calculate_percentages(region_col, sales_col)
        
        # 5. Category and region comparison
        if category_col and region_col:
            results['category_region_cross'] = self.engine.crosstab_analysis(
                category_col, region_col, sales_col, "sum"
            )
        
        # 6. Monthly sales statistics
        results['sales_stats'] = self.engine.get_summary_stats(sales_col)
        
        return results
    
    def customer_analysis(
        self,
        customer_col: str,
        sales_col: Optional[str] = None,
        date_col: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Customer analysis template
        - Customer count
        - Top customers
        - Customer lifetime value
        - Purchase frequency
        """
        results = {}
        
        # Total unique customers
        results['total_customers'] = self.df[customer_col].nunique()
        
        # Sales per customer
        if sales_col and sales_col in self.df.columns:
            results['revenue_per_customer'] = self.engine.group_by_analysis(
                customer_col, sales_col, "sum", "value"
            ).head(20)
            
            results['avg_purchase'] = self.engine.group_by_analysis(
                customer_col, sales_col, "mean", "value"
            ).head(20)
        
        # Purchase count per customer
        results['purchase_frequency'] = self.engine.group_by_analysis(
            customer_col, None, "count", "value"
        ).head(20)
        
        return results
    
    # ========================================================================
    # OPERATIONS TEMPLATES
    # ========================================================================
    
    def operational_metrics(
        self,
        date_col: str,
        metric_col: str,
        status_col: Optional[str] = None,
        period: str = "month"
    ) -> Dict[str, Any]:
        """
        Operational metrics analysis
        - Metric trends over time
        - Status breakdown
        - Performance metrics
        """
        results = {}
        
        # Metric trend
        results['metric_trend'] = self.engine.temporal_analysis(
            date_col, metric_col, None, period, "mean"
        )
        
        # Status distribution
        if status_col and status_col in self.df.columns:
            results['by_status'] = self.engine.group_by_analysis(status_col, metric_col, "mean")
        
        # Metric statistics
        results['metric_stats'] = self.engine.get_summary_stats(metric_col)
        
        return results
    
    def quality_analysis(
        self,
        issue_col: str,
        severity_col: Optional[str] = None,
        date_col: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Quality/Issues analysis
        - Issue types
        - Severity breakdown
        - Issues over time
        - Root cause analysis
        """
        results = {}
        
        # Issue distribution
        results['issue_types'] = self.engine.group_by_analysis(
            issue_col, None, "count", "value"
        )
        
        # Severity
        if severity_col and severity_col in self.df.columns:
            results['by_severity'] = self.engine.group_by_analysis(
                severity_col, None, "count", "value"
            )
            
            # Severity by issue
            results['severity_by_issue'] = self.engine.crosstab_analysis(
                issue_col, severity_col, None, "count"
            )
        
        # Temporal
        if date_col and date_col in self.df.columns:
            results['issues_trend'] = self.engine.temporal_analysis(
                date_col, None, issue_col, "month", "count"
            )
        
        return results
    
    # ========================================================================
    # GENERAL PURPOSE TEMPLATES
    # ========================================================================
    
    def quick_summary_analysis(self) -> Dict[str, Any]:
        """
        Quick summary of the entire dataset
        """
        results = {
            'row_count': len(self.df),
            'column_count': len(self.df.columns),
            'numeric_columns': len(self.engine.numeric_cols),
            'categorical_columns': len(self.engine.categorical_cols),
            'datetime_columns': len(self.engine.datetime_cols),
            'missing_values': self.df.isna().sum().sum(),
            'duplicate_rows': self.df.duplicated().sum(),
        }
        return results
    
    def distribution_analysis(
        self,
        numeric_cols: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Distribution analysis for numeric columns
        """
        results = {}
        
        cols = numeric_cols or self.engine.numeric_cols
        
        for col in cols[:10]:  # Limit to 10 columns
            results[col] = self.engine.get_summary_stats(col)
        
        return results
    
    def correlation_analysis(self) -> pd.DataFrame:
        """
        Correlation matrix between numeric columns
        """
        numeric_df = self.df[self.engine.numeric_cols]
        return numeric_df.corr()
    
    def top_bottom_analysis(
        self,
        metric_col: str,
        group_col: str,
        n: int = 10
    ) -> Dict[str, pd.DataFrame]:
        """
        Get top and bottom N groups by metric
        """
        grouped = self.engine.group_by_analysis(group_col, metric_col, "sum", "value")
        
        return {
            'top_n': grouped.head(n),
            'bottom_n': grouped.tail(n)
        }
    
    # ========================================================================
    # SUGGESTION HELPERS
    # ========================================================================
    
    @staticmethod
    def suggest_templates(df: pd.DataFrame) -> List[str]:
        """
        Suggest analysis templates based on column names and types
        
        Args:
            df: Input dataframe
            
        Returns:
            List of suggested template names
        """
        suggestions = []
        columns_lower = [col.lower() for col in df.columns]
        
        # Healthcare detection
        healthcare_keywords = ['patient', 'diagnosis', 'admit', 'discharge', 'outcome', 'treatment']
        if any(kw in col for col in columns_lower for kw in healthcare_keywords):
            suggestions.append("Hospital Patient Analysis")
            suggestions.append("Patient Demographics Analysis")
        
        # Sales detection
        sales_keywords = ['sales', 'revenue', 'price', 'amount', 'order', 'category', 'product']
        if any(kw in col for col in columns_lower for kw in sales_keywords):
            suggestions.append("Sales Analysis")
            suggestions.append("Customer Analysis")
        
        # Operations detection
        ops_keywords = ['status', 'metric', 'issue', 'quality', 'performance']
        if any(kw in col for col in columns_lower for kw in ops_keywords):
            suggestions.append("Operational Metrics")
            suggestions.append("Quality Analysis")
        
        # Always suggest general
        suggestions.append("Quick Summary")
        suggestions.append("Distribution Analysis")
        suggestions.append("Top & Bottom Analysis")
        
        return suggestions
