"""Main Streamlit application for the health economic impact simulator."""

import streamlit as st
from ..config.loader import (
    load_base_parameters, 
    load_interventions,
    PARAMETER_RANGES,
    MODIFIER_RANGES
)
from ..core.calculations import (
    calculate_impacts,
    calculate_time_series,
    calculate_sensitivity_scenarios,
    format_large_number
)
from ..visualization.plots import (
    plot_medicare_breakdown,
    plot_population_comparison,
    plot_time_series,
    plot_metrics_over_time,
    plot_sensitivity_comparison
)
from parameter_definitions import (
    EFFECT_PARAMETERS,
    IMPACT_MODIFIERS,
    POPULATION_SEGMENTS,
    SENSITIVITY_PARAMETERS,
    get_parameter_help,
    get_modifier_help,
    get_population_help
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

# App title and introduction
st.title('Health and Economic Impact Simulator')

with st.expander("ℹ️ About this simulator"):
    st.markdown("""
    This simulator helps evaluate the economic and health impacts of various therapeutic interventions.
    
    **Key Features:**
    - 🔄 Real-time impact calculations
    - 📊 Interactive visualizations
    - 📈 Long-term projections
    - 🎯 Sensitivity analysis
    
    **How to use:**
    1. Select an intervention and population segment in the sidebar
    2. Adjust parameters to explore different scenarios
    3. View impacts across different metrics and timeframes
    4. Use sensitivity analysis to understand potential ranges of outcomes
    
    **Understanding the metrics:**
    - **Medicare Savings**: Direct cost reductions in Medicare spending
    - **GDP Impact**: Economic benefits through productivity and longevity
    - **QALY Impact**: Quality-Adjusted Life Years gained
    
    *Hover over any parameter or metric to see detailed explanations.*
    """)

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
    format_func=lambda x: x.replace('_', ' ').title(),
    help=get_population_help('total_us')  # Default help text
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
            if param_name in EFFECT_PARAMETERS:
                param_def = EFFECT_PARAMETERS[param_name]
                label = f"{param_name.replace('_', ' ').title()}"
                if param_def.unit:
                    label += f" ({param_def.unit})"
                effects[effect_type][param_name] = st.sidebar.slider(
                    label,
                    min_value=param_def.min_value,
                    max_value=param_def.max_value,
                    value=float(value),
                    step=param_def.step,
                    help=param_def.help_text
                )

# Impact modifier adjustments
st.sidebar.markdown("#### Impact Modifiers")
for key, value in intervention['impact_modifiers'].items():
    if key in IMPACT_MODIFIERS:
        mod_def = IMPACT_MODIFIERS[key]
        display_name = " ".join(word.capitalize() for word in key.split('_'))
        intervention['impact_modifiers'][key] = st.sidebar.slider(
            display_name,
            min_value=mod_def.min_value,
            max_value=mod_def.max_value,
            value=float(value),
            step=mod_def.step,
            help=mod_def.help_text
        )

# Display intervention description
st.markdown(f"## {intervention['name']}")
st.markdown(intervention['description'])

# Calculate impacts
impacts = calculate_impacts(intervention, population_type, base_params)

# Display key parameters
st.markdown("### Key Parameters")
st.markdown("Current parameter values and their effects on the model. Click any parameter to adjust its value in the sidebar.")
st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Create columns for organization
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Effect Parameters")
    for effect_type, effect_params in effects.items():
        if isinstance(effect_params, dict):
            st.markdown(f"**{effect_type.replace('_', ' ').title()}**")
            for param_name, value in effect_params.items():
                if param_name in EFFECT_PARAMETERS:
                    param_def = EFFECT_PARAMETERS[param_name]
                    unit_str = f" {param_def.unit}" if param_def.unit else ""
                    # Parameter value with link to sidebar
                    st.markdown(
                        f"*<a href='#' onclick=\"javascript:document.querySelector('[data-testid=\\'stSidebar\\'] [aria-label=\\'{param_name.replace('_', ' ').title()}\\']').scrollIntoView(); return false;\">"
                        f"{param_name.replace('_', ' ').title()}</a>:* {value}{unit_str} "
                        f"<small><em>(click to adjust)</em></small>",
                        unsafe_allow_html=True
                    )
                    # Help text in muted color
                    st.markdown(
                        f"<div style='color: #666; font-size: 0.9em; margin-bottom: 1em;'>{param_def.help_text}</div>",
                        unsafe_allow_html=True
                    )

with col2:
    st.markdown("#### Impact Modifiers")
    st.markdown("Factors that determine how effects translate to outcomes:")
    for key, value in intervention['impact_modifiers'].items():
        if key in IMPACT_MODIFIERS:
            mod_def = IMPACT_MODIFIERS[key]
            # Parameter value with link to sidebar
            st.markdown(
                f"*<a href='#' onclick=\"javascript:document.querySelector('[data-testid=\\'stSidebar\\'] [aria-label=\\'{key.replace('_', ' ').title()}\\']').scrollIntoView(); return false;\">"
                f"{key.replace('_', ' ').title()}</a>:* {value:.2f} "
                f"<small><em>(click to adjust)</em></small>",
                unsafe_allow_html=True
            )
            # Help text in muted color
            st.markdown(
                f"<div style='color: #666; font-size: 0.9em; margin-bottom: 1em;'>{mod_def.help_text}</div>",
                unsafe_allow_html=True
            )

st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# Display impact summary
st.markdown("### Impact Summary")
st.markdown("Key metrics showing the overall impact of the intervention.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Medicare Savings", 
        format_large_number(impacts['Medicare Savings']),
        help="Annual Medicare cost savings from all combined effects"
    )
with col2:
    st.metric(
        "GDP Impact", 
        format_large_number(impacts['GDP Impact']),
        help="Total economic impact through productivity and longevity improvements"
    )
with col3:
    st.metric(
        "QALY Impact", 
        f"{impacts['QALY Impact']:,.0f}",
        help="Quality-Adjusted Life Years gained through health improvements and extended lifespan"
    )

# Display visualizations
st.markdown("### Impact Analysis")
st.markdown("""
This section shows how the intervention's impacts vary across different population segments 
and provides a detailed breakdown of savings sources.
""")

# Population comparison
st.markdown("#### Population Segment Comparison")
st.markdown("""
Compare the intervention's impact across different population segments. 
The bars show annual savings and impact for each group.
""")
st.plotly_chart(plot_population_comparison(intervention, base_params), use_container_width=True)
st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)

