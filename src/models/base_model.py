#!/usr/bin/env python3
"""
Base Economic Impact Model
-------------------------
Template for creating intervention-specific economic impact models.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
import pandas as pd

from ..utils.stratification import AgeStratification
from ..utils.monte_carlo import run_monte_carlo, calculate_confidence_intervals
from ..utils.visualization import (
    plot_sensitivity_analysis,
    plot_monte_carlo_results,
    plot_time_series
)

@dataclass
class BasePopulationParams:
    """Base population parameters that all models should use."""
    total_population: int
    target_population: int
    medicare_beneficiaries: Optional[int] = None
    workforce_fraction: Optional[float] = None
    age_stratification: Optional[AgeStratification] = None

    def __post_init__(self):
        if self.age_stratification is None:
            self.age_stratification = AgeStratification.default()

@dataclass
class BaseEconomicParams:
    """Base economic parameters that all models should use."""
    annual_healthcare_cost: float
    annual_productivity: float
    discount_rate: float = 0.03  # Default 3% discount rate

class BaseImpactModel(ABC):
    """Abstract base class for all intervention impact models."""
    
    def __init__(
        self,
        population_params: BasePopulationParams,
        economic_params: BaseEconomicParams,
        intervention_params: Any  # Specific to each intervention
    ):
        self.pop = population_params
        self.econ = economic_params
        self.intervention = intervention_params

    @abstractmethod
    def calculate_healthcare_savings(self) -> float:
        """Calculate annual healthcare savings from the intervention."""
        pass

    @abstractmethod
    def calculate_gdp_impact(self) -> float:
        """Calculate GDP impact from the intervention."""
        pass

    @abstractmethod
    def calculate_medicare_impact(self) -> float:
        """Calculate Medicare spending impact."""
        pass

    def apply_discount_rate(self, value: float, years: float) -> float:
        """Apply time value of money discount to a future value."""
        return value * (1 / (1 + self.econ.discount_rate) ** years)

    def generate_full_report(self) -> Dict[str, float]:
        """Generate a standardized report of all economic impacts."""
        healthcare_savings = self.calculate_healthcare_savings()
        gdp_impact = self.calculate_gdp_impact()
        medicare_impact = self.calculate_medicare_impact()
        
        return {
            "annual_healthcare_savings_billions": healthcare_savings / 1e9,
            "gdp_impact_trillions": gdp_impact / 1e12,
            "annual_medicare_impact_billions": medicare_impact / 1e9
        }

    @abstractmethod
    def get_param_ranges(self) -> Dict[str, List[float]]:
        """Get parameter ranges for sensitivity analysis."""
        pass

    def run_sensitivity_analysis(self) -> Dict[str, Dict[str, float]]:
        """Run sensitivity analysis on key parameters."""
        param_ranges = self.get_param_ranges()
        baseline_values = self.get_current_params()
        
        return plot_sensitivity_analysis(
            param_ranges,
            baseline_values,
            self.calculate_impacts_for_params
        )

    def run_monte_carlo(
        self,
        param_variations: Dict[str, float],
        n_simulations: int = 1000
    ) -> Dict[str, pd.DataFrame]:
        """Run Monte Carlo simulation."""
        base_params = self.get_current_params()
        
        results = run_monte_carlo(
            base_params,
            param_variations,
            self.calculate_impacts_for_params,
            n_simulations
        )
        
        confidence_intervals = calculate_confidence_intervals(results)
        return results, confidence_intervals

    @abstractmethod
    def get_current_params(self) -> Dict[str, float]:
        """Get current parameter values as dictionary."""
        pass

    @abstractmethod
    def calculate_impacts_for_params(self, params: Dict[str, float]) -> Dict[str, float]:
        """Calculate impacts for a given set of parameters."""
        pass

    @abstractmethod
    def validate_assumptions(self) -> bool:
        """Validate that all model assumptions are reasonable."""
        pass 