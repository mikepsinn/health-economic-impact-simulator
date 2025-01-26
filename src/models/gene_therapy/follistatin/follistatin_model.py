"""
Follistatin gene therapy impact model.

This module implements models for analyzing the impact of Follistatin therapy
showing 2 lb muscle gain and 2 lb fat reduction across US population.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from src.models.base_model import BaseImpactModel, BaseParameters

class FollistatinParameters(BaseModel):
    """Parameters for Follistatin therapy impact model."""
    muscle_gain_lbs: float = Field(default=2.0, description="Average muscle mass gain in pounds")
    fat_loss_lbs: float = Field(default=2.0, description="Average fat mass reduction in pounds")
    obesity_cost_per_lb: float = Field(default=92.0, description="Healthcare cost per pound of excess fat")
    productivity_per_lb_muscle: float = Field(default=147.0, description="Productivity value per pound of muscle")
    medicare_savings_per_lb: float = Field(default=100.0, description="Medicare savings per pound of improved body composition")

class FollistatinModel(BaseImpactModel):
    """Analyzes economic impact of Follistatin gene therapy."""
    
    def __init__(self, base_params: BaseParameters = None, therapy_params: FollistatinParameters = None):
        super().__init__(base_params)
        self.therapy_params = therapy_params or FollistatinParameters()
    
    def calculate_impacts(self) -> Dict[str, float]:
        """Calculate economic impacts of therapy."""
        # Calculate healthcare cost reduction from fat loss
        healthcare_savings = (
            self.therapy_params.fat_loss_lbs * 
            self.therapy_params.obesity_cost_per_lb * 
            1_000_000  # Scale to population level
        )
        
        # Calculate productivity gains from muscle increase
        productivity_value = (
            self.therapy_params.muscle_gain_lbs * 
            self.therapy_params.productivity_per_lb_muscle * 
            1_000_000  # Scale to population level
        )
        
        # Calculate Medicare savings
        medicare_savings = (
            (self.therapy_params.muscle_gain_lbs + self.therapy_params.fat_loss_lbs) *
            self.therapy_params.medicare_savings_per_lb *
            1_000_000  # Scale to population level
        )
        
        return {
            "healthcare_savings": healthcare_savings,
            "productivity_value": productivity_value,
            "medicare_savings": medicare_savings,
            "parameters": {
                "muscle_gain_lbs": self.therapy_params.muscle_gain_lbs,
                "fat_loss_lbs": self.therapy_params.fat_loss_lbs,
                "obesity_cost_per_lb": self.therapy_params.obesity_cost_per_lb,
                "productivity_per_lb_muscle": self.therapy_params.productivity_per_lb_muscle,
                "medicare_savings_per_lb": self.therapy_params.medicare_savings_per_lb
            }
        } 