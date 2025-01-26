"""Klotho intervention configuration."""

from src.models.config import (
    InterventionConfig,
    InterventionEffects,
    CognitiveEffects,
    KidneyEffects,
    PhysicalEffects,
    LongevityEffects,
    HealthcareEffects
)

# Define intervention effects
effects = InterventionEffects(
    cognitive=CognitiveEffects(
        iq_increase=2.5,
        alzheimers_reduction=15.0
    ),
    kidney=KidneyEffects(
        egfr_improvement=8.0,
        ckd_progression_reduction=20.0
    ),
    physical=PhysicalEffects(
        muscle_mass_change=1.5,
        fat_mass_change=-1.0
    ),
    longevity=LongevityEffects(
        lifespan_increase=2.0,
        healthspan_improvement=80.0
    ),
    healthcare=HealthcareEffects(
        hospital_visit_reduction=12.0
    )
)

# Create intervention config
config = InterventionConfig(
    name="Klotho",
    description="A protein that regulates aging and metabolism",
    default_effects=effects
) 