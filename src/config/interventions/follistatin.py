"""Follistatin intervention configuration."""

from src.models.config import (
    InterventionConfig,
    InterventionEffects,
    PhysicalEffects,
    LongevityEffects,
    HealthcareEffects
)

# Define intervention effects
effects = InterventionEffects(
    physical=PhysicalEffects(
        muscle_mass_change=2.0,
        fat_mass_change=-2.0
    ),
    longevity=LongevityEffects(
        lifespan_increase=2.5,
        healthspan_improvement=80.0
    ),
    healthcare=HealthcareEffects(
        hospital_visit_reduction=15.0
    )
)

# Create intervention config
config = InterventionConfig(
    name="Follistatin",
    description="Muscle growth and fat reduction therapeutic protein",
    default_effects=effects
) 