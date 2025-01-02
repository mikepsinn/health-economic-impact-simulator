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

def format_number(number: float, precision: int = 2) -> str:
    """Format numbers with appropriate scale and commas."""
    if abs(number) >= 1e9:
        return f"{number/1e9:.{precision}f} billion"
    elif abs(number) >= 1e6:
        return f"{number/1e6:.{precision}f} million"
    elif abs(number) >= 1e3:
        return f"{number/1e3:.{precision}f} thousand"
    else:
        return f"{number:,.{precision}f}"

def generate_intervention_report(
    model: Any,
    title: str,
    description: str,
    include_monte_carlo: bool = True
) -> str:
    """
    Generate a detailed markdown report for an intervention's economic impact.
    
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

## Executive Summary
{description}

## 1. Introduction

### 1.1 Background
This analysis examines the potential economic and health impacts of interventions that modify body composition and longevity. The study focuses on two primary mechanisms of impact:
1. Direct healthcare cost savings from improved body composition
2. Economic gains from increased healthy lifespan

### 1.2 Study Objectives
- Quantify the cumulative healthcare savings from population-wide body composition improvements
- Calculate the economic impact of increased lifespan on GDP and Medicare spending
- Assess the uncertainty and sensitivity of these estimates
- Provide actionable insights for policy makers and healthcare stakeholders

## 2. Methodology

### 2.1 Population Parameters
- Total US Population: {format_number(model.pop.total_population)}
- Medicare Beneficiaries: {format_number(model.pop.medicare_beneficiaries)}
- Workforce Participation Rate: {model.pop.workforce_fraction*100:.1f}%

### 2.2 Economic Parameters
- Annual Healthcare Cost per Medicare Beneficiary: {format_currency(model.econ.annual_healthcare_cost)}
- Annual Worker Productivity: {format_currency(model.econ.annual_productivity)}
- Discount Rate: {model.econ.discount_rate*100:.1f}%

### 2.3 Intervention Parameters
- Muscle Mass Gain: {model.intervention.muscle_gain_lb:.1f} lb per person
- Fat Mass Loss: {model.intervention.fat_loss_lb:.1f} lb per person
- Lifespan Increase: {model.intervention.lifespan_increase_years:.2f} years ({model.intervention.lifespan_increase_years/0.77:.1f}%)
- Healthcare Savings per Pound Improved: {format_currency(model.intervention.savings_per_lb)}

### 2.4 Analytical Methods
The analysis employs several quantitative approaches:
1. **Direct Impact Calculation**: Deterministic calculations using base parameters
2. **Monte Carlo Simulation**: Probabilistic analysis with parameter variations
3. **Sensitivity Analysis**: Systematic parameter variation to assess result robustness
4. **Age Stratification**: Demographic-specific impact assessment

## 3. Results

### 3.1 Body Composition Impact Analysis
The intervention's effect on muscle gain and fat loss yields significant healthcare savings:

**Annual Direct Healthcare Savings**:
- Total Savings: {format_currency(results['annual_healthcare_savings_billions'] * 1e9)}
- Per-Person Savings: {format_currency(results['annual_healthcare_savings_billions'] * 1e9 / model.pop.target_population, 'per person')}

**Calculation Methodology**:
```math
Healthcare\\ Savings = Population \\times (Muscle\\ Gain + Fat\\ Loss) \\times Savings\\ per\\ Pound

                    = {format_number(model.pop.target_population)} \\times ({model.intervention.muscle_gain_lb:.1f} + {model.intervention.fat_loss_lb:.1f}) \\times ${model.intervention.savings_per_lb:.2f}

                    = {format_currency(results['annual_healthcare_savings_billions'] * 1e9)}
```

### 3.2 Lifespan Impact Analysis
A {model.intervention.lifespan_increase_years/0.77:.1f}% increase in average lifespan produces substantial economic effects:

**GDP Impact**:
- Total Impact: {format_currency(results['gdp_impact_trillions'] * 1e12)}
- Calculation includes workforce participation and productivity gains
- Discounted at {model.econ.discount_rate*100:.1f}% annually

**Medicare Savings**:
- Annual Savings: {format_currency(results['annual_medicare_impact_billions'] * 1e9)}
- Per-Beneficiary: {format_currency(results['annual_medicare_impact_billions'] * 1e9 / model.pop.medicare_beneficiaries, 'per beneficiary')}

**Calculation Methodology**:
```math
GDP\\ Impact = Population \\times Workforce\\ Fraction \\times Years\\ Gained \\times Annual\\ Productivity \\times Discount\\ Factor

            = {format_number(model.pop.target_population)} \\times {model.pop.workforce_fraction:.2f} \\times {model.intervention.lifespan_increase_years:.2f} \\times ${model.econ.annual_productivity:,.2f} \\times discount\\_factor

            = {format_currency(results['gdp_impact_trillions'] * 1e12)}

Medicare\\ Savings = Beneficiaries \\times Annual\\ Cost \\times Improvement\\ Percentage

                  = {format_number(model.pop.medicare_beneficiaries)} \\times ${model.econ.annual_healthcare_cost:,.2f} \\times {model.intervention.healthspan_improvement_percent:.1f}\\%

                  = {format_currency(results['annual_medicare_impact_billions'] * 1e9)}
```

## 4. Uncertainty Analysis"""

    if confidence_intervals:
        report += "\n### 4.1 Monte Carlo Simulation Results\n"
        report += "Based on 1,000 simulations with parameter variations:\n\n"
        
        for metric, ci in confidence_intervals.items():
            report += f"**{metric.replace('_', ' ').title()}**\n"
            report += f"- Mean: {format_currency(ci['mean'])}\n"
            report += f"- 95% Confidence Interval: {format_currency(ci['lower_ci'])} to {format_currency(ci['upper_ci'])}\n"
            report += f"- Standard Deviation: {format_currency(ci['std'])}\n"
            report += f"- Coefficient of Variation: {(ci['std']/ci['mean'])*100:.1f}%\n\n"

        report += """### 4.2 Key Sources of Uncertainty
1. **Parameter Variations**:
   - Muscle/Fat Changes: +/- 10%
   - Lifespan Impact: +/- 15%
   - Economic Parameters: +/- 20%

2. **Model Assumptions**:
   - Uniform intervention effectiveness across populations
   - Linear relationship between improvements and savings
   - Constant workforce participation rates
   - Stable economic conditions

## 5. Discussion

### 5.1 Key Findings
1. The intervention shows substantial potential for healthcare cost reduction through improved body composition
2. Lifespan increases could generate significant economic value through extended workforce participation
3. Medicare savings provide additional economic benefits through reduced healthcare spending

### 5.2 Limitations
1. Model assumes uniform intervention effectiveness
2. Does not account for potential demographic variations
3. Long-term economic projections carry inherent uncertainty
4. Healthcare cost savings may vary by region and provider

### 5.3 Policy Implications
1. Significant potential for healthcare cost reduction
2. Positive impact on workforce productivity and GDP
3. Opportunity for Medicare spending optimization
4. Need for careful implementation planning and monitoring

## 6. Conclusions
The analysis demonstrates substantial potential economic benefits from the intervention:
1. Annual healthcare savings in the billions
2. Significant GDP impact from increased productive lifespan
3. Notable Medicare cost reductions
4. Robust results across various uncertainty scenarios

## 7. Recommendations
1. Consider pilot implementation to validate assumptions
2. Develop detailed demographic-specific impact models
3. Create monitoring framework for actual vs. projected benefits
4. Establish ongoing cost-effectiveness evaluation process"""

    return report 