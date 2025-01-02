"""Base economic impact model."""

from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import numpy as np

from .parameters import (
    BasePopulationParams,
    BaseEconomicParams,
    BaseInterventionParams
)
from .benefits import BenefitMetrics
from .report import Report, ReportMetrics, DetailedBenefits
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

    def generate_full_report(self, base_config: dict) -> Report:
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
        
        # Create report with validated data model
        return Report(
            metrics=ReportMetrics(
                annual_healthcare_savings=total_healthcare,
                total_gdp_impact=total_gdp,
                annual_medicare_savings=total_medicare,
                total_qalys=total_qalys
            ),
            benefits=DetailedBenefits(
                cognitive_benefits=cognitive_benefits.model_dump() if cognitive_benefits else None,
                kidney_benefits=kidney_benefits.model_dump() if kidney_benefits else None,
                physical_benefits=physical_benefits.model_dump() if physical_benefits else None,
                longevity_benefits=longevity_benefits.model_dump() if longevity_benefits else None,
                healthcare_benefits=healthcare_benefits.model_dump() if healthcare_benefits else None,
                total_benefits=BenefitMetrics(
                    gdp_impact=total_gdp,
                    healthcare_savings=total_healthcare,
                    medicare_savings=total_medicare,
                    qaly_improvement=total_qalys
                ).model_dump()
            ),
            validation_warnings=""  # Will be set later after validation
        )

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
        if self.intervention.longevity.lifespan_increase_years < 0:
            raise ValueError("Lifespan increase cannot be negative")
        if self.intervention.healthcare.hospital_visit_reduction_percent < 0:
            raise ValueError("Hospital visit reduction cannot be negative") 