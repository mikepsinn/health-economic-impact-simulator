"""
Lifespan extension impact model.

This module implements models for analyzing the economic impact of 
2.5% lifespan extension, including GDP impacts and Medicare savings.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from src.models.base_model import BaseImpactModel, BaseParameters

class LifespanParameters(BaseModel):
    """Parameters specific to lifespan extension therapy."""
    lifespan_increase_pct: float = Field(default=2.5, description="Percentage increase in lifespan")
    workforce_participation_rate: float = Field(default=0.63, description="Workforce participation rate")
    age_related_care_pct: float = Field(default=0.85, description="Percentage of Medicare spent on age-related care")
    qaly_value: float = Field(default=100000, description="Value of one quality-adjusted life year")
    health_quality_factor: float = Field(default=0.8, description="Health quality factor for extended years")

class LifespanModel(BaseImpactModel):
    """Models the economic impacts of lifespan extension therapy."""
    
    def __init__(self, base_params: BaseParameters = None, therapy_params: LifespanParameters = None):
        super().__init__(base_params)
        self.therapy_params = therapy_params or LifespanParameters()
    
    def calculate_workforce_gdp(self) -> float:
        """Calculate GDP increase from extended workforce participation."""
        extension_impact = self.therapy_params.lifespan_increase_pct / 100
        working_population = (
            self.params.adult_population * 
            self.therapy_params.workforce_participation_rate
        )
        return self.calculate_gdp_impact(extension_impact)
    
    def calculate_medicare_delay_savings(self) -> float:
        """Calculate Medicare savings from delayed age-related care."""
        care_delay = self.therapy_params.lifespan_increase_pct / 100
        age_related_spending = (
            self.params.medicare_per_capita * 
            self.therapy_params.age_related_care_pct
        )
        return self.calculate_medicare_savings(care_delay)
    
    def calculate_qaly_value(self) -> float:
        """Calculate economic value of additional healthy years."""
        extension_years = 79.1 * (self.therapy_params.lifespan_increase_pct / 100)  # 79.1 is average lifespan
        annual_value = (
            self.params.adult_population *
            extension_years *
            self.therapy_params.qaly_value *
            self.therapy_params.health_quality_factor
        ) / self.params.time_horizon_years
        return self.calculate_npv(annual_value, self.params.time_horizon_years)
    
    def calculate_impacts(self) -> Dict[str, Any]:
        """Calculate all economic impacts."""
        return {
            "gdp_increase": self.calculate_workforce_gdp(),
            "medicare_savings": self.calculate_medicare_delay_savings(),
            "qaly_value": self.calculate_qaly_value(),
            "parameters": {
                "lifespan_increase": self.therapy_params.lifespan_increase_pct,
                "health_quality": self.therapy_params.health_quality_factor,
                "time_horizon": self.params.time_horizon_years
            }
        } 