"""Report generation utilities."""

from pathlib import Path
from typing import Dict

from src.models.base_model import BaseImpactModel
from src.models.parameters import BaseInterventionParams
from src.models.report import Report
from .writers import (
    write_executive_summary,
    write_study_design,
    write_intervention_analysis
)

def get_report_filename(name: str, params: BaseInterventionParams) -> str:
    """Format report filename from key parameters."""
    # Extract key parameters for filename
    muscle = params.physical.muscle_mass_change_lb if params.physical else 0
    fat = params.physical.fat_mass_change_lb if params.physical else 0
    lifespan = params.longevity.lifespan_increase_years
    health = params.longevity.healthspan_improvement_percent
    
    # Format filename with key metrics
    return (
        f"{name.lower()}_"
        f"m{muscle:+.1f}lb_"
        f"f{fat:+.1f}lb_"
        f"l{lifespan:.2f}y_"
        f"h{health:.1f}pct.md"
    )

def generate_report(config: Dict, model: BaseImpactModel, report: Report, base_params: Dict) -> str:
    """Generate markdown report from model results."""
    # Format filename
    report_file = get_report_filename(config['name'], model.intervention)
    
    # Create report directory
    report_dir = Path('reports/generated')
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / report_file
    
    # Generate report content
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# Impact Analysis: {config['name']}\n\n")
        
        write_executive_summary(f, config, report)
        write_study_design(f)
        write_intervention_analysis(f, model)
        
        # Add validation warnings if any
        if report.validation_warnings:
            f.write(report.validation_warnings)
    
    return str(report_path) 