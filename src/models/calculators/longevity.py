"""Calculator for longevity benefits."""

from dataclasses import dataclass
from typing import Dict, Optional

from ..parameters import (
    LongevityParams,
    BasePopulationParams,
    BaseEconomicParams,
    ImpactModifiers
)

@dataclass
class LongevityBenefits:
    """Benefits from increased lifespan and healthspan."""
    gdp_impact: float
    qaly_improvement: float

def calculate_longevity_benefits(
    params: LongevityParams,
    pop: BasePopulationParams,
    econ: BaseEconomicParams,
    modifiers: ImpactModifiers,
    base_config: Dict
) -> LongevityBenefits:
    """Calculate benefits from increased lifespan and healthspan."""
    # Calculate GDP impact from increased productive years
    # Assume working years increase proportionally with lifespan
    additional_working_years = (
        params.lifespan_increase_percent / 100.0 *
        pop.workforce_fraction *
        pop.target_population
    )
    
    gdp_impact = (
        additional_working_years *
        econ.annual_productivity *
        modifiers.lifespan_to_gdp
    )
    
    # Calculate QALY improvement from increased lifespan and health quality
    base_life_expectancy = 79.1  # years
    additional_years = base_life_expectancy * (params.lifespan_increase_percent / 100.0)
    
    qaly_improvement = (
        pop.target_population *
        additional_years *
        (params.healthspan_improvement_percent / 100.0)
    )
    
    return LongevityBenefits(
        gdp_impact=gdp_impact,
        qaly_improvement=qaly_improvement
    ) 