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