"""Main report generator module."""

from datetime import datetime
from pathlib import Path
from typing import TextIO, Dict

from src.models.base_model import (
    BaseImpactModel,
    BaseInterventionParams
)
from .writers import (
    write_executive_summary,
    write_study_design,
    write_intervention_analysis,
    write_economic_calculations,
    write_population_impact,
    write_uncertainty_analysis,
    write_conclusions
)

def get_report_filename(intervention_name: str, params: BaseInterventionParams) -> str:
    """Generate report filename based on intervention parameters."""
    clean_name = intervention_name.lower().replace(" ", "_")
    muscle_change = params.physical.muscle_mass_change_lb if params.physical else 0.0
    fat_change = params.physical.fat_mass_change_lb if params.physical else 0.0
    return (
        f"{clean_name}_"
        f"m{muscle_change:+.1f}lb_"
        f"f{fat_change:+.1f}lb_"
        f"l{params.lifespan_increase_years:.2f}y_"
        f"h{params.longevity.healthspan_improvement_percent:.1f}pct.md"
    )

def generate_report(
    intervention_config: dict,
    model: BaseImpactModel,
    report: dict,
    base_config: dict,
    output_dir: Path = Path('reports/generated')
) -> Path:
    """Generate a complete economic impact report.
    
    Args:
        intervention_config: Configuration for the intervention
        model: The impact model instance
        report: Generated report data
        base_config: Base configuration parameters
        output_dir: Directory to save the report
        
    Returns:
        Path to the generated report file
    """
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    report_file = get_report_filename(intervention_config['name'], model.intervention)
    report_path = output_dir / report_file
    
    # Generate report
    with open(report_path, 'w') as f:
        # Title
        f.write(f"# Impact Analysis: {intervention_config['name']}\n\n")

        # Write each section
        write_executive_summary(f, intervention_config, report)
        write_study_design(f)
        write_intervention_analysis(f, model)
        write_economic_calculations(f, model, base_config)
        write_population_impact(f, model)
        write_uncertainty_analysis(f)
        write_conclusions(f, model, report)
    
    return report_path 