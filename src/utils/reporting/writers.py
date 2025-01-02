"""Report section writers."""

from datetime import datetime
from typing import TextIO, Dict

from src.models.base_model import BaseImpactModel
from .formatters import format_currency, format_percentage, format_number, format_equation

def write_executive_summary(
    f: TextIO,
    intervention_config: dict,
    report: dict
) -> None:
    """Write executive summary section."""
    f.write("## Executive Summary\n\n")
    f.write(f"{intervention_config['description']}\n\n")
    f.write("### Key Findings\n")
    f.write(f"- Annual Healthcare System Savings: {format_currency(report['annual_healthcare_savings_billions']*1e9)}\n")
    f.write(f"- Total GDP Impact: {format_currency(report['gdp_impact_trillions']*1e12)}\n")
    f.write(f"- Annual Medicare Cost Reduction: {format_currency(report['annual_medicare_impact_billions']*1e9)}\n")
    f.write(f"- Quality-Adjusted Life Years Gained: {format_number(report['qalys_gained'])}\n\n")

def write_study_design(f: TextIO) -> None:
    """Write study design section."""
    f.write("## Study Design\n\n")
    f.write("### Methodology\n")
    f.write("This analysis employs a comprehensive economic model that integrates multiple impact pathways:\n")
    f.write("1. Direct healthcare cost reductions from improved health outcomes\n")
    f.write("2. Economic gains from increased productive lifespan\n")
    f.write("3. Medicare savings from reduced healthcare utilization\n")
    f.write("4. Quality of life improvements measured in QALYs\n\n")
    
    f.write("### Data Sources\n")
    f.write("The model uses the following primary data sources:\n")
    f.write("- US Census Bureau population statistics\n")
    f.write("- Medicare cost and utilization data\n")
    f.write("- Bureau of Labor Statistics workforce data\n")
    f.write("- CDC health outcome statistics\n\n")

def write_intervention_analysis(
    f: TextIO,
    model: BaseImpactModel
) -> None:
    """Write intervention analysis section."""
    f.write("## Intervention Analysis\n\n")
    
    # Physical Impact
    if model.intervention.physical:
        f.write("### Physical Impact Pathway\n")
        f.write(f"- Muscle Mass Change: {model.intervention.physical.muscle_mass_change_lb:+.1f} lb\n")
        f.write(f"- Fat Mass Change: {model.intervention.physical.fat_mass_change_lb:+.1f} lb\n")
        f.write("These changes affect:\n")
        f.write("1. Healthcare utilization through improved mobility and reduced fall risk\n")
        f.write("2. Quality of life through enhanced physical capability\n")
        f.write("3. Healthcare costs through metabolic health improvements\n\n")
    
    # Cognitive Impact
    if model.intervention.cognitive:
        f.write("### Cognitive Impact Pathway\n")
        f.write(f"- IQ Increase: {model.intervention.cognitive.iq_increase:+.1f} points\n")
        f.write(f"- Alzheimer's Progression Reduction: {model.intervention.cognitive.alzheimers_reduction:.1f}%\n")
        f.write("These improvements lead to:\n")
        f.write("1. Enhanced workforce productivity\n")
        f.write("2. Reduced cognitive decline costs\n")
        f.write("3. Improved quality of life\n\n")
    
    # Kidney Impact
    if model.intervention.kidney:
        f.write("### Kidney Function Impact Pathway\n")
        f.write(f"- eGFR Improvement: {model.intervention.kidney.egfr_improvement:+.1f} mL/min/1.73m²\n")
        f.write(f"- CKD Progression Reduction: {model.intervention.kidney.ckd_progression_reduction:.1f}%\n")
        f.write("These improvements result in:\n")
        f.write("1. Reduced kidney disease progression\n")
        f.write("2. Lower dialysis and treatment costs\n")
        f.write("3. Enhanced patient wellbeing\n\n")
    
    # Longevity Impact
    f.write("### Longevity Impact Pathway\n")
    f.write(f"- Lifespan Increase: {model.intervention.lifespan_increase_years:.2f} years\n")
    f.write(f"- Health Quality Improvement: {format_percentage(model.intervention.longevity.healthspan_improvement_percent)}\n")
    f.write("These improvements contribute to:\n")
    f.write("1. Extended workforce participation\n")
    f.write("2. Increased lifetime earnings\n")
    f.write("3. Enhanced quality of life\n\n")
    
    # Healthcare System Impact
    f.write("### Healthcare System Impact\n")
    f.write(f"- Hospital Visit Reduction: {format_percentage(model.intervention.healthcare.hospital_visit_reduction_percent)}\n")
    f.write("This leads to:\n")
    f.write("1. Reduced acute care costs\n")
    f.write("2. Lower Medicare spending\n")
    f.write("3. Improved healthcare system efficiency\n\n")

