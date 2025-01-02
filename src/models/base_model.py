"""Base economic impact model."""

from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import numpy as np

from .parameters import (
    BasePopulationParams,
    BaseEconomicParams,
    BaseInterventionParams,
    HealthcareParams,
    ImpactModifiers
)
from .report import Report, ReportMetrics
from .calculators import (
    PhysicalCalculator,
    CognitiveCalculator,
    KidneyCalculator,
    LongevityCalculator,
    HealthcareCalculator
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
        
        # Initialize calculators
        self.physical_calculator = PhysicalCalculator(
            pop=self.pop,
            econ=self.econ,
            healthcare=self.intervention.healthcare,
            modifiers=self.intervention.modifiers
        )
        self.cognitive_calculator = CognitiveCalculator(
            pop=self.pop,
            econ=self.econ,
            healthcare=self.intervention.healthcare,
            modifiers=self.intervention.modifiers
        )
        self.kidney_calculator = KidneyCalculator(
            pop=self.pop,
            econ=self.econ,
            healthcare=self.intervention.healthcare,
            modifiers=self.intervention.modifiers
        )
        self.longevity_calculator = LongevityCalculator(
            pop=self.pop,
            econ=self.econ,
            healthcare=self.intervention.healthcare,
            modifiers=self.intervention.modifiers
        )
        self.healthcare_calculator = HealthcareCalculator(
            pop=self.pop,
            econ=self.econ,
            healthcare=self.intervention.healthcare,
            modifiers=self.intervention.modifiers
        )
        
        # Calculate results
        self.physical_results = {}
        self.cognitive_results = {}
        self.kidney_results = {}
        self.longevity_results = {}
        self.healthcare_results = {}
        self.calculate_all_impacts()

    def calculate_all_impacts(self) -> None:
        """Calculate impacts from all pathways."""
        if self.intervention.physical:
            self.physical_results = self.physical_calculator.calculate(
                self.intervention.physical.dict()
            )
            
        if self.intervention.cognitive:
            self.cognitive_results = self.cognitive_calculator.calculate(
                self.intervention.cognitive.dict()
            )
            
        if self.intervention.kidney:
            self.kidney_results = self.kidney_calculator.calculate(
                self.intervention.kidney.dict()
            )
            
        self.longevity_results = self.longevity_calculator.calculate(
            self.intervention.longevity.dict()
        )
        
        self.healthcare_results = self.healthcare_calculator.calculate(
            self.intervention.healthcare.dict()
        )

    def generate_full_report(self, base_config: Dict[str, Any]) -> Report:
        """Generate a complete impact report."""
        # Calculate total metrics
        total_healthcare_savings = (
            self.physical_results.get('healthcare_savings', 0) +
            self.healthcare_results.get('visit_savings', 0)
        )
        
        total_medicare_savings = (
            self.cognitive_results.get('alzheimers_savings', 0) +
            self.kidney_results.get('medicare_savings', 0)
        )
        
        total_gdp_impact = (
            self.cognitive_results.get('gdp_impact', 0) +
            self.longevity_results.get('gdp_impact', 0)
        )
        
        total_qalys = (
            self.physical_results.get('qalys_gained', 0) +
            self.cognitive_results.get('qalys_gained', 0) +
            self.kidney_results.get('qalys_gained', 0) +
            self.healthcare_results.get('qalys_gained', 0)
        )
        
        # Create report metrics
        metrics = ReportMetrics(
            annual_healthcare_savings=total_healthcare_savings,
            annual_medicare_savings=total_medicare_savings,
            total_gdp_impact=total_gdp_impact,
            total_qalys=total_qalys
        )
        
        return Report(metrics=metrics) 