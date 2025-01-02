"""Report generation utilities."""

from pathlib import Path
from typing import Dict

from src.models.base_model import BaseImpactModel
from src.models.report import Report
from .formatters import format_currency, format_number

def format_report_filename(config: Dict, model: BaseImpactModel) -> str:
    """Format report filename from key parameters."""
    # Extract key parameters for filename
    muscle = model.intervention.physical.muscle_mass_change_lb if model.intervention.physical else 0
    fat = model.intervention.physical.fat_mass_change_lb if model.intervention.physical else 0
    lifespan = model.intervention.longevity.lifespan_increase_years
    health = model.intervention.longevity.healthspan_improvement_percent
    
    # Format filename with key metrics
    return (
        f"{config['name'].lower()}_"
        f"m{muscle:+.1f}lb_"
        f"f{fat:+.1f}lb_"
        f"l{lifespan:.2f}y_"
        f"h{health:.1f}pct.md"
    )

def generate_report(config: Dict, model: BaseImpactModel, report: Report, base_params: Dict) -> str:
    """Generate markdown report from model results."""
    # Format filename from key parameters
    filename = format_report_filename(config, model)
    
    # Generate report content
    content = f"""# Impact Analysis: {config['name']}

## Executive Summary

{config['description']}

### Key Findings
- Annual Healthcare System Savings: {format_currency(report.metrics.annual_healthcare_savings)}
- Total GDP Impact: {format_currency(report.metrics.total_gdp_impact)}
- Annual Medicare Cost Reduction: {format_currency(report.metrics.annual_medicare_savings)}
- Quality-Adjusted Life Years Gained: {format_number(report.metrics.total_qalys)}

{report.validation_warnings}

## Study Design

### Methodology
This analysis employs a comprehensive economic model that integrates multiple impact pathways:
1. Direct healthcare cost reductions from improved health outcomes
2. Economic gains from increased productive lifespan
3. Medicare savings from reduced healthcare utilization
4. Quality of life improvements measured in QALYs

### Data Sources
The model uses the following primary data sources:
- US Census Bureau population statistics
- Medicare cost and utilization data
- Bureau of Labor Statistics workforce data
- CDC health outcome statistics

## Intervention Analysis
"""
    
    # Add intervention-specific sections
    content += generate_intervention_sections(config, model)
    
    # Write report to file
    report_dir = Path('reports/generated')
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / filename
    report_path.write_text(content)
    
    return str(report_path)

def generate_intervention_sections(config: Dict, model: BaseImpactModel) -> str:
    """Generate intervention-specific sections of the report."""
    content = ""
    
    # Physical Impact
    if model.intervention.physical:
        content += "### Physical Impact Pathway\n"
        content += f"- Muscle Mass Change: {model.intervention.physical.muscle_mass_change_lb:+.1f} lb\n"
        content += f"- Fat Mass Change: {model.intervention.physical.fat_mass_change_lb:+.1f} lb\n"
        content += "These changes affect:\n"
        content += "1. Healthcare utilization through improved mobility and reduced fall risk\n"
        content += "2. Quality of life through enhanced physical capability\n"
        content += "3. Healthcare costs through metabolic health improvements\n\n"
    
    # Cognitive Impact
    if model.intervention.cognitive:
        content += "### Cognitive Impact Pathway\n"
        content += f"- IQ Increase: +{model.intervention.cognitive.iq_increase:.1f} points\n"
        content += f"- Alzheimer's Progression Reduction: {model.intervention.cognitive.alzheimers_reduction:.1f}%\n"
        content += "These improvements lead to:\n"
        content += "1. Enhanced workforce productivity\n"
        content += "2. Reduced cognitive decline costs\n"
        content += "3. Improved quality of life\n\n"
    
    # Kidney Function Impact
    if model.intervention.kidney:
        content += "### Kidney Function Impact Pathway\n"
        content += f"- eGFR Improvement: +{model.intervention.kidney.egfr_improvement:.1f} mL/min/1.73m²\n"
        content += f"- CKD Progression Reduction: {model.intervention.kidney.ckd_progression_reduction:.1f}%\n"
        content += "These improvements result in:\n"
        content += "1. Reduced Medicare costs\n"
        content += "2. Improved quality of life\n"
        content += "3. Extended healthspan\n\n"
    
    # Longevity Impact
    content += "### Longevity Impact Pathway\n"
    content += f"- Lifespan Increase: {model.intervention.longevity.lifespan_increase_years:.2f} years\n"
    content += f"- Health Quality Improvement: {model.intervention.longevity.healthspan_improvement_percent:.1f}%\n"
    content += "These improvements contribute to:\n"
    content += "1. Extended productive years\n"
    content += "2. Increased lifetime earnings\n"
    content += "3. Enhanced quality of life\n\n"
    
    return content 