def write_economic_calculations(
    f: TextIO,
    model: BaseImpactModel,
    base_config: dict
) -> None:
    """Write economic calculations section."""
    f.write("## Economic Impact Calculations\n\n")
    
    # Healthcare Savings
    f.write("### Healthcare Savings Calculation\n")
    equation = "Annual Savings = Population * (Muscle_Mass_Change + Fat_Mass_Change) * Savings_per_lb +\n"
    equation += "                Population * Baseline_Visits * Visit_Reduction * Cost_per_Visit"
    f.write(format_equation(equation))
    
    muscle_change = model.intervention.physical.muscle_mass_change_lb if model.intervention.physical else 0.0
    fat_change = model.intervention.physical.fat_mass_change_lb if model.intervention.physical else 0.0
    composition_savings = (
        model.pop.target_population * 
        (muscle_change + fat_change) * 
        model.intervention.healthcare.savings_per_lb
    )
    baseline_visits = model.pop.target_population * base_config['healthcare']['annual_hospital_visits'] / model.pop.total_population
    visit_reduction = baseline_visits * (model.intervention.healthcare.hospital_visit_reduction_percent / 100.0)
    hospital_savings = visit_reduction * model.intervention.healthcare.cost_per_hospital_visit
    
    f.write(f"\nComposition-related savings: {format_currency(composition_savings)}\n")
    f.write(f"Hospital visit reduction savings: {format_currency(hospital_savings)}\n")
    f.write(f"Total annual healthcare savings: {format_currency(composition_savings + hospital_savings)}\n\n")
    
    # GDP Impact
    f.write("### GDP Impact Calculation\n")
    equation = "GDP Impact = Population * Workforce_Fraction * Lifespan_Increase *\n"
    equation += "            Annual_Productivity * (1 / (1 + Discount_Rate)^(Years/2))"
    f.write(format_equation(equation))
    
    working_years = model.intervention.lifespan_increase_years * model.pop.workforce_fraction
    annual_impact = model.pop.target_population * working_years * model.econ.annual_productivity
    discounted_impact = model.apply_discount_rate(annual_impact, working_years / 2)
    
    f.write(f"\nAdditional productive years: {working_years:.2f}\n")
    f.write(f"Annual economic impact: {format_currency(annual_impact)}\n")
    f.write(f"Discounted lifetime impact: {format_currency(discounted_impact)}\n\n")
    
    # Medicare Impact
    f.write("### Medicare Impact Calculation\n")
    equation = "Medicare Savings = Beneficiaries * Annual_Cost * Health_Improvement"
    f.write(format_equation(equation))
    
    medicare_impact = (
        model.pop.medicare_beneficiaries * 
        model.econ.annual_healthcare_cost * 
        (model.intervention.longevity.healthspan_improvement_percent / 100.0)
    )
    f.write(f"\nAnnual Medicare savings: {format_currency(medicare_impact)}\n\n")
    
    # QALY Impact
    f.write("### QALY Calculation\n")
    equation = "QALYs = Population * Lifespan_Increase * (1 + Quality_Improvement)"
    f.write(format_equation(equation))
    
    qalys = model.calculate_qalys()
    f.write(f"\nTotal QALYs gained: {format_number(qalys)}\n\n")

def write_population_impact(
    f: TextIO,
    model: BaseImpactModel
) -> None:
    """Write population impact section."""
    f.write("## Population Impact\n\n")
    f.write("### Target Population\n")
    f.write(f"- Total US Population: {format_number(model.pop.total_population)}\n")
    f.write(f"- Target Population: {format_number(model.pop.target_population)}\n")
    f.write(f"- Medicare Beneficiaries: {format_number(model.pop.medicare_beneficiaries)}\n")
    f.write(f"- Workforce Participation: {format_percentage(model.pop.workforce_fraction*100)}\n\n")
    
    f.write("### Cost Basis\n")
    f.write(f"- Annual Healthcare Cost: {format_currency(model.econ.annual_healthcare_cost)}\n")
    f.write(f"- Annual Productivity: {format_currency(model.econ.annual_productivity)}\n")
    f.write(f"- Discount Rate: {format_percentage(model.econ.discount_rate*100)}\n\n")

def write_uncertainty_analysis(f: TextIO) -> None:
    """Write uncertainty analysis section."""
    f.write("## Uncertainty Analysis\n\n")
    f.write("### Key Assumptions\n")
    f.write("1. Population response follows clinical trial results\n")
    f.write("2. Economic benefits scale linearly with health improvements\n")
    f.write("3. Workforce participation remains stable\n")
    f.write("4. Healthcare costs follow historical trends\n\n")
    
    f.write("### Risk Factors\n")
    f.write("1. Variable individual response to intervention\n")
    f.write("2. Economic condition fluctuations\n")
    f.write("3. Healthcare system changes\n")
    f.write("4. Demographic shifts\n\n")

def write_conclusions(
    f: TextIO,
    model: BaseImpactModel,
    report: dict
) -> None:
    """Write conclusions section."""
    f.write("## Conclusions\n\n")
    total_annual_savings = (report['annual_healthcare_savings_billions'] + 
                          report['annual_medicare_impact_billions']) * 1e9
    per_person_savings = total_annual_savings / model.pop.target_population
    
    f.write("### Economic Viability\n")
    f.write(f"The intervention demonstrates significant economic benefits:\n")
    f.write(f"- Per-person annual savings: {format_currency(per_person_savings)}\n")
    f.write(f"- Total annual system savings: {format_currency(total_annual_savings)}\n")
    f.write(f"- Long-term GDP impact: {format_currency(report['gdp_impact_trillions']*1e12)}\n\n")
    
    f.write("### Healthcare System Impact\n")
    f.write("The intervention would significantly reduce healthcare system burden through:\n")
    f.write("1. Reduced hospitalization rates\n")
    f.write("2. Improved health outcomes\n")
    f.write("3. Extended healthy lifespan\n")
    f.write("4. Enhanced quality of life\n\n")
    
    f.write("### Recommendations\n")
    f.write("Based on this analysis, we recommend:\n")
    f.write("1. Proceeding with intervention implementation\n")
    f.write("2. Establishing monitoring systems for outcome tracking\n")
    f.write("3. Developing scaled deployment strategies\n")
    f.write("4. Creating long-term impact assessment frameworks\n") 