# Time series projections
st.markdown("### Long-term Impact Projections")
st.markdown("""
Explore how the intervention's impacts compound over time. Adjust the timeline and growth 
parameters to see different scenarios.
""")

projection_years = st.slider(
    "Projection Timeline (Years)", 
    min_value=5, 
    max_value=20, 
    value=10,
    help="Number of years to project the intervention's impacts into the future"
)

# Calculate and display time series
time_series_df = calculate_time_series(intervention, population_type, base_params, projection_years)
st.markdown("#### Medicare Savings Trajectory")
st.markdown("Annual and cumulative Medicare savings over the projection period.")
st.plotly_chart(plot_time_series(time_series_df), use_container_width=True)

st.markdown("#### All Metrics Over Time")
st.markdown("Compare how different impact metrics evolve over time. Click legend items to show/hide metrics.")
st.plotly_chart(plot_metrics_over_time(time_series_df), use_container_width=True)

# Sensitivity analysis
st.markdown("### Sensitivity Analysis")
st.markdown("""
Explore how changes in key assumptions affect the projected outcomes. This helps understand 
the range of possible impacts under different scenarios.

- **Conservative**: Lower bound estimate (80% of base values)
- **Base Case**: Current parameter values
- **Optimistic**: Upper bound estimate (120% of base values)
""")

sens_col1, sens_col2 = st.columns(2)

with sens_col1:
    sens_def = SENSITIVITY_PARAMETERS['effect_multiplier']
    effect_multiplier = st.slider(
        "Effect Magnitude Multiplier",
        min_value=sens_def.min_value,
        max_value=sens_def.max_value,
        value=1.0,
        step=sens_def.step,
        format=sens_def.format,
        help=sens_def.help_text
    )
    st.markdown("""
    <small>Adjusts all effect magnitudes up or down proportionally. 
    Use this to explore more conservative or optimistic scenarios.</small>
    """, unsafe_allow_html=True)

with sens_col2:
    sens_def = SENSITIVITY_PARAMETERS['growth_rate']
    growth_rate = st.slider(
        "Annual Compound Growth Rate",
        min_value=sens_def.min_value,
        max_value=sens_def.max_value,
        value=0.02,
        step=sens_def.step,
        format=sens_def.format,
        help=sens_def.help_text
    )
    st.markdown("""
    <small>Rate at which benefits compound over time. 
    Higher rates suggest accelerating returns from the intervention.</small>
    """, unsafe_allow_html=True)

# Calculate and display sensitivity analysis
sensitivity_results = calculate_sensitivity_scenarios(
    intervention,
    population_type,
    base_params,
    effect_multiplier,
    growth_rate
)

st.plotly_chart(plot_sensitivity_comparison(sensitivity_results), use_container_width=True)

# Display scenario details with explanations
st.markdown("#### Scenario Details (10-Year Cumulative Impact)")
st.markdown("""
Each scenario represents a different set of assumptions about the intervention's effectiveness 
and how benefits accumulate over time.
""")

for scenario in sensitivity_results.index:
    st.markdown(f"""
    **{scenario}**
    - Medicare Savings: {format_large_number(sensitivity_results.loc[scenario, 'Cumulative Medicare Savings'])}
    - GDP Impact: {format_large_number(sensitivity_results.loc[scenario, 'Cumulative GDP Impact'])}
    - QALYs Gained: {sensitivity_results.loc[scenario, 'Cumulative QALY Impact']:,.0f}
    """)

# Footer with additional context
st.markdown("---")
st.markdown("""
*This is an MVP version for demonstration purposes. Values are estimates based on provided parameters.*

**Note on Uncertainty:**
- All projections are based on current understanding and available data
- Actual results may vary based on implementation and external factors
- Regular updates to parameters and assumptions will improve accuracy
""")

# Add a final help text about data interpretation
with st.expander("📊 How to Interpret These Results"):
    st.markdown("""
    **Understanding the Projections:**
    1. **Base Case** represents our current best estimates
    2. **Conservative** and **Optimistic** scenarios help understand the range of possible outcomes
    3. Long-term projections become more uncertain over time
    
    **Key Considerations:**
    - Results are most reliable for near-term projections
    - Multiple scenarios should be considered for decision-making
    - Regular updates to parameters may change projections
    
    **Using This Information:**
    - Compare different interventions using the same assumptions
    - Focus on relative differences between scenarios
    - Consider both immediate and long-term impacts
    """) 