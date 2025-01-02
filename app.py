import streamlit as st
from config_loader import (
    load_base_parameters, 
    load_interventions,
    PARAMETER_RANGES,
    MODIFIER_RANGES
)
from calculations import (
    calculate_impacts,
    calculate_time_series,
    calculate_sensitivity_scenarios,
    format_large_number
)
from visualizations import (
    plot_medicare_breakdown,
    plot_population_comparison,
    plot_time_series,
    plot_metrics_over_time,
    plot_sensitivity_comparison
)

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

# App title
st.title('Health and Economic Impact Simulator')

# Load configurations
base_params = load_base_parameters()
intervention_data = load_interventions()

# Sidebar controls
st.sidebar.header('Parameters')
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

# Parameter adjustment section
st.sidebar.markdown("### Adjust Parameters")
st.sidebar.markdown("Modify the intervention parameters to see their impact.")

# Create a deep copy of the intervention for modification
intervention = intervention_data[selected_intervention].copy()
effects = intervention['default_effects']

# Add parameter sliders based on effect types
for effect_type, effect_params in effects.items():
    if isinstance(effect_params, dict):
        st.sidebar.markdown(f"#### {effect_type.replace('_', ' ').title()}")
        for param_name, value in effect_params.items():
            if param_name in PARAMETER_RANGES:
                min_val, max_val, step = PARAMETER_RANGES[param_name]
                effects[effect_type][param_name] = st.sidebar.slider(
                    param_name.replace('_', ' ').title(),
                    min_value=min_val,
                    max_value=max_val,
                    value=float(value),
                    step=step
                )

# Impact modifier adjustments
st.sidebar.markdown("#### Impact Modifiers")
for key, value in intervention['impact_modifiers'].items():
    display_name = " ".join(word.capitalize() for word in key.split('_'))
    intervention['impact_modifiers'][key] = st.sidebar.slider(
        display_name,
        min_value=MODIFIER_RANGES['min_value'],
        max_value=MODIFIER_RANGES['max_value'],
        value=float(value),
        step=MODIFIER_RANGES['step']
    )

# Display intervention description
st.markdown(f"## {intervention['name']}")
st.markdown(intervention['description'])

# Calculate impacts
impacts = calculate_impacts(intervention, population_type, base_params)

# Display key parameters
st.markdown("### Key Parameters")
st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Key Effects**")
    for effect_type, effect_params in effects.items():
        if isinstance(effect_params, dict):
            for param_name, value in effect_params.items():
                st.write(f"{param_name.replace('_', ' ').title()}: {value}")

with col2:
    st.markdown("**Impact Modifiers**")
    for key, value in intervention['impact_modifiers'].items():
        st.write(f"{key.replace('_', ' ').title()}: {value:.2f}")

# Display impact summary
st.markdown("### Impact Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Medicare Savings", format_large_number(impacts['Medicare Savings']))
with col2:
    st.metric("GDP Impact", format_large_number(impacts['GDP Impact']))
with col3:
    st.metric("QALY Impact", f"{impacts['QALY Impact']:,.0f}")

# Display visualizations
st.markdown("### Impact Analysis")

# Population comparison
st.plotly_chart(plot_population_comparison(intervention, base_params), use_container_width=True)
st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)

# Time series projections
st.markdown("### Long-term Impact Projections")
projection_years = st.slider("Projection Timeline (Years)", min_value=5, max_value=20, value=10)

# Calculate and display time series
time_series_df = calculate_time_series(intervention, population_type, base_params, projection_years)
st.plotly_chart(plot_time_series(time_series_df), use_container_width=True)
st.plotly_chart(plot_metrics_over_time(time_series_df), use_container_width=True)

# Sensitivity analysis
st.markdown("### Sensitivity Analysis")
sens_col1, sens_col2 = st.columns(2)

with sens_col1:
    effect_multiplier = st.slider(
        "Effect Magnitude Multiplier",
        min_value=0.5,
        max_value=1.5,
        value=1.0,
        step=0.1,
        help="Adjust the magnitude of all effects up or down"
    )

with sens_col2:
    growth_rate = st.slider(
        "Annual Compound Growth Rate",
        min_value=0.0,
        max_value=0.05,
        value=0.02,
        step=0.005,
        format="%.1f%%",
        help="Adjust the annual compound growth rate of benefits"
    )

# Calculate and display sensitivity analysis
sensitivity_results = calculate_sensitivity_scenarios(
    intervention,
    population_type,
    base_params,
    effect_multiplier,
    growth_rate
)

st.plotly_chart(plot_sensitivity_comparison(sensitivity_results), use_container_width=True)

# Display scenario details
st.markdown("#### Scenario Details (10-Year Cumulative Impact)")
for scenario in sensitivity_results.index:
    st.markdown(f"""
    **{scenario}**
    - Medicare Savings: {format_large_number(sensitivity_results.loc[scenario, 'Cumulative Medicare Savings'])}
    - GDP Impact: {format_large_number(sensitivity_results.loc[scenario, 'Cumulative GDP Impact'])}
    - QALYs Gained: {sensitivity_results.loc[scenario, 'Cumulative QALY Impact']:,.0f}
    """)

# Footer
st.markdown("---")
st.markdown("*This is an MVP version for demonstration purposes. Values are estimates based on provided parameters.*") 