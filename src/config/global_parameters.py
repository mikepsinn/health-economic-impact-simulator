"""Global parameters for economic impact models."""

from src.models.config import (
    BaseConfig,
    PopulationConfig,
    EconomicsConfig,
    HealthcareConfig,
    ImpactModifiers
)

# Population parameters
population = PopulationConfig(
    total_population=331900000,  # Total US population
    target_population=165950000,  # Population that could benefit
    medicare_beneficiaries=61733400,  # Medicare enrollment
    workforce_fraction=0.63  # Labor force participation rate
)

# Economic parameters
economics = EconomicsConfig(
    annual_healthcare_cost=12500.0,  # Per person
    annual_productivity=68000.0,  # GDP per worker
    discount_rate=0.03  # Standard 3% rate
)

# Healthcare system parameters
healthcare = HealthcareConfig(
    annual_hospital_visits=36500000,  # Total annual hospital visits
    annual_alzheimers_cost=305000000000.0,  # Total Alzheimer's cost
    annual_ckd_cost=87000000000.0,  # Total CKD cost
    savings_per_lb_muscle=12.0,  # Healthcare savings per pound muscle gain
    savings_per_lb_fat=8.0,  # Healthcare savings per pound fat loss
    cost_per_hospital_visit=12500.0 * 331900000 / 36500000  # Total healthcare cost / visits
)

# Global impact modifiers
impact_modifiers = ImpactModifiers(
    iq_to_gdp=0.02,  # GDP increase per IQ point
    kidney_to_medicare=0.4,  # Medicare savings from kidney improvement
    alzheimers_to_medicare=0.5,  # Medicare savings from Alzheimer's reduction
    health_quality=0.8,  # Quality of life improvement
    lifespan_to_gdp=0.6  # GDP conversion from lifespan increase
)

# Combined configuration
config = BaseConfig(
    population=population,
    economics=economics,
    healthcare=healthcare,
    impact_modifiers=impact_modifiers
) 