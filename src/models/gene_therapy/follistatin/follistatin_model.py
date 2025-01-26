"""
Follistatin gene therapy impact model.

This module implements models for analyzing the impact of Follistatin therapy
showing 2 lb muscle gain and 2 lb fat reduction across US population.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from src.models.base_model import BaseImpactModel, BaseParameters

class FollistatinParameters(BaseModel):
    """Parameters specific to Follistatin therapy."""
    muscle_gain_lbs: float = Field(default=2.0, description="Muscle mass gain in pounds")
    fat_reduction_lbs: float = Field(default=2.0, description="Fat mass reduction in pounds")
    obesity_cost_per_lb: float = Field(default=150.0, description="Annual healthcare cost per pound of excess fat")
    productivity_per_muscle_lb: float = Field(default=0.001, description="Productivity increase per pound of muscle")
    comorbidity_reduction: float = Field(default=0.05, description="Reduction in obesity-related comorbidities")

class FollistatinModel(BaseImpactModel):
    """Models the health and economic impacts of Follistatin gene therapy."""
    
    def __init__(self, base_params: BaseParameters = None, therapy_params: FollistatinParameters = None):
        super().__init__(base_params)
        self.therapy_params = therapy_params or FollistatinParameters()
    
    def calculate_obesity_cost_reduction(self) -> float:
        """Calculate reduction in obesity-related healthcare costs."""
        annual_savings = (
            self.params.adult_population *
            self.therapy_params.fat_reduction_lbs *
            self.therapy_params.obesity_cost_per_lb
        )
        return self.calculate_npv(annual_savings, self.params.time_horizon_years)
    
    def calculate_productivity_impact(self) -> float:
        """Calculate workforce productivity improvement."""
        return self.calculate_gdp_impact(
            self.therapy_params.muscle_gain_lbs *
            self.therapy_params.productivity_per_muscle_lb
        )
    
    def calculate_medicare_impact(self) -> float:
        """Calculate Medicare savings from reduced comorbidities."""
        return self.calculate_medicare_savings(self.therapy_params.comorbidity_reduction)
    
    def calculate_impacts(self) -> Dict[str, Any]:
        """Calculate all health and economic impacts."""
        return {
            "obesity_cost_reduction": self.calculate_obesity_cost_reduction(),
            "productivity_impact": self.calculate_productivity_impact(),
            "medicare_savings": self.calculate_medicare_impact(),
            "parameters": {
                "muscle_gain": self.therapy_params.muscle_gain_lbs,
                "fat_reduction": self.therapy_params.fat_reduction_lbs,
                "time_horizon": self.params.time_horizon_years
            }
        } 