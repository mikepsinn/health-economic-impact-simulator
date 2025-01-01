import streamlit as st
import yaml
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from pathlib import Path

# Load configuration files
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Load base parameters
base_params = load_yaml('config/base_parameters.yml')

# Load interventions
def load_interventions():
    interventions = {}
    interventions_dir = Path('config/interventions')
    for file in interventions_dir.glob('*.yml'):
        interventions[file.stem] = load_yaml(file)
    return interventions

# Calculate impacts
def calculate_impacts(intervention, population_type, base_params):
    pop = base_params['population'][population_type]
    effects = intervention['default_effects']
    modifiers = intervention['impact_modifiers']
    
    # Initialize impact values
    medicare_savings = 0
    gdp_impact = 0
    qaly_impact = 0
    
    # Calculate Medicare impact from hospital visits
    if 'healthcare' in effects:
        hospital_reduction = effects['healthcare']['hospital_visit_reduction'] / 100
        medicare_savings += (
            pop * 
            base_params['economics']['medicare_per_capita'] * 
            base_params['health_baselines']['medicare_enrollment_rate'] *
            hospital_reduction
        )
    
    # Calculate cognitive impacts
    if 'cognitive' in effects:
        # IQ impact on GDP
        if 'iq_increase' in effects['cognitive']:
            iq_impact = effects['cognitive']['iq_increase'] * modifiers.get('iq_to_gdp', 0)
            gdp_impact += pop * base_params['economics']['gdp_per_capita'] * iq_impact
        
        # Alzheimer's impact
        if 'alzheimers_reduction' in effects['cognitive'] and population_type == 'over_60':
            alz_reduction = effects['cognitive']['alzheimers_reduction'] / 100
            medicare_savings += (
                base_params['economics']['alzheimers_annual_cost'] * 
                alz_reduction * 
                modifiers.get('alzheimers_to_medicare', 0)
            )
    
    # Calculate kidney disease impacts
    if 'kidney' in effects and 'ckd_progression_reduction' in effects['kidney']:
        ckd_reduction = effects['kidney']['ckd_progression_reduction'] / 100
        medicare_savings += (
            base_params['economics']['ckd_annual_cost'] * 
            ckd_reduction * 
            modifiers.get('kidney_to_medicare', 0)
        )
    
    # Calculate GDP impact from longevity
    if 'longevity' in effects:
        lifespan_impact = effects['longevity']['lifespan_increase'] / 100
        gdp_impact += (
            pop * 
            base_params['economics']['gdp_per_capita'] * 
            lifespan_impact * 
            modifiers.get('lifespan_to_gdp', 0.8)
        )
    
    # Calculate QALYs
    qaly_base = pop * base_params['health_baselines']['average_lifespan']
    qaly_impact = qaly_base * modifiers.get('health_quality', 0)
    if 'longevity' in effects:
        qaly_impact += qaly_base * (effects['longevity']['lifespan_increase'] / 100)
    
    return {
        'Medicare Savings': medicare_savings,
        'GDP Impact': gdp_impact,
        'QALY Impact': qaly_impact
    }

def create_impact_breakdown(impacts, intervention, population_type, base_params):
    """Create a detailed breakdown of impact sources"""
    effects = intervention['default_effects']
    breakdown = []
    
    if 'healthcare' in effects:
        hospital_impact = (
            base_params['population'][population_type] * 
            base_params['economics']['medicare_per_capita'] * 
            base_params['health_baselines']['medicare_enrollment_rate'] *
            effects['healthcare']['hospital_visit_reduction'] / 100
        )
        breakdown.append({
            'Category': 'Hospital Visits',
            'Medicare Savings': hospital_impact
        })
    
    if 'cognitive' in effects and 'alzheimers_reduction' in effects['cognitive'] and population_type == 'over_60':
        alz_impact = (
            base_params['economics']['alzheimers_annual_cost'] * 
            effects['cognitive']['alzheimers_reduction'] / 100 * 
            intervention['impact_modifiers'].get('alzheimers_to_medicare', 0)
        )
        breakdown.append({
            'Category': "Alzheimer's",
            'Medicare Savings': alz_impact
        })
    
    if 'kidney' in effects and 'ckd_progression_reduction' in effects['kidney']:
        kidney_impact = (
            base_params['economics']['ckd_annual_cost'] * 
            effects['kidney']['ckd_progression_reduction'] / 100 * 
            intervention['impact_modifiers'].get('kidney_to_medicare', 0)
        )
        breakdown.append({
            'Category': 'Kidney Disease',
            'Medicare Savings': kidney_impact
        })
    
    return pd.DataFrame(breakdown)

