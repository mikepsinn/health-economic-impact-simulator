"""
Model sensitivity analysis module.

This module provides tools for analyzing model sensitivity and complexity:
1. Parameter sensitivity analysis
2. Model complexity assessment
3. Validation frameworks
"""

from typing import Dict, Any, List, Callable
from pydantic import BaseModel, Field
import numpy as np
from dataclasses import dataclass

@dataclass
class SensitivityResult:
    """Result of a sensitivity analysis for a parameter."""
    parameter: str
    base_value: float
    range: tuple
    impact: float
    relative_importance: float

class SensitivityParameters(BaseModel):
    """Parameters for sensitivity analysis."""
    parameter_ranges: Dict[str, tuple] = Field(
        default={
            "discount_rate": (0.01, 0.05),
            "time_horizon_years": (5, 15),
            "medicare_per_capita": (10000, 15000),
            "gdp_per_capita": (55000, 75000)
        },
        description="Parameter ranges for sensitivity analysis"
    )
    simulation_runs: int = Field(default=1000, description="Number of Monte Carlo simulations")
    confidence_level: float = Field(default=0.95, description="Confidence level for intervals")

class ModelSensitivityAnalyzer:
    """Analyzes model sensitivity and complexity."""
    
    def __init__(self, params: SensitivityParameters = None):
        self.params = params or SensitivityParameters()
    
    def analyze_parameter_sensitivity(self, model_func: Callable) -> List[SensitivityResult]:
        """Analyze sensitivity to parameter variations."""
        results = []
        base_output = model_func()  # Get baseline output
        
        for param, (min_val, max_val) in self.params.parameter_ranges.items():
            # Calculate impact of parameter variation
            delta = max_val - min_val
            base_val = (max_val + min_val) / 2
            
            # Simple one-at-a-time sensitivity analysis
            high_output = model_func(**{param: max_val})
            low_output = model_func(**{param: min_val})
            impact = (high_output - low_output) / base_output
            
            results.append(SensitivityResult(
                parameter=param,
                base_value=base_val,
                range=(min_val, max_val),
                impact=impact,
                relative_importance=abs(impact)
            ))
        
        # Sort by relative importance
        results.sort(key=lambda x: x.relative_importance, reverse=True)
        return results
    
    def assess_model_complexity(self) -> Dict[str, Any]:
        """Assess current model complexity and recommendations."""
        return {
            "minimum_viable_components": [
                "Basic population parameters",
                "Core economic calculations",
                "Primary health impacts"
            ],
            "complexity_levels": {
                "current": "medium",
                "recommended_next": "high",
                "rationale": "Need more granular age stratification"
            },
            "priority_additions": [
                "Age-specific impact modeling",
                "Regional variation analysis",
                "Comorbidity interactions"
            ]
        }
    
    def create_validation_framework(self) -> Dict[str, Any]:
        """Define validation framework for the model."""
        return {
            "validation_metrics": [
                "Parameter stability",
                "Output consistency",
                "Literature alignment",
                "Expert review feedback"
            ],
            "data_requirements": {
                "clinical_trials": "Minimum 1000 participants",
                "followup_duration": "5+ years",
                "biomarker_data": "Quarterly measurements"
            },
            "stakeholder_validation": [
                "Clinical experts",
                "Health economists",
                "Medicare officials",
                "Industry partners"
            ]
        }
    
    def analyze_model(self, model_func: Callable) -> Dict[str, Any]:
        """Perform comprehensive model analysis."""
        return {
            "parameter_sensitivity": [
                vars(r) for r in self.analyze_parameter_sensitivity(model_func)
            ],
            "complexity_assessment": self.assess_model_complexity(),
            "validation_framework": self.create_validation_framework(),
            "parameters": {
                "simulation_runs": self.params.simulation_runs,
                "confidence_level": self.params.confidence_level
            }
        } 