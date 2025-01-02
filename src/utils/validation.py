"""Validation utilities for economic impact calculations."""

from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class ValidationBounds:
    """Bounds for validating economic calculations."""
    # US total healthcare expenditure 2023: ~$4.5T
    MAX_HEALTHCARE_SAVINGS_PCT = 0.05  # Max 5% reduction
    
    # US GDP 2023: ~$25T
    MAX_GDP_IMPACT_PCT = 0.02  # Max 2% impact
    
    # Medicare spending 2023: ~$1T
    MAX_MEDICARE_SAVINGS_PCT = 0.10  # Max 10% reduction
    
    # Life expectancy ~79 years
    MAX_QALY_PER_PERSON = 5  # Max additional QALYs per person

def validate_economic_impacts(
    healthcare_savings: float,
    gdp_impact: float,
    medicare_savings: float,
    qalys: float,
    population: int,
    base_healthcare_cost: float,
    base_gdp: Optional[float] = 25e12,  # US GDP ~$25T
    base_medicare: Optional[float] = 1e12,  # Medicare spending ~$1T
) -> Dict[str, str]:
    """
    Validate economic impact calculations against realistic bounds.
    Returns a dict of validation messages for any exceeded bounds.
    """
    bounds = ValidationBounds()
    messages = {}
    
    # Validate healthcare savings
    total_healthcare = base_healthcare_cost * population
    savings_pct = healthcare_savings / total_healthcare
    if savings_pct > bounds.MAX_HEALTHCARE_SAVINGS_PCT:
        messages['healthcare_savings'] = (
            f"Healthcare savings of ${healthcare_savings:,.2f} exceed maximum expected "
            f"reduction of {bounds.MAX_HEALTHCARE_SAVINGS_PCT:.1%} of total expenditure"
        )
    
    # Validate GDP impact
    if base_gdp:
        gdp_pct = gdp_impact / base_gdp
        if gdp_pct > bounds.MAX_GDP_IMPACT_PCT:
            messages['gdp_impact'] = (
                f"GDP impact of ${gdp_impact:,.2f} exceeds maximum expected "
                f"impact of {bounds.MAX_GDP_IMPACT_PCT:.1%} of GDP"
            )
    
    # Validate Medicare savings
    if base_medicare:
        medicare_pct = medicare_savings / base_medicare
        if medicare_pct > bounds.MAX_MEDICARE_SAVINGS_PCT:
            messages['medicare_savings'] = (
                f"Medicare savings of ${medicare_savings:,.2f} exceed maximum expected "
                f"reduction of {bounds.MAX_MEDICARE_SAVINGS_PCT:.1%} of Medicare spending"
            )
    
    # Validate QALYs
    qaly_per_person = qalys / population
    if qaly_per_person > bounds.MAX_QALY_PER_PERSON:
        messages['qalys'] = (
            f"QALYs gained per person ({qaly_per_person:.1f}) exceed maximum "
            f"expected gain of {bounds.MAX_QALY_PER_PERSON} QALYs"
        )
    
    return messages

def format_validation_messages(messages: Dict[str, str]) -> str:
    """Format validation messages for report."""
    if not messages:
        return ""
    
    formatted = "### Validation Warnings\n\n"
    formatted += "The following calculations exceed expected bounds:\n\n"
    for msg in messages.values():
        formatted += f"- {msg}\n"
    return formatted 