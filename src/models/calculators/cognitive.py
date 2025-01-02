"""Calculator for cognitive benefits."""

from dataclasses import dataclass
from typing import Dict, Optional

from ..parameters import (
    CognitiveParams,
    BasePopulationParams,
    BaseEconomicParams,
    ImpactModifiers
)

@dataclass
class CognitiveBenefits:
    """Benefits from cognitive improvements."""
    gdp_impact: float
    medicare_savings: float
    qaly_improvement: float

def calculate_cognitive_benefits(
    params: Optional[CognitiveParams],
    pop: BasePopulationParams,
    econ: BaseEconomicParams,
    modifiers: ImpactModifiers,
    base_config: Dict
) -> Optional[CognitiveBenefits]:
    """Calculate benefits from cognitive improvements."""
    if not params:
        return None
        
    # Calculate GDP impact from IQ increase
    gdp_impact = (
        params.iq_increase *
        pop.target_population *
        econ.annual_productivity *
        modifiers.iq_to_gdp
    )
    
    # Calculate Medicare savings from reduced Alzheimer's
    alzheimers_baseline_cost = base_config['healthcare']['annual_alzheimers_cost']
    medicare_savings = (
        alzheimers_baseline_cost *
        (params.alzheimers_reduction / 100.0) *
        pop.medicare_beneficiaries *
        modifiers.alzheimers_to_medicare
    )
    
    # Calculate QALY improvement
    # Assume each IQ point improves quality of life by 0.01
    # and Alzheimer's reduction improves quality of life proportionally
    qaly_iq = params.iq_increase * 0.01 * pop.target_population
    qaly_alzheimers = (
        params.alzheimers_reduction / 100.0 *
        0.2 *  # Assume Alzheimer's reduces quality of life by 0.2
        pop.medicare_beneficiaries
    )
    
    total_qalys = (qaly_iq + qaly_alzheimers) * modifiers.health_quality
    
    return CognitiveBenefits(
        gdp_impact=gdp_impact,
        medicare_savings=medicare_savings,
        qaly_improvement=total_qalys
    ) 