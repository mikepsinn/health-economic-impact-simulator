"""Calculator for physical composition benefits."""

from dataclasses import dataclass
from typing import Dict, Optional

from ..parameters import (
    PhysicalParams,
    BasePopulationParams,
    BaseEconomicParams,
    ImpactModifiers
)

@dataclass
class PhysicalBenefits:
    """Benefits from physical composition changes."""
    healthcare_savings: float
    qaly_improvement: float

def calculate_physical_benefits(
    params: Optional[PhysicalParams],
    pop: BasePopulationParams,
    econ: BaseEconomicParams,
    modifiers: ImpactModifiers,
    base_config: Dict
) -> Optional[PhysicalBenefits]:
    """Calculate benefits from physical composition changes."""
    if not params:
        return None
        
    # Calculate healthcare savings from muscle and fat changes
    muscle_savings = (
        params.muscle_mass_change_lb * 
        pop.target_population * 
        base_config['healthcare']['savings_per_lb_muscle']
    )
    
    fat_savings = (
        abs(params.fat_mass_change_lb) *  # Use absolute value since both gain and loss have costs
        pop.target_population * 
        base_config['healthcare']['savings_per_lb_fat']
    )
    
    total_savings = muscle_savings + fat_savings
    
    # Calculate QALY improvement
    # Assume each pound of muscle gain improves quality of life by 0.001
    # and each pound of fat loss improves quality of life by 0.0005
    qaly_muscle = params.muscle_mass_change_lb * 0.001 * pop.target_population
    qaly_fat = abs(params.fat_mass_change_lb) * 0.0005 * pop.target_population
    
    total_qalys = (qaly_muscle + qaly_fat) * modifiers.health_quality
    
    return PhysicalBenefits(
        healthcare_savings=total_savings,
        qaly_improvement=total_qalys
    ) 