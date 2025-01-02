"""
Visualization utilities for economic impact models.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional
import numpy as np

def plot_sensitivity_analysis(
    param_ranges: Dict[str, List[float]],
    baseline_values: Dict[str, float],
    calculate_impacts: callable,
    title: str = 'Sensitivity Analysis'
) -> go.Figure:
    """
    Generate sensitivity analysis visualization.
    
    Args:
        param_ranges: Dictionary of parameter names and their test values
        baseline_values: Dictionary of baseline values for comparison
        calculate_impacts: Callback function that calculates impacts given parameters
        title: Plot title
    """
    results = []
    
    for param, values in param_ranges.items():
        for val in values:
            # Calculate impacts with modified parameter
            impacts = calculate_impacts({**baseline_values, param: val})
            
            # Calculate percent changes from baseline
            baseline_impacts = calculate_impacts(baseline_values)
            for metric, value in impacts.items():
                results.append({
                    'Parameter': param,
                    'Value': val,
                    f'{metric} % Change': (value - baseline_impacts[metric]) / baseline_impacts[metric] * 100
                })
    
    df = pd.DataFrame(results)
    
    fig = go.Figure()
    metrics = [col for col in df.columns if '% Change' in col]
    colors = ['blue', 'green', 'red'][:len(metrics)]
    
    for metric, color in zip(metrics, colors):
        for param in param_ranges.keys():
            param_df = df[df['Parameter'] == param]
            fig.add_trace(go.Scatter(
                x=param_df['Value'],
                y=param_df[metric],
                name=f'{param} - {metric}',
                line=dict(color=color),
                showlegend=True
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Parameter Value',
        yaxis_title='Percent Change from Baseline',
        height=800
    )
    
    return fig

def plot_monte_carlo_results(
    results: Dict[str, pd.DataFrame],
    title: str = 'Monte Carlo Simulation Results'
) -> go.Figure:
    """
    Create histogram plots for Monte Carlo simulation results.
    
    Args:
        results: Dictionary of metric names and their simulation results
        title: Plot title
    """
    fig = go.Figure()
    
    for metric, data in results.items():
        fig.add_trace(go.Histogram(
            x=data.iloc[:, 0],
            name=metric,
            nbinsx=30,
            opacity=0.7
        ))
    
    fig.update_layout(
        title=title,
        barmode='overlay',
        xaxis_title='Value',
        yaxis_title='Frequency',
        showlegend=True
    )
    
    return fig

def plot_time_series(
    data: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    title: str = 'Time Series Analysis'
) -> go.Figure:
    """
    Create time series plots.
    
    Args:
        data: DataFrame containing time series data
        x_col: Name of column containing x-axis values
        y_cols: List of column names to plot on y-axis
        title: Plot title
    """
    fig = go.Figure()
    
    for col in y_cols:
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[col],
            name=col,
            mode='lines'
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title='Value',
        showlegend=True
    )
    
    return fig 