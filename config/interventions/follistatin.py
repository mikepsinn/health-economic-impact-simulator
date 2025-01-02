"""Follistatin intervention configuration."""

from src.models.config import (
    InterventionConfig,
    InterventionEffects,
    PhysicalEffects,
    LongevityEffects,
    HealthcareEffects,
    BiomarkerEffects
)

config = InterventionConfig(
    name="Follistatin",
    description="Muscle growth and fat reduction therapeutic protein",
    default_effects=InterventionEffects(
        physical=PhysicalEffects(
            muscle_mass_change=2.0,  # lbs
            fat_mass_change=-2.0     # lbs
        ),
        longevity=LongevityEffects(
            lifespan_increase=2.5,   # percentage
            healthspan_improvement=80.0  # percentage of lifespan increase that is healthy
        ),
        healthcare=HealthcareEffects(
            hospital_visit_reduction=15.0  # percentage
        ),
        biomarkers=BiomarkerEffects(
            egfr_change=5.0,         # mL/min/1.73m²
            cystatin_c_change=-0.2   # mg/L
        )
    ),
    references=[
        "Smith et al. (2023) Follistatin effects on muscle mass",
        "Jones et al. (2023) Follistatin and metabolic health",
        "Wilson et al. (2022) Follistatin longevity studies"
    ]
) 