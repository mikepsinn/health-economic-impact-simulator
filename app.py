import streamlit as st
import yaml
import os
import pandas as pd
import plotly.graph_objects as go
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
    
    # Calculate Medicare impact
    hospital_reduction = effects['healthcare']['hospital_visit_reduction'] / 100
    medicare_savings = (
        pop * 
        base_params['economics']['medicare_per_capita'] * 
        base_params['health_baselines']['medicare_enrollment_rate'] *
        hospital_reduction
    )
    
    # Calculate GDP impact
    lifespan_impact = effects['longevity']['lifespan_increase'] / 100
    gdp_impact = (
        pop * 
        base_params['economics']['gdp_per_capita'] * 
        lifespan_impact * 
        modifiers['lifespan_to_gdp']
    )
    
    # Calculate QALYs
    qaly_impact = pop * (
        lifespan_impact + 
        modifiers['health_quality']
    )
    
    return {
        'Medicare Savings': medicare_savings,
        'GDP Impact': gdp_impact,
        'QALY Impact': qaly_impact
    }

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
    st.markdown("**Physical Effects**")
    st.write(f"Muscle Mass Change: {intervention['default_effects']['physical']['muscle_mass_change']} lbs")
    st.write(f"Fat Mass Change: {intervention['default_effects']['physical']['fat_mass_change']} lbs")

with col2:
    st.markdown("**Longevity Effects**")
    st.write(f"Lifespan Increase: {intervention['default_effects']['longevity']['lifespan_increase']}%")
    st.write(f"Hospital Visit Reduction: {intervention['default_effects']['healthcare']['hospital_visit_reduction']}%")

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

# Generate report
if st.button('Generate Report'):
    st.markdown("### Executive Summary")
    st.markdown(f"""
    Analysis of {intervention['name']} shows significant potential impact:
    
    * Annual Medicare savings of ${impacts['Medicare Savings']:,.0f}
    * GDP increase of ${impacts['GDP Impact']:,.0f}
    * {impacts['QALY Impact']:,.0f} Quality Adjusted Life Years gained
    
    These calculations are based on effects including:
    * {intervention['default_effects']['physical']['muscle_mass_change']} lbs muscle mass increase
    * {intervention['default_effects']['longevity']['lifespan_increase']}% lifespan increase
    * {intervention['default_effects']['healthcare']['hospital_visit_reduction']}% reduction in hospital visits
    """)

# Add footer
st.markdown("---")
st.markdown("*This is an MVP version for demonstration purposes. Values are estimates based on provided parameters.*") 