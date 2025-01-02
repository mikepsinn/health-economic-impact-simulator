#!/usr/bin/env python3
"""Generate economic impact report for interventions."""

import yaml
from pathlib import Path
from datetime import datetime

from src.models.base_model import (
    BaseImpactModel,
    BasePopulationParams,
    BaseEconomicParams,
    BaseInterventionParams
)

def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_report_filename(params: BaseInterventionParams) -> str:
    """Generate report filename based on intervention parameters."""
    return (
        f"impact_analysis_"
        f"m{params.muscle_gain_lb:.1f}lb_"
        f"f{params.fat_loss_lb:.1f}lb_"
        f"l{params.lifespan_increase_years:.2f}y_"
        f"h{params.healthspan_improvement_percent:.1f}pct.md"
    )

def main():
    """Main entry point."""
    # Load configurations
    base_config = load_config('config/base_parameters.yml')
    
    # Create output directory if it doesn't exist
    Path('reports/generated').mkdir(parents=True, exist_ok=True)
    
    # Process each intervention config
    for config_file in Path('config/interventions').glob('*.yml'):
        if config_file.name == 'template.yml':
            continue
            
        intervention_config = load_config(str(config_file))
        
        # Create model parameters
        pop_params = BasePopulationParams(
            total_population=base_config['population']['total'],
            target_population=base_config['population']['target'],
            medicare_beneficiaries=base_config['population']['medicare_beneficiaries'],
            workforce_fraction=base_config['population']['workforce_fraction']
        )
        
        econ_params = BaseEconomicParams(
            annual_healthcare_cost=base_config['economics']['annual_healthcare_cost'],
            annual_productivity=base_config['economics']['annual_productivity'],
            discount_rate=base_config['economics']['discount_rate']
        )
        
        intervention_params = BaseInterventionParams.from_config(
            intervention_config,
            base_config
        )
        
        # Create and validate model
        model = BaseImpactModel(pop_params, econ_params, intervention_params)
        model.validate_assumptions()
        
        # Generate report
        report = model.generate_full_report()
        
        # Save report
        report_file = get_report_filename(intervention_params)
        report_path = Path('reports/generated') / report_file
        
        with open(report_path, 'w') as f:
            f.write(f"# Economic Impact Analysis: {intervention_config['name']}\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Summary\n\n")
            f.write(f"- Annual Healthcare Savings: ${report['annual_healthcare_savings_billions']:.2f}B\n")
            f.write(f"- GDP Impact: ${report['gdp_impact_trillions']:.2f}T\n")
            f.write(f"- Annual Medicare Savings: ${report['annual_medicare_impact_billions']:.2f}B\n")
            f.write(f"- QALYs Gained: {report['qalys_gained']:,.0f}\n")
            
            f.write("\n## Parameters\n\n")
            f.write("### Intervention Effects\n")
            f.write(f"- Muscle Mass Change: {intervention_params.muscle_gain_lb:.1f} lb\n")
            f.write(f"- Fat Mass Change: {intervention_params.fat_loss_lb:.1f} lb\n")
            f.write(f"- Lifespan Increase: {intervention_params.lifespan_increase_years:.2f} years\n")
            f.write(f"- Health Improvement: {intervention_params.healthspan_improvement_percent:.1f}%\n")
            f.write(f"- Hospital Visit Reduction: {intervention_params.hospital_visit_reduction_percent:.1f}%\n")
            
            f.write("\n### Population Parameters\n")
            f.write(f"- Total Population: {pop_params.total_population:,}\n")
            f.write(f"- Target Population: {pop_params.target_population:,}\n")
            f.write(f"- Medicare Beneficiaries: {pop_params.medicare_beneficiaries:,}\n")
            f.write(f"- Workforce Fraction: {pop_params.workforce_fraction:.1%}\n")
            
            f.write("\n### Economic Parameters\n")
            f.write(f"- Annual Healthcare Cost: ${econ_params.annual_healthcare_cost:,.2f}\n")
            f.write(f"- Annual Productivity: ${econ_params.annual_productivity:,.2f}\n")
            f.write(f"- Discount Rate: {econ_params.discount_rate:.1%}\n")
        
        print(f"Generated report: {report_path}")

if __name__ == '__main__':
    main() 