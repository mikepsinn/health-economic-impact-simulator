"""Base model for all impact calculations."""

from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod

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

class BaseParameters(BaseModel):
    """Base parameters shared across all models."""
    population_size: int = Field(default=331900000, description="Total US population")
    medicare_population: int = Field(default=73000000, description="Population over 60")
    adult_population: int = Field(default=258300000, description="Adult population (18+)")
    medicare_per_capita: float = Field(default=12500, description="Annual Medicare spending per beneficiary")
    gdp_per_capita: float = Field(default=65000, description="US GDP per capita")
    discount_rate: float = Field(default=0.03, description="Annual discount rate for future values")
    time_horizon_years: int = Field(default=10, description="Time horizon for calculations in years")

class BaseImpactModel(ABC):
    """Abstract base class for all impact models."""
    
    def __init__(self, params: Optional[BaseParameters] = None):
        self.params = params or BaseParameters()
        
    @abstractmethod
    def calculate_impacts(self) -> Dict[str, Any]:
        """Calculate health and economic impacts."""
        pass
    
    def calculate_npv(self, annual_value: float, years: int) -> float:
        """Calculate net present value of future cash flows."""
        npv = 0
        for year in range(years):
            npv += annual_value / ((1 + self.params.discount_rate) ** year)
        return npv
    
    def calculate_medicare_savings(self, reduction_percentage: float) -> float:
        """Calculate Medicare savings based on a reduction percentage."""
        annual_savings = (
            self.params.medicare_population * 
            self.params.medicare_per_capita * 
            reduction_percentage
        )
        return self.calculate_npv(annual_savings, self.params.time_horizon_years)
    
    def calculate_gdp_impact(self, productivity_increase: float) -> float:
        """Calculate GDP impact from productivity changes."""
        annual_impact = (
            self.params.adult_population * 
            self.params.gdp_per_capita * 
            productivity_increase
        )
        return self.calculate_npv(annual_impact, self.params.time_horizon_years)

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