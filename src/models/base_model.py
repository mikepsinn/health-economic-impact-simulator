#!/usr/bin/env python3
"""
Base Economic Impact Model
-------------------------
Template for creating intervention-specific economic impact models.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import numpy as np

from src.utils.stratification import AgeStratification
from src.utils.monte_carlo import run_monte_carlo, calculate_confidence_intervals
from src.utils.visualization import (
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
        if self.medicare_beneficiaries is None:
            self.medicare_beneficiaries = int(self.total_population * 0.186)  # Default Medicare enrollment rate
        if self.workforce_fraction is None:
            self.workforce_fraction = 0.5  # Default workforce participation
        if self.age_stratification is None:
            self.age_stratification = AgeStratification.default()

@dataclass
class BaseEconomicParams:
    """Base economic parameters that all models should use."""
    annual_healthcare_cost: float
    annual_productivity: float
    discount_rate: float = 0.03  # Default 3% discount rate

@dataclass
class BaseInterventionParams:
    """Base parameters for intervention effects."""
    muscle_mass_change_lb: float  # Positive = gain, negative = loss
    fat_mass_change_lb: float    # Positive = gain, negative = loss
    lifespan_increase_years: float
    healthspan_improvement_percent: float
    savings_per_lb: float = 10.0  # Default $10 savings per pound improvement
    hospital_visit_reduction_percent: float = 15.0  # Default 15% reduction
    cost_per_hospital_visit: float = 12000.0  # Default $12,000 per visit

    def __post_init__(self):
        """Validate parameter values."""
        if self.muscle_mass_change_lb < -10 or self.muscle_mass_change_lb > 10:
            raise ValueError("Muscle mass change must be between -10 and +10 lbs")
        if self.fat_mass_change_lb < -30 or self.fat_mass_change_lb > 10:
            raise ValueError("Fat mass change must be between -30 and +10 lbs")
        if self.lifespan_increase_years < 0:
            raise ValueError("Lifespan increase must be positive")
        if self.healthspan_improvement_percent < 0 or self.healthspan_improvement_percent > 100:
            raise ValueError("Health improvement must be between 0 and 100 percent")

    @classmethod
    def from_config(cls, config: Dict[str, Any], base_params: Dict[str, Any]) -> 'BaseInterventionParams':
        """Create parameters from configuration."""
        effects = config['default_effects']
        modifiers = config['impact_modifiers']
        
        return cls(
            muscle_mass_change_lb=effects['physical']['muscle_mass_change'],
            fat_mass_change_lb=effects['physical']['fat_mass_change'],
            lifespan_increase_years=base_params['health_baselines']['average_lifespan'] * 
                                  (effects['longevity']['lifespan_increase'] / 100.0),
            healthspan_improvement_percent=modifiers['health_quality'] * 100,
            savings_per_lb=10.0,  # Could be added to config
            hospital_visit_reduction_percent=effects['healthcare']['hospital_visit_reduction'],
            cost_per_hospital_visit=12000.0  # Could be added to config
        )

class BaseImpactModel(ABC):
    """Base class for all intervention impact models."""
    
    def __init__(
        self,
        population_params: BasePopulationParams,
        economic_params: BaseEconomicParams,
        intervention_params: BaseInterventionParams
    ):
        self.pop = population_params
        self.econ = economic_params
        self.intervention = intervention_params

    def calculate_healthcare_savings(self) -> float:
        """
        Calculate annual healthcare savings from the intervention.
        
        Returns:
            float: Annual healthcare savings in dollars
        
        Formula:
            savings = target_population * (muscle_mass_change + fat_mass_change) * savings_per_lb +
                     target_population * baseline_hospital_visits * hospital_reduction * cost_per_visit
        """
        # Savings from body composition changes
        composition_savings = (
            self.pop.target_population * 
            (self.intervention.muscle_mass_change_lb + self.intervention.fat_mass_change_lb) * 
            self.intervention.savings_per_lb
        )
        
        # Additional savings from reduced hospital visits
        baseline_visits = self.pop.target_population * 0.125  # Average visits per person per year
        visit_reduction = baseline_visits * (self.intervention.hospital_visit_reduction_percent / 100.0)
        hospital_savings = visit_reduction * self.intervention.cost_per_hospital_visit
        
        return composition_savings + hospital_savings

    def calculate_gdp_impact(self) -> float:
        """
        Calculate GDP impact from the intervention.
        
        Returns:
            float: Total GDP impact in dollars
        
        Formula:
            impact = population * workforce_fraction * lifespan_increase * 
                    annual_productivity * lifespan_to_gdp * discount_factor
        """
        working_years = (
            self.intervention.lifespan_increase_years * 
            self.pop.workforce_fraction
        )
        
        annual_impact = (
            self.pop.target_population * 
            working_years * 
            self.econ.annual_productivity
        )
        
        # Apply discount rate over average period
        return self.apply_discount_rate(annual_impact, working_years / 2)

    def calculate_medicare_impact(self) -> float:
        """
        Calculate Medicare spending impact.
        
        Returns:
            float: Annual Medicare savings in dollars
        
        Formula:
            savings = beneficiaries * annual_cost * 
                     (health_quality + biomarker_impact)
        """
        health_improvement = self.intervention.healthspan_improvement_percent / 100.0
        
        return (
            self.pop.medicare_beneficiaries * 
            self.econ.annual_healthcare_cost * 
            health_improvement
        )

    def calculate_qalys(self) -> float:
        """
        Calculate Quality Adjusted Life Years gained.
        
        Returns:
            float: Total QALYs gained across population
        
        Formula:
            qalys = population * lifespan_increase * (1 + quality_improvement)
        """
        base_qaly = self.intervention.lifespan_increase_years
        quality_improvement = self.intervention.healthspan_improvement_percent / 100.0
        return self.pop.target_population * (base_qaly * (1 + quality_improvement))

    def apply_discount_rate(self, value: float, years: float) -> float:
        """Apply time value of money discount to a future value."""
        return value * (1 / (1 + self.econ.discount_rate) ** years)

    def generate_full_report(self) -> Dict[str, float]:
        """Generate a standardized report of all economic impacts."""
        healthcare_savings = self.calculate_healthcare_savings()
        gdp_impact = self.calculate_gdp_impact()
        medicare_impact = self.calculate_medicare_impact()
        qalys = self.calculate_qalys()
        
        return {
            "annual_healthcare_savings_billions": healthcare_savings / 1e9,
            "gdp_impact_trillions": gdp_impact / 1e12,
            "annual_medicare_impact_billions": medicare_impact / 1e9,
            "qalys_gained": qalys
        }

    def get_param_ranges(self) -> Dict[str, List[float]]:
        """
        Get parameter ranges for sensitivity analysis.
        
        Returns:
            Dict mapping parameter names to [min, max, step] lists
        """
        return {
            'muscle_mass_change_lb': [0.0, 5.0, 0.5],
            'fat_mass_change_lb': [0.0, 5.0, 0.5],
            'lifespan_increase_years': [0.0, 3.0, 0.1],
            'healthspan_improvement_percent': [0.0, 10.0, 1.0],
            'hospital_visit_reduction_percent': [0.0, 30.0, 5.0]
        }

    def get_current_params(self) -> Dict[str, float]:
        """
        Get current parameter values as dictionary.
        
        Returns:
            Dict mapping parameter names to their current values
        """
        return {
            'muscle_mass_change_lb': self.intervention.muscle_mass_change_lb,
            'fat_mass_change_lb': self.intervention.fat_mass_change_lb,
            'lifespan_increase_years': self.intervention.lifespan_increase_years,
            'healthspan_improvement_percent': self.intervention.healthspan_improvement_percent,
            'hospital_visit_reduction_percent': self.intervention.hospital_visit_reduction_percent
        }

    def calculate_impacts_for_params(self, params: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate impacts for a given set of parameters.
        
        Args:
            params: Dict mapping parameter names to values
        
        Returns:
            Dict mapping impact names to calculated values
        """
        # Store original values
        orig_values = self.get_current_params()
        
        # Update parameters
        self.intervention.muscle_mass_change_lb = params['muscle_mass_change_lb']
        self.intervention.fat_mass_change_lb = params['fat_mass_change_lb']
        self.intervention.lifespan_increase_years = params['lifespan_increase_years']
        self.intervention.healthspan_improvement_percent = params['healthspan_improvement_percent']
        self.intervention.hospital_visit_reduction_percent = params['hospital_visit_reduction_percent']
        
        # Calculate impacts
        impacts = {
            'healthcare_savings': self.calculate_healthcare_savings(),
            'gdp_impact': self.calculate_gdp_impact(),
            'medicare_impact': self.calculate_medicare_impact(),
            'qalys': self.calculate_qalys()
        }
        
        # Restore original values
        self.intervention.muscle_mass_change_lb = orig_values['muscle_mass_change_lb']
        self.intervention.fat_mass_change_lb = orig_values['fat_mass_change_lb']
        self.intervention.lifespan_increase_years = orig_values['lifespan_increase_years']
        self.intervention.healthspan_improvement_percent = orig_values['healthspan_improvement_percent']
        self.intervention.hospital_visit_reduction_percent = orig_values['hospital_visit_reduction_percent']
        
        return impacts

    def validate_assumptions(self) -> None:
        """
        Validate model assumptions.
        
        Raises:
            ValueError: If any assumptions are invalid
        """
        # Population assumptions
        if self.pop.target_population > self.pop.total_population:
            raise ValueError("Target population cannot exceed total population")
        if self.pop.medicare_beneficiaries > self.pop.total_population:
            raise ValueError("Medicare beneficiaries cannot exceed total population")
        if not 0 <= self.pop.workforce_fraction <= 1:
            raise ValueError("Workforce fraction must be between 0 and 1")
            
        # Economic assumptions
        if self.econ.annual_healthcare_cost <= 0:
            raise ValueError("Healthcare cost must be positive")
        if self.econ.annual_productivity <= 0:
            raise ValueError("Productivity must be positive")
        if not 0 <= self.econ.discount_rate <= 0.2:
            raise ValueError("Discount rate must be between 0 and 20%")
            
        # Intervention assumptions
        if self.intervention.muscle_mass_change_lb < -10 or self.intervention.muscle_mass_change_lb > 10:
            raise ValueError("Muscle mass change must be between -10 and +10 lbs")
        if self.intervention.fat_mass_change_lb < -30 or self.intervention.fat_mass_change_lb > 10:
            raise ValueError("Fat mass change must be between -30 and +10 lbs")
        if self.intervention.lifespan_increase_years < 0:
            raise ValueError("Lifespan increase must be positive")
        if not 0 <= self.intervention.healthspan_improvement_percent <= 100:
            raise ValueError("Health improvement must be between 0 and 100%")
        if not 0 <= self.intervention.hospital_visit_reduction_percent <= 100:
            raise ValueError("Hospital visit reduction must be between 0 and 100%") 