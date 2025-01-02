#!/usr/bin/env python3
"""Generate economic impact report for interventions."""

import importlib.util
from pathlib import Path

from src.models.base_model import (
    BaseImpactModel,
    BasePopulationParams,
    BaseEconomicParams,
    BaseInterventionParams
)
from src.utils.reporting import generate_report
from config.global_parameters import config as global_config

def load_python_config(path: str) -> object:
    """Load configuration from Python file."""
    spec = importlib.util.spec_from_file_location("config", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.config

def main():
    """Main entry point."""
    # Process each intervention config
    for config_file in Path('config/interventions').glob('*.py'):
        if config_file.name == '__init__.py':
            continue
            
        intervention_config = load_python_config(str(config_file))
        
        # Create model parameters
        pop_params = BasePopulationParams(
            total_population=global_config.population.total,
            target_population=global_config.population.target,
            medicare_beneficiaries=global_config.population.medicare_beneficiaries,
            workforce_fraction=global_config.population.workforce_fraction
        )
        
        econ_params = BaseEconomicParams(
            annual_healthcare_cost=global_config.economics.annual_healthcare_cost,
            annual_productivity=global_config.economics.annual_productivity,
            discount_rate=global_config.economics.discount_rate
        )
        
        intervention_params = BaseInterventionParams.from_config(
            intervention_config.model_dump(),
            global_config.model_dump()
        )
        
        # Create and validate model
        model = BaseImpactModel(pop_params, econ_params, intervention_params)
        
        # Generate report
        report = model.generate_full_report(global_config.model_dump())
        report_path = generate_report(intervention_config.model_dump(), model, report, global_config.model_dump())
        print(f"Generated report: {report_path}")

if __name__ == '__main__':
    main() 