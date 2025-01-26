import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any
from calculations import calculate_impacts, format_large_number

def plot_medicare_breakdown(breakdown_df: pd.DataFrame) -> go.Figure:
    """Create a bar chart showing Medicare savings by category."""
    fig = px.bar(
        breakdown_df,
        x='Medicare Savings',
        y='Category',
        title='Medicare Savings Breakdown',
        labels={'Medicare Savings': 'Annual Savings'},
        color='Category',
        orientation='h'
    )
    
    fig.update_traces(
        text=[format_large_number(x) for x in breakdown_df['Medicare Savings']],
        textposition='auto'
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis_title='Annual Medicare Savings ($)',
        yaxis_title=None
    )
    
    return fig

def plot_population_comparison(intervention: Dict[Any, Any], base_params: Dict[Any, Any]) -> go.Figure:
    """Create a comparison of impacts across population segments."""
    populations = ['total_us', 'over_60', 'adult']
    results = []
    
    for pop in populations:
        impact = calculate_impacts(intervention, pop, base_params)
        results.append({
            'Population': pop.replace('_', ' ').title(),
            'Medicare Savings': impact['Medicare Savings'],
            'GDP Impact': impact['GDP Impact'],
            'QALY Impact': impact['QALY Impact']
        })
    
    df = pd.DataFrame(results)
    
    fig = go.Figure()
    metrics = ['Medicare Savings', 'GDP Impact']
    
    for metric in metrics:
        fig.add_trace(go.Bar(
            name=metric,
            y=df['Population'],
            x=df[metric],
            text=[format_large_number(x) for x in df[metric]],
            textposition='auto',
            orientation='h'
        ))
    
    fig.update_layout(
        title='Impact Comparison Across Populations',
        barmode='group',
        xaxis_tickformat='$,.0f',
        height=400,
        margin=dict(l=20, r=20, t=50, b=50),
        title_x=0.5,
        title_y=0.98,
        yaxis_title=None,
        xaxis_title=None,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def plot_time_series(time_series_df: pd.DataFrame) -> go.Figure:
    """Create time series visualization."""
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=time_series_df['Year'],
            y=time_series_df['Annual Medicare Savings'],
            name='Annual',
            line=dict(color='blue')
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=time_series_df['Year'],
            y=time_series_df['Cumulative Medicare Savings'],
            name='Cumulative',
            line=dict(color='red', dash='dash')
        )
    )
    
    fig.update_layout(
        title='Medicare Savings Over Time',
        xaxis_title='Year',
        yaxis_title='Savings ($)',
        yaxis_tickformat='$,.0f',
        hovermode='x unified',
        height=450,
        margin=dict(l=20, r=20, t=50, b=50),
        title_x=0.5,
        title_y=0.98,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def plot_metrics_over_time(time_series_df: pd.DataFrame) -> go.Figure:
    """Create a multi-metric time series comparison."""
    fig = go.Figure()
    
    metrics = [
        ('GDP Impact', 'Annual GDP Impact', 'Cumulative GDP Impact'),
        ('Medicare Savings', 'Annual Medicare Savings', 'Cumulative Medicare Savings'),
        ('QALY Impact', 'Annual QALY Impact', 'Cumulative QALY Impact')
    ]
    
    for metric_name, annual_col, cumulative_col in metrics:
        fig.add_trace(
            go.Scatter(
                x=time_series_df['Year'],
                y=time_series_df[annual_col],
                name=f'Annual {metric_name}',
                line=dict(dash='solid'),
                visible='legendonly' if metric_name != 'Medicare Savings' else True
            )
        )
        fig.add_trace(
            go.Scatter(
                x=time_series_df['Year'],
                y=time_series_df[cumulative_col],
                name=f'Cumulative {metric_name}',
                line=dict(dash='dash'),
                visible='legendonly' if metric_name != 'Medicare Savings' else True
            )
        )
    
    fig.update_layout(
        title='Impact Metrics Over Time',
        xaxis_title='Year',
        yaxis_title='Value',
        yaxis_tickformat='$,.0f',
        hovermode='x unified',
        height=500,
        margin=dict(l=20, r=20, t=50, b=70),
        title_x=0.5,
        title_y=0.98,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )
    
    return fig

def plot_sensitivity_comparison(sensitivity_results: pd.DataFrame) -> go.Figure:
    """Create sensitivity analysis comparison chart."""
    fig = go.Figure()
    
    metrics = ['Cumulative Medicare Savings', 'Cumulative GDP Impact']
    for metric in metrics:
        fig.add_trace(go.Bar(
            name=metric.replace('Cumulative ', ''),
            x=sensitivity_results.index,
            y=sensitivity_results[metric],
            text=[format_large_number(x) for x in sensitivity_results[metric]],
            textposition='auto',
        ))
    
    fig.update_layout(
        title='10-Year Impact Scenarios',
        barmode='group',
        yaxis_tickformat='$,.0f',
        height=450,
        margin=dict(l=20, r=20, t=50, b=50),
        title_x=0.5,
        title_y=0.98,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig 