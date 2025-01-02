"""Calculator for healthcare utilization benefits."""

from typing import Dict, Optional

from ..parameters import (
    HealthcareParams,
    BasePopulationParams,
    BaseEconomicParams,
    ImpactModifiers
)
from ..benefits import HealthcareBenefits

def calculate_healthcare_benefits(
    params: Optional[HealthcareParams],
    pop: BasePopulationParams,
    econ: BaseEconomicParams,
    modifiers: ImpactModifiers,
    base_config: Dict
) -> Optional[HealthcareBenefits]:
    """Calculate benefits from reduced healthcare utilization."""
    if not params:
        return None
        
    # Calculate savings from reduced hospital visits
    total_visits = base_config['healthcare']['annual_hospital_visits']
    visits_reduced = total_visits * (params.hospital_visit_reduction_percent / 100.0)
    cost_per_visit = econ.annual_healthcare_cost * pop.total_population / total_visits
    
    hospital_savings = visits_reduced * cost_per_visit
    
    # Calculate Medicare portion of savings
    medicare_savings = hospital_savings * (pop.medicare_beneficiaries / pop.total_population)
    
    # Calculate QALY improvement
    # Each avoided hospital visit improves quality of life by 10%
    qalys = (
        pop.target_population *
        (params.hospital_visit_reduction_percent / 100.0) *
        0.1
    )
    
    return HealthcareBenefits(
        hospital_savings=hospital_savings,
        medicare_savings=medicare_savings,
        qaly_improvement=qalys
    ) 