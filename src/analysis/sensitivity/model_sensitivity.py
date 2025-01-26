"""
Model sensitivity analysis module.

This module provides tools for analyzing model sensitivity and complexity:
1. Parameter sensitivity analysis
2. Model complexity assessment
3. Validation frameworks
"""

from typing import Dict, Any, List, Callable, Tuple
from pydantic import BaseModel, Field
import numpy as np
from dataclasses import dataclass
from inspect import signature

@dataclass
class SensitivityResult:
    """Result of sensitivity analysis for a parameter."""
    parameter: str
    base_value: float
    low_value: float
    high_value: float
    base_output: Dict[str, float]
    low_output: Dict[str, float]
    high_output: Dict[str, float]
    
    @property
    def sensitivity_score(self) -> float:
        """Calculate sensitivity score."""
        # Use first numeric output as sensitivity metric
        metric = next(k for k,v in self.base_output.items() if isinstance(v, (int, float)))
        base = self.base_output[metric]
        low = self.low_output[metric]
        high = self.high_output[metric]
        
        param_range = self.high_value - self.low_value
        output_range = high - low
        
        if abs(base) < 1e-10 or abs(param_range) < 1e-10:
            return 0
            
        return (output_range / base) / (param_range / self.base_value)

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
    """Analyzes model sensitivity to parameter variations."""
    
    def __init__(self):
        """Initialize analyzer with default parameter ranges."""
        self.parameter_ranges = {
            # Economic parameters
            "discount_rate": (0.02, 0.07),
            "qaly_value": (50000, 150000),
            
            # Follistatin parameters
            "muscle_gain_lbs": (1.0, 3.0),
            "fat_loss_lbs": (1.0, 3.0),
            
            # Klotho parameters  
            "iq_increase": (2.0, 5.0),
            "alzheimers_delay_years": (1.0, 3.0),
            
            # Lifespan parameters
            "lifespan_increase_pct": (1.5, 3.5),
            "health_quality_factor": (0.7, 0.9)
        }
        
    def analyze_parameter_sensitivity(self, model_func: Callable) -> List[SensitivityResult]:
        """Analyze sensitivity to parameter variations."""
        results = []
        base_output = model_func()  # Get baseline output
        
        # Get the parameters accepted by this model
        valid_params = signature(model_func).parameters.keys()
        
        for param, (min_val, max_val) in self.parameter_ranges.items():
            # Skip parameters not used by this model
            if param not in valid_params:
                continue
                
            # Calculate impact of parameter variation
            delta = max_val - min_val
            base_val = (max_val + min_val) / 2
            
            # Simple one-at-a-time sensitivity analysis
            try:
                high_output = model_func(**{param: max_val})
                low_output = model_func(**{param: min_val})
                
                results.append(SensitivityResult(
                    parameter=param,
                    base_value=base_val,
                    low_value=min_val,
                    high_value=max_val,
                    base_output=base_output,
                    low_output=low_output,
                    high_output=high_output
                ))
            except Exception as e:
                print(f"Warning: Could not analyze sensitivity for {param}: {str(e)}")
                continue
                
        return results
        
    def analyze_model(self, model_func: Callable) -> Dict[str, Any]:
        """Analyze sensitivity of a model."""
        results = self.analyze_parameter_sensitivity(model_func)
        
        # Convert to dict for reporting
        return {
            "sensitivity_scores": {
                r.parameter: r.sensitivity_score for r in results
            },
            "parameter_impacts": [
                vars(r) for r in results
            ]
        }
    
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