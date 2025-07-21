"""
Evidently Monitoring Pipeline Step
---------------------------------
Generates data/model drift reports using Evidently AI.
"""
import pandas as pd
from evidently.report import Report
from evidently.metrics import DataDriftPreset
import os

def evidently_monitoring_step(reference_data: pd.DataFrame, current_data: pd.DataFrame, output_path: str = "drift_report.html") -> str:
    """
    Runs Evidently AI drift report and saves as HTML.
    Args:
        reference_data (pd.DataFrame): Baseline data.
        current_data (pd.DataFrame): New data to compare.
        output_path (str): Where to save the report.
    Returns:
        str: Path to the saved report.
    """
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)
    report.save_html(output_path)
    return output_path 