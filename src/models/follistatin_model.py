#!/usr/bin/env python3
"""
Follistatin Gene Therapy Impact Model
-------------------------------------
Economic impact model for follistatin gene therapy intervention.
"""

from dataclasses import dataclass
from typing import Dict, Tuple, List

from src.models.base_model import BaseImpactModel, BasePopulationParams, BaseEconomicParams

@dataclass
class FollistatinParams:
    """Parameters specific to follistatin intervention."""
    muscle_gain_lb: float
    fat_loss_lb: float
    lifespan_increase_years: float
    healthspan_improvement_percent: float
    savings_per_lb: float  # Healthcare savings per pound of improvement

class FollistatinImpactModel(BaseImpactModel):
    """Economic impact model for follistatin gene therapy."""
    
    def __init__(
        self,
        population_params: BasePopulationParams,
        economic_params: BaseEconomicParams,
        intervention_params: FollistatinParams
    ):
        super().__init__(population_params, economic_params, intervention_params)

    def calculate_healthcare_savings(self) -> float:
        """Calculate healthcare savings from body composition changes."""
        total_improvement_lb = (
            self.intervention.muscle_gain_lb + 
            self.intervention.fat_loss_lb
        )
        return (
            self.pop.target_population * 
            total_improvement_lb * 
            self.intervention.savings_per_lb
        )

    def calculate_gdp_impact(self) -> float:
        """Calculate GDP impact from increased lifespan."""
        if not self.pop.workforce_fraction:
            raise ValueError("Workforce fraction required for GDP calculations")
            
        basic_impact = (
            self.pop.target_population *
            self.pop.workforce_fraction *
            self.intervention.lifespan_increase_years *
            self.econ.annual_productivity
        )
        
        return self.apply_discount_rate(
            basic_impact, 
            self.intervention.lifespan_increase_years
        )

    def calculate_medicare_impact(self) -> float:
        """Calculate Medicare savings from improved healthspan."""
        if not self.pop.medicare_beneficiaries:
            raise ValueError("Medicare beneficiaries required for Medicare calculations")
            
        return (
            self.pop.medicare_beneficiaries *
            self.econ.annual_healthcare_cost *
            (self.intervention.healthspan_improvement_percent / 100.0)
        )

    def validate_assumptions(self) -> bool:
        """Validate model assumptions."""
        validations = [
            0 <= self.intervention.muscle_gain_lb <= 10,  # Reasonable muscle gain
            0 <= self.intervention.fat_loss_lb <= 10,     # Reasonable fat loss
            0 <= self.intervention.lifespan_increase_years <= 5,  # Reasonable lifespan increase
            0 <= self.intervention.healthspan_improvement_percent <= 20,  # Reasonable health improvement
            self.intervention.savings_per_lb > 0,
            self.pop.target_population <= self.pop.total_population
        ]
        return all(validations)

    def get_param_ranges(self) -> Dict[str, List[float]]:
        """Get parameter ranges for sensitivity analysis."""
        return {
            'muscle_gain_lb': [1.0, 2.0, 3.0],
            'fat_loss_lb': [1.0, 2.0, 3.0],
            'lifespan_increase_years': [1.0, 1.925, 3.0],
            'healthspan_improvement_percent': [2.5, 5.0, 7.5],
            'savings_per_lb': [5.0, 10.0, 15.0]
        }

    def get_current_params(self) -> Dict[str, float]:
        """Get current parameter values as dictionary."""
        return {
            'muscle_gain_lb': self.intervention.muscle_gain_lb,
            'fat_loss_lb': self.intervention.fat_loss_lb,
            'lifespan_increase_years': self.intervention.lifespan_increase_years,
            'healthspan_improvement_percent': self.intervention.healthspan_improvement_percent,
            'savings_per_lb': self.intervention.savings_per_lb
        }

    def calculate_impacts_for_params(self, params: Dict[str, float]) -> Dict[str, float]:
        """Calculate impacts for a given set of parameters."""
        # Store original values
        orig_values = self.get_current_params()
        
        # Update parameters
        for param, value in params.items():
            setattr(self.intervention, param, value)
        
        # Calculate impacts
        impacts = {
            'healthcare_savings': self.calculate_healthcare_savings(),
            'gdp_impact': self.calculate_gdp_impact(),
            'medicare_savings': self.calculate_medicare_impact()
        }
        
        # Restore original values
        for param, value in orig_values.items():
            setattr(self.intervention, param, value)
        
        return impacts


def main():
    """Example usage of the model."""
    
    # Initialize parameters
    pop_params = BasePopulationParams(
        total_population=332_000_000,
        target_population=332_000_000,  # Assuming universal treatment
        medicare_beneficiaries=64_000_000,
        workforce_fraction=0.5
    )
    
    econ_params = BaseEconomicParams(
        annual_healthcare_cost=14_000,  # Average Medicare cost per beneficiary
        annual_productivity=70_000,     # Average annual productivity per worker
        discount_rate=0.03             # 3% annual discount rate
    )
    
    intervention_params = FollistatinParams(
        muscle_gain_lb=2.0,
        fat_loss_lb=2.0,
        lifespan_increase_years=1.925,  # 2.5% of 77 years
        healthspan_improvement_percent=5.0,
        savings_per_lb=10.0
    )
    
    # Create and validate model
    model = FollistatinImpactModel(pop_params, econ_params, intervention_params)
    if not model.validate_assumptions():
        raise ValueError("Invalid model assumptions")
    
    # Generate and print report
    report = model.generate_full_report()
    
    print("\n=== Follistatin Gene Therapy Impact Model Results ===\n")
    print(f"Annual Healthcare Savings: ${report['annual_healthcare_savings_billions']:.2f} billion")
    print(f"GDP Impact (Discounted): ${report['gdp_impact_trillions']:.2f} trillion")
    print(f"Annual Medicare Savings: ${report['annual_medicare_impact_billions']:.2f} billion\n")
    
    # Optional: Run sensitivity analysis
    sensitivity = model.sensitivity_analysis()
    print("=== Sensitivity Analysis ===")
    for param, results in sensitivity.items():
        print(f"\nImpact of varying {param}:")
        for factor, values in results.items():
            print(f"  {factor}: Healthcare savings = ${values['annual_healthcare_savings_billions']:.2f}B")


if __name__ == "__main__":
    main() 