"""Calculator for kidney function benefits."""

from typing import Dict, Optional

from ..parameters import (
    KidneyParams,
    BasePopulationParams,
    BaseEconomicParams,
    ImpactModifiers
)
from ..benefits import KidneyBenefits

def calculate_kidney_benefits(
    params: Optional[KidneyParams],
    pop: BasePopulationParams,
    econ: BaseEconomicParams,
    modifiers: ImpactModifiers,
    base_config: Dict
) -> Optional[KidneyBenefits]:
    """Calculate benefits from kidney function improvements."""
    if not params:
        return None
        
    # Calculate Medicare savings from reduced CKD progression
    medicare_savings = (
        (params.ckd_progression_reduction / 100.0) *
        modifiers.kidney_to_medicare *
        base_config['healthcare']['annual_ckd_cost']
    )
    
    # Calculate QALY improvement
    # Each mL/min/1.73m² of eGFR improves quality of life by 1%
    qaly_egfr = params.egfr_improvement * 0.01 * pop.target_population
    
    # Reduced CKD progression improves quality of life by 30%
    qaly_ckd = (
        pop.medicare_beneficiaries *
        (params.ckd_progression_reduction / 100.0) *
        0.3
    )
    
    return KidneyBenefits(
        medicare_savings=medicare_savings,
        qaly_improvement=qaly_egfr + qaly_ckd
    ) 