def plot_medicare_breakdown(breakdown_df):
    """Create a bar chart showing Medicare savings by category"""
    fig = px.bar(
        breakdown_df,
        x='Category',
        y='Medicare Savings',
        title='Medicare Savings Breakdown',
        labels={'Medicare Savings': 'Annual Savings ($)'},
        color='Category'
    )
    fig.update_layout(
        showlegend=False,
        yaxis_tickformat='$,.0f'
    )
    return fig

def plot_population_comparison(intervention, base_params):
    """Create a comparison of impacts across population segments"""
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
            x=df['Population'],
            y=df[metric],
            text=df[metric].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
        ))
    
    fig.update_layout(
        title='Impact Comparison Across Populations',
        barmode='group',
        yaxis_tickformat='$,.0f'
    )
    
    return fig

def calculate_time_series(intervention, population_type, base_params, years=10):
    """Calculate impact over time"""
    annual_impact = calculate_impacts(intervention, population_type, base_params)
    
    # Initialize time series data
    years_range = range(years)
    cumulative_data = []
    
    # Calculate compound effects
    for year in years_range:
        # Assume some compound growth in benefits
        compound_factor = 1 + (year * 0.02)  # 2% compound effect each year
        
        medicare_savings = annual_impact['Medicare Savings'] * compound_factor
        gdp_impact = annual_impact['GDP Impact'] * compound_factor
        qaly_impact = annual_impact['QALY Impact'] * compound_factor
        
        cumulative_medicare = medicare_savings * (year + 1)
        cumulative_gdp = gdp_impact * (year + 1)
        cumulative_qaly = qaly_impact * (year + 1)
        
        cumulative_data.append({
            'Year': year + 1,
            'Annual Medicare Savings': medicare_savings,
            'Cumulative Medicare Savings': cumulative_medicare,
            'Annual GDP Impact': gdp_impact,
            'Cumulative GDP Impact': cumulative_gdp,
            'Annual QALY Impact': qaly_impact,
            'Cumulative QALY Impact': cumulative_qaly
        })
    
    return pd.DataFrame(cumulative_data)

def plot_time_series(time_series_df):
    """Create time series visualization"""
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add annual Medicare savings
    fig.add_trace(
        go.Scatter(
            x=time_series_df['Year'],
            y=time_series_df['Annual Medicare Savings'],
            name='Annual Medicare Savings',
            line=dict(color='blue')
        )
    )
    
    # Add cumulative Medicare savings
    fig.add_trace(
        go.Scatter(
            x=time_series_df['Year'],
            y=time_series_df['Cumulative Medicare Savings'],
            name='Cumulative Medicare Savings',
            line=dict(color='red', dash='dash')
        )
    )
    
    # Update layout
    fig.update_layout(
        title='Projected Medicare Savings Over Time',
        xaxis_title='Year',
        yaxis_title='Savings ($)',
        yaxis_tickformat='$,.0f',
        hovermode='x unified',
        showlegend=True
    )
    
    return fig

