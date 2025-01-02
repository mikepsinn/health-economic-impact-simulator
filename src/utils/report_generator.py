"""
Utilities for generating markdown reports from model results.
"""

from typing import Dict, Any
from datetime import datetime
import pandas as pd
import numpy as np

def format_currency(amount: float, unit: str = 'dollars') -> str:
    """Format currency values with appropriate scale."""
    if abs(amount) >= 1e12:
        return f"${amount/1e12:.2f} trillion {unit}"
    elif abs(amount) >= 1e9:
        return f"${amount/1e9:.2f} billion {unit}"
    elif abs(amount) >= 1e6:
        return f"${amount/1e6:.2f} million {unit}"
    else:
        return f"${amount:,.2f} {unit}"

def generate_intervention_report(
    model: Any,
    title: str,
    description: str,
    include_monte_carlo: bool = True
) -> str:
    """
    Generate a markdown report for an intervention's economic impact.
    
    Args:
        model: The impact model instance
        title: Report title
        description: Brief description of the intervention
        include_monte_carlo: Whether to include Monte Carlo analysis
    """
    # Get base results
    results = model.generate_full_report()
    
    # Run Monte Carlo if requested
    monte_carlo_results = None
    confidence_intervals = None
    if include_monte_carlo:
        param_variations = {
            'muscle_gain_lb': 0.1,  # 10% variation
            'fat_loss_lb': 0.1,
            'lifespan_increase_years': 0.15,
            'savings_per_lb': 0.2
        }
        monte_carlo_results, confidence_intervals = model.run_monte_carlo(param_variations)

    # Generate report
    report = f"""# {title}
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
{description}

## Key Findings

### Body Composition Impact
If the intervention increases muscle mass by {model.intervention.muscle_gain_lb} lb and decreases fat mass by {model.intervention.fat_loss_lb} lb across the US population:

- Total Population Affected: {model.pop.target_population:,} people
- Annual Healthcare Savings: {format_currency(results['annual_healthcare_savings_billions'] * 1e9)}
- Per-Person Average Savings: {format_currency(results['annual_healthcare_savings_billions'] * 1e9 / model.pop.target_population, 'per person')}

### Lifespan Impact
A {model.intervention.lifespan_increase_years/0.77:.1f}% increase in average lifespan ({model.intervention.lifespan_increase_years:.2f} years) would result in:

- GDP Impact: {format_currency(results['gdp_impact_trillions'] * 1e12)}
- Annual Medicare Savings: {format_currency(results['annual_medicare_impact_billions'] * 1e9)}
- Per-Beneficiary Medicare Savings: {format_currency(results['annual_medicare_impact_billions'] * 1e9 / model.pop.medicare_beneficiaries, 'per beneficiary')}

## Model Assumptions
- US Total Population: {model.pop.total_population:,}
- Medicare Beneficiaries: {model.pop.medicare_beneficiaries:,}
- Workforce Participation: {model.pop.workforce_fraction*100:.1f}%
- Annual Healthcare Cost: {format_currency(model.econ.annual_healthcare_cost, 'per Medicare beneficiary')}
- Annual Productivity: {format_currency(model.econ.annual_productivity, 'per worker')}
- Discount Rate: {model.econ.discount_rate*100:.1f}%
"""

    if confidence_intervals:
        report += "\n## Uncertainty Analysis\n"
        report += "95% Confidence Intervals from Monte Carlo simulation:\n\n"
        
        for metric, ci in confidence_intervals.items():
            report += f"### {metric.replace('_', ' ').title()}\n"
            report += f"- Mean: {format_currency(ci['mean'])}\n"
            report += f"- Range: {format_currency(ci['lower_ci'])} to {format_currency(ci['upper_ci'])}\n"
            report += f"- Standard Deviation: {format_currency(ci['std'])}\n\n"

    return report 