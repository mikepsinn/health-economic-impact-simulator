"""Report section writers."""

from datetime import datetime
from typing import TextIO, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.base_model import BaseImpactModel
    from src.models.report import Report

from .formatters import format_currency, format_percentage, format_number, format_equation

def write_executive_summary(
    f: TextIO,
    intervention_config: Dict[str, Any],
    report: 'Report'
) -> None:
    """Write executive summary section."""
    f.write("## Executive Summary\n\n")
    f.write(f"{intervention_config['description']}\n\n")
    f.write("### Key Findings\n")
    f.write(f"- Annual Healthcare System Savings: {format_currency(report.metrics.annual_healthcare_savings)}\n")
    f.write(f"- Total GDP Impact: {format_currency(report.metrics.total_gdp_impact)}\n")
    f.write(f"- Annual Medicare Cost Reduction: {format_currency(report.metrics.annual_medicare_savings)}\n")
    f.write(f"- Quality-Adjusted Life Years Gained: {format_number(report.metrics.total_qalys)}\n\n")

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
    model: 'BaseImpactModel'
) -> None:
    """Write intervention analysis section."""
    f.write("## Intervention Analysis\n\n")
    
    # Physical Impact
    if model.intervention.physical:
        f.write("### Physical Impact Pathway\n")
        model.physical_calculator.write_calculations(f, model.intervention.physical.dict(), model.physical_results)
        f.write("\n")
    
    # Cognitive Impact
    if model.intervention.cognitive:
        f.write("### Cognitive Impact Pathway\n")
        model.cognitive_calculator.write_calculations(f, model.intervention.cognitive.dict(), model.cognitive_results)
        f.write("\n")
    
    # Kidney Impact
    if model.intervention.kidney:
        f.write("### Kidney Function Impact Pathway\n")
        model.kidney_calculator.write_calculations(f, model.intervention.kidney.dict(), model.kidney_results)
        f.write("\n")
    
    # Healthcare Impact
    f.write("### Healthcare Utilization Impact\n")
    model.healthcare_calculator.write_calculations(f, model.intervention.healthcare.dict(), model.healthcare_results)
    f.write("\n")

def write_economic_calculations(
    f: TextIO,
    model: 'BaseImpactModel',
    report: 'Report'
) -> None:
    """Write economic calculations section."""
    f.write("## Economic Impact Calculations\n\n")
    
    # Total Healthcare System Savings
    f.write("### Total Healthcare System Savings\n")
    f.write("Sum of savings from all impact pathways:\n\n")
    equation = "Total Savings = Physical_Savings + Hospital_Savings + Medicare_Savings"
    f.write(format_equation(equation))
    f.write(f"\nAnnual healthcare system savings: {format_currency(report.metrics.annual_healthcare_savings)}\n\n")
    
    # Total GDP Impact
    f.write("### Total GDP Impact\n")
    f.write("Economic gains from improved health and productivity:\n\n")
    equation = "GDP Impact = Cognitive_Impact + Longevity_Impact"
    f.write(format_equation(equation))
    f.write(f"\nTotal GDP impact: {format_currency(report.metrics.total_gdp_impact)}\n\n")
    
    # Total QALYs
    f.write("### Quality-Adjusted Life Years\n")
    f.write("Total health improvements across all pathways:\n\n")
    equation = "Total QALYs = Physical_QALYs + Cognitive_QALYs + Kidney_QALYs + Healthcare_QALYs"
    f.write(format_equation(equation))
    f.write(f"\nTotal QALYs gained: {format_number(report.metrics.total_qalys)}\n\n")

def write_population_impact(
    f: TextIO,
    model: 'BaseImpactModel'
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
    model: 'BaseImpactModel',
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