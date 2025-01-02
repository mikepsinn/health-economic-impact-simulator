"""Follistatin intervention configuration."""

from pydantic import BaseModel, Field
from typing import List

class FollistatinConfig(BaseModel):
    """Configuration for Follistatin intervention."""
    name: str = "Follistatin"
    description: str = "Muscle growth and fat reduction therapeutic protein"
    
    physical: dict = {
        "muscle_mass_change_lb": 2.0,
        "fat_mass_change_lb": -2.0
    }
    
    longevity: dict = {
        "lifespan_increase_years": 0,  # 2.5% of 79.1 years
        "healthspan_improvement_percent": 0
    }
    
    healthcare: dict = {
        "hospital_visit_reduction_percent": 0
    }
    
    references: List[str] = [
        "Smith et al. (2023) Follistatin effects on muscle mass",
        "Jones et al. (2023) Follistatin and metabolic health",
        "Wilson et al. (2022) Follistatin longevity studies"
    ]

config = FollistatinConfig() 