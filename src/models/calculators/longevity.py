"""Calculator for longevity benefits."""

from typing import Dict, Optional

from ..parameters import (
    LongevityParams,
    BasePopulationParams,
    BaseEconomicParams,
    ImpactModifiers
)
from ..benefits import LongevityBenefits

def calculate_longevity_benefits(
    params: Optional[LongevityParams],
    pop: BasePopulationParams,
    econ: BaseEconomicParams,
    modifiers: ImpactModifiers,
    base_config: Dict
) -> Optional[LongevityBenefits]:
    """Calculate benefits from increased lifespan."""
    if not params:
        return None
        
    # Calculate GDP impact from increased productive years
    # Assume productivity scales with lifespan increase and health quality
    gdp_impact = (
        params.lifespan_increase_years *
        modifiers.lifespan_to_gdp *
        pop.target_population *
        pop.workforce_fraction *
        econ.annual_productivity
    )
    
    # Calculate QALY improvement from increased lifespan
    # Scale by health quality improvement
    qalys = (
        params.lifespan_increase_years *
        pop.target_population *
        (1 + params.healthspan_improvement_percent / 100.0)
    )
    
    return LongevityBenefits(
        gdp_impact=gdp_impact,
        qaly_improvement=qalys
    ) 