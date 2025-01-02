"""Calculator for cognitive benefits."""

from typing import Dict, Optional

from ..parameters import (
    CognitiveParams,
    BasePopulationParams,
    BaseEconomicParams,
    ImpactModifiers
)
from ..benefits import CognitiveBenefits

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
    # Each IQ point increases productivity by the modifier percentage
    gdp_impact = (
        params.iq_increase *
        modifiers.iq_to_gdp *
        pop.target_population *
        pop.workforce_fraction *
        econ.annual_productivity
    )
    
    # Calculate Medicare savings from reduced Alzheimer's progression
    medicare_savings = (
        (params.alzheimers_reduction / 100.0) *
        modifiers.alzheimers_to_medicare *
        base_config['healthcare']['annual_alzheimers_cost']
    )
    
    # Calculate QALY improvement
    # Each IQ point improves quality of life by 1%
    qaly_iq = params.iq_increase * 0.01 * pop.target_population
    
    # Reduced Alzheimer's progression improves quality of life by 20%
    qaly_alzheimers = (
        pop.medicare_beneficiaries *
        (params.alzheimers_reduction / 100.0) *
        0.2
    )
    
    return CognitiveBenefits(
        gdp_impact=gdp_impact,
        medicare_savings=medicare_savings,
        qaly_improvement=qaly_iq + qaly_alzheimers
    ) 