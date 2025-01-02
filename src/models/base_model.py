"""Base economic impact model."""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import numpy as np

from .parameters import (
    BasePopulationParams,
    BaseEconomicParams,
    BaseInterventionParams,
    TotalBenefits
)
from .calculators import (
    calculate_cognitive_benefits,
    calculate_kidney_benefits,
    calculate_physical_benefits,
    calculate_longevity_benefits,
    calculate_healthcare_benefits
)

class BaseImpactModel:
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

    def calculate_total_benefits(self, base_config: Dict) -> TotalBenefits:
        """Calculate combined benefits from all effects."""
        # Calculate benefits from each type of effect
        cognitive = calculate_cognitive_benefits(
            self.intervention.cognitive,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        kidney = calculate_kidney_benefits(
            self.intervention.kidney,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        physical = calculate_physical_benefits(
            self.intervention.physical,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        longevity = calculate_longevity_benefits(
            self.intervention.longevity,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        healthcare = calculate_healthcare_benefits(
            self.intervention.healthcare,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        # Combine all benefits
        return TotalBenefits(
            gdp_impact=(
                (cognitive.gdp_impact if cognitive else 0) +
                (longevity.gdp_impact if longevity else 0)
            ),
            healthcare_savings=(
                (physical.healthcare_savings if physical else 0) +
                (healthcare.hospital_savings if healthcare else 0)
            ),
            medicare_savings=(
                (cognitive.medicare_savings if cognitive else 0) +
                (kidney.medicare_savings if kidney else 0) +
                (healthcare.medicare_savings if healthcare else 0)
            ),
            qaly_improvement=(
                (cognitive.qaly_improvement if cognitive else 0) +
                (kidney.qaly_improvement if kidney else 0) +
                (physical.qaly_improvement if physical else 0) +
                (longevity.qaly_improvement if longevity else 0) +
                (healthcare.qaly_improvement if healthcare else 0)
            )
        )

    def generate_full_report(self, base_config: dict) -> dict:
        """Generate a complete impact report."""
        # Calculate benefits
        cognitive_benefits = calculate_cognitive_benefits(
            self.intervention.cognitive,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        kidney_benefits = calculate_kidney_benefits(
            self.intervention.kidney,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        physical_benefits = calculate_physical_benefits(
            self.intervention.physical,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        longevity_benefits = calculate_longevity_benefits(
            self.intervention.longevity,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        healthcare_benefits = calculate_healthcare_benefits(
            self.intervention.healthcare,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        # Combine all benefits
        total_gdp = (
            (cognitive_benefits.gdp_impact if cognitive_benefits else 0) +
            (longevity_benefits.gdp_impact if longevity_benefits else 0)
        )
        
        total_healthcare = (
            (physical_benefits.healthcare_savings if physical_benefits else 0) +
            (healthcare_benefits.hospital_savings if healthcare_benefits else 0)
        )
        
        total_medicare = (
            (cognitive_benefits.medicare_savings if cognitive_benefits else 0) +
            (kidney_benefits.medicare_savings if kidney_benefits else 0) +
            (healthcare_benefits.medicare_savings if healthcare_benefits else 0)
        )
        
        total_qalys = (
            (cognitive_benefits.qaly_improvement if cognitive_benefits else 0) +
            (kidney_benefits.qaly_improvement if kidney_benefits else 0) +
            (physical_benefits.qaly_improvement if physical_benefits else 0) +
            (longevity_benefits.qaly_improvement if longevity_benefits else 0) +
            (healthcare_benefits.qaly_improvement if healthcare_benefits else 0)
        )
        
        return {
            'total_benefits': TotalBenefits(
                gdp_impact=total_gdp,
                healthcare_savings=total_healthcare,
                medicare_savings=total_medicare,
                qaly_improvement=total_qalys
            ),
            'cognitive_benefits': cognitive_benefits,
            'kidney_benefits': kidney_benefits,
            'physical_benefits': physical_benefits,
            'longevity_benefits': longevity_benefits,
            'healthcare_benefits': healthcare_benefits,
            'annual_healthcare_savings_billions': total_healthcare / 1e9,
            'gdp_impact_trillions': total_gdp / 1e12,
            'annual_medicare_impact_billions': total_medicare / 1e9,
            'qalys_gained': total_qalys
        }

    def apply_discount_rate(self, value: float, years: float) -> float:
        """Apply discount rate to a value over a number of years."""
        return value / ((1 + self.econ.discount_rate) ** years)
        
    def validate_assumptions(self) -> None:
        """Validate model assumptions."""
        # Validate population assumptions
        if self.pop.target_population > self.pop.total_population:
            raise ValueError("Target population cannot exceed total population")
            
        # Validate economic assumptions
        if self.econ.annual_healthcare_cost <= 0:
            raise ValueError("Annual healthcare cost must be positive")
        if self.econ.annual_productivity <= 0:
            raise ValueError("Annual productivity must be positive")
            
        # Validate intervention assumptions
        if self.intervention.longevity.lifespan_increase_percent < 0:
            raise ValueError("Lifespan increase cannot be negative")
        if self.intervention.healthcare.hospital_visit_reduction_percent < 0:
            raise ValueError("Hospital visit reduction cannot be negative")
            
    def generate_full_report(self, base_config: dict) -> dict:
        """Generate a complete impact report."""
        # Calculate benefits
        cognitive_benefits = calculate_cognitive_benefits(
            self.intervention.cognitive,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        kidney_benefits = calculate_kidney_benefits(
            self.intervention.kidney,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        physical_benefits = calculate_physical_benefits(
            self.intervention.physical,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        longevity_benefits = calculate_longevity_benefits(
            self.intervention.longevity,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        healthcare_benefits = calculate_healthcare_benefits(
            self.intervention.healthcare,
            self.pop,
            self.econ,
            self.intervention.modifiers,
            base_config
        )
        
        # Combine all benefits
        total_gdp = (
            (cognitive_benefits.gdp_impact if cognitive_benefits else 0) +
            (longevity_benefits.gdp_impact if longevity_benefits else 0)
        )
        
        total_healthcare = (
            (physical_benefits.healthcare_savings if physical_benefits else 0) +
            (healthcare_benefits.hospital_savings if healthcare_benefits else 0)
        )
        
        total_medicare = (
            (cognitive_benefits.medicare_savings if cognitive_benefits else 0) +
            (kidney_benefits.medicare_savings if kidney_benefits else 0) +
            (healthcare_benefits.medicare_savings if healthcare_benefits else 0)
        )
        
        total_qalys = (
            (cognitive_benefits.qaly_improvement if cognitive_benefits else 0) +
            (kidney_benefits.qaly_improvement if kidney_benefits else 0) +
            (physical_benefits.qaly_improvement if physical_benefits else 0) +
            (longevity_benefits.qaly_improvement if longevity_benefits else 0) +
            (healthcare_benefits.qaly_improvement if healthcare_benefits else 0)
        )
        
        return {
            'total_benefits': TotalBenefits(
                gdp_impact=total_gdp,
                healthcare_savings=total_healthcare,
                medicare_savings=total_medicare,
                qaly_improvement=total_qalys
            ),
            'cognitive_benefits': cognitive_benefits,
            'kidney_benefits': kidney_benefits,
            'physical_benefits': physical_benefits,
            'longevity_benefits': longevity_benefits,
            'healthcare_benefits': healthcare_benefits,
            'annual_healthcare_savings_billions': total_healthcare / 1e9,
            'gdp_impact_trillions': total_gdp / 1e12,
            'annual_medicare_impact_billions': total_medicare / 1e9,
            'qalys_gained': total_qalys
        } 

    def calculate_qalys(self) -> float:
        """Calculate total quality-adjusted life years gained."""
        # Calculate QALYs from lifespan increase
        base_qalys = (
            self.pop.target_population *
            self.intervention.lifespan_increase_years *
            (1 + self.intervention.longevity.healthspan_improvement_percent / 100.0)
        )
        
        # Add QALYs from physical improvements if present
        if self.intervention.physical:
            muscle_qalys = (
                self.pop.target_population *
                abs(self.intervention.physical.muscle_mass_change_lb) *
                0.001  # Each pound of muscle affects quality of life by 0.1%
            )
            fat_qalys = (
                self.pop.target_population *
                abs(self.intervention.physical.fat_mass_change_lb) *
                0.0005  # Each pound of fat affects quality of life by 0.05%
            )
            base_qalys += muscle_qalys + fat_qalys
        
        # Add QALYs from cognitive improvements if present
        if self.intervention.cognitive:
            iq_qalys = (
                self.pop.target_population *
                self.intervention.cognitive.iq_increase *
                0.01  # Each IQ point improves quality of life by 1%
            )
            alzheimers_qalys = (
                self.pop.medicare_beneficiaries *
                (self.intervention.cognitive.alzheimers_reduction / 100.0) *
                0.2  # Alzheimer's reduces quality of life by 20%
            )
            base_qalys += iq_qalys + alzheimers_qalys
        
        # Add QALYs from kidney improvements if present
        if self.intervention.kidney:
            egfr_qalys = (
                self.pop.target_population *
                self.intervention.kidney.egfr_improvement *
                0.01  # Each mL/min/1.73m² improves quality of life by 1%
            )
            ckd_qalys = (
                self.pop.medicare_beneficiaries *
                (self.intervention.kidney.ckd_progression_reduction / 100.0) *
                0.3  # CKD reduces quality of life by 30%
            )
            base_qalys += egfr_qalys + ckd_qalys
        
        # Add QALYs from reduced hospital visits
        hospital_qalys = (
            self.pop.target_population *
            (self.intervention.healthcare.hospital_visit_reduction_percent / 100.0) *
            0.1  # Each avoided hospital visit improves quality of life by 10%
        )
        base_qalys += hospital_qalys
        
        # Apply health quality modifier
        return base_qalys * self.intervention.modifiers.health_quality 