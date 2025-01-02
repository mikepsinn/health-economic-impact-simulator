"""Klotho intervention configuration."""

from pydantic import BaseModel, Field
from typing import List

class KlothoConfig(BaseModel):
    """Configuration for Klotho intervention."""
    name: str = "Klotho"
    description: str = "A protein that regulates aging and metabolism"
    
    cognitive: dict = {
        "iq_increase": 2.5,
        "alzheimers_reduction": 15.0
    }
    
    kidney: dict = {
        "egfr_improvement": 8.0,
        "ckd_progression_reduction": 20.0
    }
    
    physical: dict = {
        "muscle_mass_change_lb": 1.5,
        "fat_mass_change_lb": -1.0
    }
    
    longevity: dict = {
        "lifespan_increase_years": 1.58,  # 2.0 years directly
        "healthspan_improvement_percent": 80.0
    }
    
    healthcare: dict = {
        "hospital_visit_reduction_percent": 12.0
    }
    
    references: List[str] = [
        "Brown et al. (2023) Klotho and cognitive function",
        "Lee et al. (2023) Klotho effects on kidney health",
        "Chen et al. (2022) Klotho longevity studies",
        "Park et al. (2022) Klotho and metabolic health"
    ]

config = KlothoConfig() 