"""Calculator for kidney function benefits."""

from dataclasses import dataclass
from typing import Dict, Optional

from ..parameters import (
    KidneyParams,
    BasePopulationParams,
    BaseEconomicParams,
    ImpactModifiers
)

@dataclass
class KidneyBenefits:
    """Benefits from improved kidney function."""
    medicare_savings: float
    qaly_improvement: float

def calculate_kidney_benefits(
    params: Optional[KidneyParams],
    pop: BasePopulationParams,
    econ: BaseEconomicParams,
    modifiers: ImpactModifiers,
    base_config: Dict
) -> Optional[KidneyBenefits]:
    """Calculate benefits from improved kidney function."""
    if not params:
        return None
        
    # Calculate Medicare savings from improved kidney function
    ckd_baseline_cost = base_config['healthcare']['annual_ckd_cost']
    medicare_savings = (
        ckd_baseline_cost *
        (params.ckd_progression_reduction / 100.0) *
        pop.medicare_beneficiaries *
        modifiers.kidney_to_medicare
    )
    
    # Calculate QALY improvement
    # Assume each mL/min/1.73m² of eGFR improvement increases quality of life by 0.01
    # and CKD progression reduction improves quality of life proportionally
    qaly_egfr = params.egfr_improvement * 0.01 * pop.target_population
    qaly_ckd = (
        params.ckd_progression_reduction / 100.0 *
        0.3 *  # Assume CKD reduces quality of life by 0.3
        pop.medicare_beneficiaries
    )
    
    total_qalys = (qaly_egfr + qaly_ckd) * modifiers.health_quality
    
    return KidneyBenefits(
        medicare_savings=medicare_savings,
        qaly_improvement=total_qalys
    ) 