def plot_metrics_over_time(time_series_df):
    """Create a multi-metric time series comparison"""
    fig = go.Figure()
    
    metrics = [
        ('GDP Impact', 'Annual GDP Impact', 'Cumulative GDP Impact'),
        ('Medicare Savings', 'Annual Medicare Savings', 'Cumulative Medicare Savings'),
        ('QALY Impact', 'Annual QALY Impact', 'Cumulative QALY Impact')
    ]
    
    for metric_name, annual_col, cumulative_col in metrics:
        # Create subplot for each metric
        fig.add_trace(
            go.Scatter(
                x=time_series_df['Year'],
                y=time_series_df[annual_col],
                name=f'Annual {metric_name}',
                line=dict(dash='solid')
            )
        )
        fig.add_trace(
            go.Scatter(
                x=time_series_df['Year'],
                y=time_series_df[cumulative_col],
                name=f'Cumulative {metric_name}',
                line=dict(dash='dash')
            )
        )
    
    fig.update_layout(
        title='Projected Impact Metrics Over Time',
        xaxis_title='Year',
        yaxis_title='Value',
        yaxis_tickformat='$,.0f',
        hovermode='x unified',
        height=600,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig

# Streamlit UI
st.title('Health and Economic Impact Simulator')

# Sidebar controls
st.sidebar.header('Parameters')
intervention_data = load_interventions()
selected_intervention = st.sidebar.selectbox(
    'Select Intervention',
    options=list(intervention_data.keys()),
    format_func=lambda x: intervention_data[x]['name']
)

population_type = st.sidebar.selectbox(
    'Population Segment',
    options=['total_us', 'over_60', 'adult'],
    format_func=lambda x: x.replace('_', ' ').title()
)

# Display intervention description
intervention = intervention_data[selected_intervention]
st.markdown(f"## {intervention['name']}")
st.markdown(intervention['description'])

# Display key parameters
st.markdown("### Key Parameters")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Key Effects**")
    effects = intervention['default_effects']
    
    if 'physical' in effects:
        st.write(f"Muscle Mass Change: {effects['physical']['muscle_mass_change']} lbs")
        st.write(f"Fat Mass Change: {effects['physical']['fat_mass_change']} lbs")
    
    if 'cognitive' in effects:
        st.write(f"IQ Increase: {effects['cognitive']['iq_increase']} points")
        st.write(f"Alzheimer's Reduction: {effects['cognitive']['alzheimers_reduction']}%")

with col2:
    st.markdown("**Health Impacts**")
    if 'longevity' in effects:
        st.write(f"Lifespan Increase: {effects['longevity']['lifespan_increase']}%")
    if 'healthcare' in effects:
        st.write(f"Hospital Visit Reduction: {effects['healthcare']['hospital_visit_reduction']}%")
    if 'kidney' in effects:
        st.write(f"CKD Progression Reduction: {effects['kidney']['ckd_progression_reduction']}%")

# Calculate and display impacts
impacts = calculate_impacts(intervention, population_type, base_params)

st.markdown("### Impact Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Medicare Savings", f"${impacts['Medicare Savings']:,.0f}")
with col2:
    st.metric("GDP Impact", f"${impacts['GDP Impact']:,.0f}")
with col3:
    st.metric("QALY Impact", f"{impacts['QALY Impact']:,.0f}")

# Add visualizations
st.markdown("### Impact Analysis")

# Medicare savings breakdown
breakdown_df = create_impact_breakdown(impacts, intervention, population_type, base_params)
if not breakdown_df.empty:
    st.plotly_chart(plot_medicare_breakdown(breakdown_df), use_container_width=True)

# Population comparison
st.plotly_chart(plot_population_comparison(intervention, base_params), use_container_width=True)

# Add time series projections
st.markdown("### Long-term Impact Projections")

# Add year range selector
projection_years = st.slider("Projection Timeline (Years)", min_value=5, max_value=20, value=10)

# Calculate and display time series data
time_series_df = calculate_time_series(intervention, population_type, base_params, projection_years)

# Display Medicare savings over time
st.plotly_chart(plot_time_series(time_series_df), use_container_width=True)

# Display all metrics over time
st.plotly_chart(plot_metrics_over_time(time_series_df), use_container_width=True)

# Add summary of long-term impact
final_year = time_series_df.iloc[-1]
st.markdown(f"""
### Cumulative Impact After {projection_years} Years
- Total Medicare Savings: ${final_year['Cumulative Medicare Savings']:,.0f}
- Total GDP Impact: ${final_year['Cumulative GDP Impact']:,.0f}
- Total QALYs Gained: {final_year['Cumulative QALY Impact']:,.0f}
""")

# Generate report
if st.button('Generate Report'):
    st.markdown("### Executive Summary")
    
    # Create impact statements based on intervention type
    impact_statements = []
    effects = intervention['default_effects']
    
    if 'cognitive' in effects:
        if 'iq_increase' in effects['cognitive']:
            impact_statements.append(f"* IQ increase of {effects['cognitive']['iq_increase']} points")
        if 'alzheimers_reduction' in effects['cognitive']:
            impact_statements.append(f"* {effects['cognitive']['alzheimers_reduction']}% reduction in Alzheimer's progression")
    
    if 'kidney' in effects:
        if 'ckd_progression_reduction' in effects['kidney']:
            impact_statements.append(f"* {effects['kidney']['ckd_progression_reduction']}% reduction in CKD progression")
    
    if 'physical' in effects:
        impact_statements.append(f"* {effects['physical']['muscle_mass_change']} lbs muscle mass increase")
    
    if 'longevity' in effects:
        impact_statements.append(f"* {effects['longevity']['lifespan_increase']}% lifespan increase")
    
    effects_text = "\n".join(impact_statements)
    
    st.markdown(f"""
    Analysis of {intervention['name']} shows significant potential impact:
    
    * Annual Medicare savings of ${impacts['Medicare Savings']:,.0f}
    * GDP increase of ${impacts['GDP Impact']:,.0f}
    * {impacts['QALY Impact']:,.0f} Quality Adjusted Life Years gained
    
    These calculations are based on effects including:
    {effects_text}
    """)

# Add footer
st.markdown("---")
st.markdown("*This is an MVP version for demonstration purposes. Values are estimates based on provided parameters.*") 