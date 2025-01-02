from typing import Dict, Any, Tuple, NamedTuple

class ParameterDefinition(NamedTuple):
    """Definition for a parameter including its range and help text."""
    min_value: float
    max_value: float
    step: float
    help_text: str
    unit: str = ""
    format: str = ""

class ImpactModifierDefinition(NamedTuple):
    """Definition for an impact modifier including its range and help text."""
    min_value: float
    max_value: float
    step: float
    help_text: str
    default_value: float

# Effect parameter definitions
EFFECT_PARAMETERS = {
    'muscle_mass_change': ParameterDefinition(
        min_value=-5.0,
        max_value=10.0,
        step=0.5,
        unit="lbs",
        help_text="Expected change in muscle mass. Positive values indicate muscle gain, negative values indicate loss."
    ),
    'fat_mass_change': ParameterDefinition(
        min_value=-10.0,
        max_value=5.0,
        step=0.5,
        unit="lbs",
        help_text="Expected change in fat mass. Negative values indicate fat loss, positive values indicate gain."
    ),
    'iq_increase': ParameterDefinition(
        min_value=0.0,
        max_value=10.0,
        step=0.5,
        unit="points",
        help_text="Expected increase in IQ points. Higher values indicate greater cognitive enhancement."
    ),
    'alzheimers_reduction': ParameterDefinition(
        min_value=0.0,
        max_value=50.0,
        step=5.0,
        unit="%",
        help_text="Percentage reduction in Alzheimer's disease progression rate."
    ),
    'egfr_improvement': ParameterDefinition(
        min_value=0.0,
        max_value=15.0,
        step=0.5,
        unit="mL/min/1.73m²",
        help_text="Expected improvement in estimated Glomerular Filtration Rate (eGFR), a key measure of kidney function."
    ),
    'ckd_progression_reduction': ParameterDefinition(
        min_value=0.0,
        max_value=50.0,
        step=5.0,
        unit="%",
        help_text="Percentage reduction in Chronic Kidney Disease (CKD) progression rate."
    ),
    'lifespan_increase': ParameterDefinition(
        min_value=0.0,
        max_value=5.0,
        step=0.1,
        unit="%",
        help_text="Expected percentage increase in lifespan."
    ),
    'hospital_visit_reduction': ParameterDefinition(
        min_value=0.0,
        max_value=50.0,
        step=5.0,
        unit="%",
        help_text="Expected percentage reduction in hospital visits."
    )
}

# Impact modifier definitions
IMPACT_MODIFIERS = {
    'iq_to_gdp': ImpactModifierDefinition(
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        default_value=0.02,
        help_text="Conversion factor from IQ increase to GDP impact. A value of 0.02 means each IQ point increases productivity by 2%."
    ),
    'kidney_to_medicare': ImpactModifierDefinition(
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        default_value=0.15,
        help_text="Proportion of kidney disease improvement that translates to Medicare savings."
    ),
    'alzheimers_to_medicare': ImpactModifierDefinition(
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        default_value=0.20,
        help_text="Proportion of Alzheimer's reduction that translates to Medicare savings."
    ),
    'health_quality': ImpactModifierDefinition(
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        default_value=0.08,
        help_text="Overall improvement in quality of life, affecting QALY calculations."
    ),
    'lifespan_to_gdp': ImpactModifierDefinition(
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        default_value=0.8,
        help_text="Proportion of lifespan increase that contributes to GDP through extended productivity."
    ),
    'muscle_to_falls': ImpactModifierDefinition(
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        default_value=0.1,
        help_text="Impact of muscle mass increase on fall reduction. A value of 0.1 means each pound of muscle reduces falls by 10%."
    )
}

# Population segment definitions
POPULATION_SEGMENTS = {
    'total_us': "Total US population, representing the broadest possible impact.",
    'over_60': "Population over 60 years old, particularly relevant for age-related interventions.",
    'adult': "Adult population (18+), excluding children and adolescents."
}

# Sensitivity analysis definitions
SENSITIVITY_PARAMETERS = {
    'effect_multiplier': ParameterDefinition(
        min_value=0.5,
        max_value=1.5,
        step=0.1,
        help_text="Adjusts the magnitude of all effects up or down. Values below 1 represent more conservative estimates, above 1 more optimistic.",
        format="%.1fx"
    ),
    'growth_rate': ParameterDefinition(
        min_value=0.0,
        max_value=0.05,
        step=0.005,
        help_text="Annual compound growth rate of benefits. Higher rates indicate accelerating returns over time.",
        format="%.1f%%"
    )
}

def get_parameter_range(param_name: str) -> Tuple[float, float, float]:
    """Get the range values for a parameter."""
    param = EFFECT_PARAMETERS[param_name]
    return (param.min_value, param.max_value, param.step)

def get_parameter_help(param_name: str) -> str:
    """Get the help text for a parameter."""
    return EFFECT_PARAMETERS[param_name].help_text

def get_modifier_help(modifier_name: str) -> str:
    """Get the help text for an impact modifier."""
    return IMPACT_MODIFIERS[modifier_name].help_text

def get_population_help(segment: str) -> str:
    """Get the help text for a population segment."""
    return POPULATION_SEGMENTS[segment] 