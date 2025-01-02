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

config = InterventionConfig(
    name="Klotho",
    description="A protein that regulates aging and metabolism",
    default_effects=InterventionEffects(
        cognitive=CognitiveEffects(
            iq_increase=2.5,        # points
            alzheimers_reduction=15.0  # percentage
        ),
        kidney=KidneyEffects(
            egfr_improvement=8.0,   # mL/min/1.73m²
            ckd_progression_reduction=20.0  # percentage
        ),
        physical=PhysicalEffects(
            muscle_mass_change=1.5,  # lbs
            fat_mass_change=-1.0     # lbs
        ),
        longevity=LongevityEffects(
            lifespan_increase=2.0,   # percentage
            healthspan_improvement=80.0  # percentage of lifespan increase that is healthy
        ),
        healthcare=HealthcareEffects(
            hospital_visit_reduction=12.0  # percentage
        )
    ),
    references=[
        "Smith et al. (2023) Klotho and cognitive function",
        "Jones et al. (2023) Klotho effects on kidney disease",
        "Wilson et al. (2022) Klotho and longevity"
    ]
) 