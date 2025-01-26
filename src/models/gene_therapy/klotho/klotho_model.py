"""
Klotho gene therapy impact model.

This module implements models for analyzing the impact of Klotho therapy showing:
1. Cognitive function improvements (2-5 IQ points)
2. Alzheimer's progression delay (2 years)
3. Kidney disease progression delay (2 years)

See questions.md for full requirements.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from src.models.base_model import BaseImpactModel, BaseParameters

class KlothoParameters(BaseModel):
    """Parameters specific to Klotho therapy."""
    iq_increase: float = Field(default=3.5, description="IQ point increase (2-5 range)")
    alzheimers_delay_years: float = Field(default=2.0, description="Alzheimer's progression delay in years")
    kidney_delay_years: float = Field(default=2.0, description="Kidney disease progression delay in years")
    alzheimers_annual_cost: float = Field(default=355e9, description="Total US annual Alzheimer's cost")
    esrd_annual_cost: float = Field(default=87e9, description="Total US annual ESRD cost")
    cognitive_value_per_iq: float = Field(default=2200, description="Annual economic value per IQ point")

class KlothoModel(BaseImpactModel):
    """Models the health and economic impacts of Klotho gene therapy."""
    
    def __init__(self, base_params: BaseParameters = None, therapy_params: KlothoParameters = None):
        super().__init__(base_params)
        self.therapy_params = therapy_params or KlothoParameters()
    
    def calculate_cognitive_value(self) -> float:
        """Calculate economic value of cognitive improvement."""
        annual_value = (
            self.params.adult_population *
            self.therapy_params.iq_increase *
            self.therapy_params.cognitive_value_per_iq
        )
        return self.calculate_npv(annual_value, self.params.time_horizon_years)
    
    def calculate_dementia_savings(self) -> float:
        """Calculate reduction in dementia care costs."""
        delay_impact = self.therapy_params.alzheimers_delay_years / 10  # Assume 10-year progression
        annual_savings = self.therapy_params.alzheimers_annual_cost * delay_impact
        return self.calculate_npv(annual_savings, self.params.time_horizon_years)
    
    def calculate_kidney_savings(self) -> float:
        """Calculate Medicare savings from delayed ESRD."""
        delay_impact = self.therapy_params.kidney_delay_years / 5  # Assume 5-year progression
        annual_savings = self.therapy_params.esrd_annual_cost * delay_impact
        return self.calculate_npv(annual_savings, self.params.time_horizon_years)
    
    def calculate_impacts(self) -> Dict[str, Any]:
        """Calculate all health and economic impacts."""
        return {
            "cognitive_value": self.calculate_cognitive_value(),
            "dementia_savings": self.calculate_dementia_savings(),
            "kidney_savings": self.calculate_kidney_savings(),
            "parameters": {
                "iq_increase": self.therapy_params.iq_increase,
                "alzheimers_delay": self.therapy_params.alzheimers_delay_years,
                "kidney_delay": self.therapy_params.kidney_delay_years,
                "time_horizon": self.params.time_horizon_years
            }
        } 