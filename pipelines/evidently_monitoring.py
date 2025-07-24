"""
Evidently Monitoring Pipeline Step
---------------------------------
Generates data/model drift reports using Evidently AI.
"""
import pandas as pd
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import os

def evidently_monitoring_step(reference_data: pd.DataFrame, current_data: pd.DataFrame, output_path: str = "drift_report.html") -> str:
    """Generate data drift report.
    
    Args:
        reference_data: Baseline data
        current_data: New data to compare
        output_path: Where to save the report
        
    Returns:
        Path to the saved report
    """
    # Create dashboard with data drift tab
    dashboard = Dashboard(tabs=[DataDriftTab()])
    
    # Calculate drift metrics
    dashboard.calculate(reference_data, current_data)
    
    # Save report
    dashboard.save(output_path)
    
    return output_path 