"""
Model sensitivity analysis module.

This module provides tools for analyzing model sensitivity and complexity:
1. Parameter sensitivity analysis
2. Model complexity assessment
3. Validation frameworks
"""

from typing import Dict, Any, List, Callable
from inspect import signature
from dataclasses import dataclass

@dataclass
class SensitivityResult:
    """Result of sensitivity analysis for a single parameter."""
    parameter: str
    base_value: float
    low_value: float
    high_value: float
    base_output: float
    low_output: float
    high_output: float
    
    @property
    def sensitivity_score(self) -> float:
        """Calculate sensitivity score."""
        param_range = self.high_value - self.low_value
        output_range = self.high_output - self.low_output
        if param_range == 0:
            return 0
        return (output_range / self.base_output) / (param_range / self.base_value)

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
        
    def analyze_parameter_sensitivity(self, model: Any) -> List[SensitivityResult]:
        """Analyze sensitivity to parameter variations."""
        results = []
        base_output = sum(v for k,v in model.calculate_impacts().items() if isinstance(v, (int, float)) and k != "parameters")
        
        # Get parameters from model's therapy_params
        params = model.therapy_params.dict()
        
        for param, base_val in params.items():
            # Skip if we don't have a range for this parameter
            if param not in self.parameter_ranges:
                continue
            
            min_val, max_val = self.parameter_ranges[param]
            
            # Create copies of parameters for low and high values
            low_params = params.copy()
            low_params[param] = min_val
            
            high_params = params.copy()
            high_params[param] = max_val
            
            # Create new parameter objects and update model
            param_class = model.therapy_params.__class__
            
            # Save original params
            original_params = model.therapy_params
            
            try:
                # Test low value
                model.therapy_params = param_class(**low_params)
                low_output = sum(v for k,v in model.calculate_impacts().items() if isinstance(v, (int, float)) and k != "parameters")
                
                # Test high value
                model.therapy_params = param_class(**high_params)
                high_output = sum(v for k,v in model.calculate_impacts().items() if isinstance(v, (int, float)) and k != "parameters")
                
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
            finally:
                # Restore original params
                model.therapy_params = original_params
                
        return results
    
    def analyze_model(self, model: Any) -> Dict[str, Any]:
        """Analyze sensitivity of a model."""
        results = self.analyze_parameter_sensitivity(model)
        
        # Convert to dict for reporting
        return {
            "sensitivity_scores": {
                r.parameter: r.sensitivity_score for r in results
            },
            "parameter_impacts": [
                vars(r) for r in results
            ],
            "parameters": {
                "simulation_runs": 1000,  # Default value
                "confidence_level": 0.95  # Default value
            }
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