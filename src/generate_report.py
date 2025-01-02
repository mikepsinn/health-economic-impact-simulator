#!/usr/bin/env python3
"""Generate economic impact report for interventions."""

import yaml
from pathlib import Path

from src.models.base_model import (
    BaseImpactModel,
    BasePopulationParams,
    BaseEconomicParams,
    BaseInterventionParams
)
from src.utils.reporting import generate_report

def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    """Main entry point."""
    # Load configurations
    base_config = load_config('config/base_parameters.yml')
    
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
        report_path = generate_report(intervention_config, model, report, base_config)
        print(f"Generated report: {report_path}")

if __name__ == '__main__':
    main() 