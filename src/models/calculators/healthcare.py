"""Calculator for healthcare utilization benefits."""

from dataclasses import dataclass
from typing import Dict, Optional

from ..parameters import (
    HealthcareParams,
    BasePopulationParams,
    BaseEconomicParams,
    ImpactModifiers
)

@dataclass
class HealthcareBenefits:
    """Benefits from reduced healthcare utilization."""
    hospital_savings: float
    medicare_savings: float
    qaly_improvement: float

def calculate_healthcare_benefits(
    params: HealthcareParams,
    pop: BasePopulationParams,
    econ: BaseEconomicParams,
    modifiers: ImpactModifiers,
    base_config: Dict
) -> HealthcareBenefits:
    """Calculate benefits from reduced healthcare utilization."""
    # Calculate hospital visit savings
    annual_visits = base_config['healthcare']['annual_hospital_visits']
    visits_reduced = (
        annual_visits *
        (params.hospital_visit_reduction_percent / 100.0) *
        pop.target_population
    )
    
    hospital_savings = visits_reduced * params.cost_per_hospital_visit
    
    # Calculate Medicare savings (assume 40% of hospital costs are Medicare)
    medicare_savings = hospital_savings * 0.4
    
    # Calculate QALY improvement
    # Assume each avoided hospital visit improves quality of life by 0.1
    qaly_improvement = (
        visits_reduced *
        0.1 *
        modifiers.health_quality
    )
    
    return HealthcareBenefits(
        hospital_savings=hospital_savings,
        medicare_savings=medicare_savings,
        qaly_improvement=qaly_improvement
    ) 