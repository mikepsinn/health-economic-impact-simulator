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
        x='Medicare Savings',
        y='Category',
        title='Medicare Savings Breakdown',
        labels={'Medicare Savings': 'Annual Savings'},
        color='Category',
        orientation='h'
    )
    
    # Format text labels
    fig.update_traces(
        text=[format_large_number(x) for x in breakdown_df['Medicare Savings']],
        textposition='auto'
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis_tickformat='$,.0f',
        height=400,
        margin=dict(l=20, r=20, t=50, b=50),
        title_x=0.5,
        title_y=0.98,
        yaxis_title=None
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

def calculate_time_series(intervention, population_type, base_params, years=10, growth_rate=0.02):
    """Calculate impact over time with configurable growth rate"""
    annual_impact = calculate_impacts(intervention, population_type, base_params)
    
    years_range = range(years)
    cumulative_data = []
    
    for year in years_range:
        compound_factor = 1 + (year * growth_rate)
        
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
    fig = go.Figure()
    
    # Add annual Medicare savings
    fig.add_trace(
        go.Scatter(
            x=time_series_df['Year'],
            y=time_series_df['Annual Medicare Savings'],
            name='Annual',
            line=dict(color='blue')
        )
    )
    
    # Add cumulative Medicare savings
    fig.add_trace(
        go.Scatter(
            x=time_series_df['Year'],
            y=time_series_df['Cumulative Medicare Savings'],
            name='Cumulative',
            line=dict(color='red', dash='dash')
        )
    )
    
    # Update layout
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

def plot_metrics_over_time(time_series_df):
    """Create a multi-metric time series comparison"""
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

def format_large_number(num):
    """Format large numbers into B/M format"""
    abs_num = abs(num)
    if abs_num >= 1e9:
        return f"${abs_num/1e9:.1f}B"
    elif abs_num >= 1e6:
        return f"${abs_num/1e6:.1f}M"
    else:
        return f"${abs_num:,.0f}"

# Streamlit UI
st.title('Health and Economic Impact Simulator')

# Add custom CSS for section spacing
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h2, h3 {
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

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

# Calculate impacts first
impacts = calculate_impacts(intervention, population_type, base_params)

# Display key parameters
st.markdown("### Key Parameters")
st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
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
st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
st.markdown("### Impact Summary")
st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Medicare Savings", format_large_number(impacts['Medicare Savings']))
with col2:
    st.metric("GDP Impact", format_large_number(impacts['GDP Impact']))
with col3:
    st.metric("QALY Impact", f"{impacts['QALY Impact']:,.0f}")

# Add visualizations
st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
st.markdown("### Impact Analysis")
st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Medicare savings breakdown
breakdown_df = create_impact_breakdown(impacts, intervention, population_type, base_params)
if not breakdown_df.empty:
    st.plotly_chart(plot_medicare_breakdown(breakdown_df), use_container_width=True)
    st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)

# Population comparison
st.plotly_chart(plot_population_comparison(intervention, base_params), use_container_width=True)
st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)

# Add time series projections
st.markdown("### Long-term Impact Projections")
st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Add year range selector
projection_years = st.slider("Projection Timeline (Years)", min_value=5, max_value=20, value=10)
st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# Calculate and display time series data
time_series_df = calculate_time_series(intervention, population_type, base_params, projection_years)

# Display Medicare savings over time
st.plotly_chart(plot_time_series(time_series_df), use_container_width=True)
st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)

# Display all metrics over time
st.plotly_chart(plot_metrics_over_time(time_series_df), use_container_width=True)
st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)

# Add summary of long-term impact
final_year = time_series_df.iloc[-1]
st.markdown(f"""
### Cumulative Impact After {projection_years} Years
- Total Medicare Savings: ${final_year['Cumulative Medicare Savings']:,.0f}
- Total GDP Impact: ${final_year['Cumulative GDP Impact']:,.0f}
- Total QALYs Gained: {final_year['Cumulative QALY Impact']:,.0f}
""")
st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)

# Add sensitivity analysis
st.markdown("### Sensitivity Analysis")
st.markdown("Explore how changes in key parameters affect the outcomes.")
st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# Create columns for sensitivity controls
sens_col1, sens_col2 = st.columns(2)

with sens_col1:
    # Effect magnitude adjustment
    effect_multiplier = st.slider(
        "Effect Magnitude Multiplier",
        min_value=0.5,
        max_value=1.5,
        value=1.0,
        step=0.1,
        help="Adjust the magnitude of all effects up or down"
    )

with sens_col2:
    # Compound growth rate adjustment
    growth_rate = st.slider(
        "Annual Compound Growth Rate",
        min_value=0.0,
        max_value=0.05,
        value=0.02,
        step=0.005,
        format="%.1f%%",
        help="Adjust the annual compound growth rate of benefits"
    )

# Calculate sensitivity scenarios
def calculate_sensitivity_scenarios(intervention, population_type, base_params, effect_mult, growth_rate):
    # Create three scenarios
    scenarios = {
        'Conservative': {'effect_mult': effect_mult * 0.8, 'growth': growth_rate * 0.8},
        'Base Case': {'effect_mult': effect_mult, 'growth': growth_rate},
        'Optimistic': {'effect_mult': effect_mult * 1.2, 'growth': growth_rate * 1.2}
    }
    
    results = {}
    for scenario, params in scenarios.items():
        # Modify intervention effects
        modified_intervention = intervention.copy()
        for category in modified_intervention['default_effects']:
            if isinstance(modified_intervention['default_effects'][category], dict):
                for key in modified_intervention['default_effects'][category]:
                    modified_intervention['default_effects'][category][key] *= params['effect_mult']
        
        # Calculate time series with modified growth rate
        df = calculate_time_series(
            modified_intervention,
            population_type,
            base_params,
            years=10,
            growth_rate=params['growth']
        )
        results[scenario] = df.iloc[-1]  # Get final year values
    
    return pd.DataFrame(results).T

# Calculate and display sensitivity analysis
sensitivity_results = calculate_sensitivity_scenarios(
    intervention,
    population_type,
    base_params,
    effect_multiplier,
    growth_rate
)

# Create sensitivity comparison chart
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

st.plotly_chart(fig, use_container_width=True)
st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# Display scenario details
st.markdown("#### Scenario Details (10-Year Cumulative Impact)")
for scenario in sensitivity_results.index:
    st.markdown(f"""
    **{scenario}**
    - Medicare Savings: {format_large_number(sensitivity_results.loc[scenario, 'Cumulative Medicare Savings'])}
    - GDP Impact: {format_large_number(sensitivity_results.loc[scenario, 'Cumulative GDP Impact'])}
    - QALYs Gained: {sensitivity_results.loc[scenario, 'Cumulative QALY Impact']:,.0f}
    """)
    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Add footer
st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Health and Economic Impact Simulator") 