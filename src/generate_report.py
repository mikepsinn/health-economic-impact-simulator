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
from src.models.report import Report
from src.utils.reporting import generate_report
from src.utils.validation import validate_economic_impacts, format_validation_messages
from config.global_parameters import config as global_config

def load_python_config(path: str) -> object:
    """Load configuration from Python file."""
    print(f"Loading config from {path}")
    spec = importlib.util.spec_from_file_location("config", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.config

def main():
    """Main entry point."""
    # Process each intervention config
    config_files = list(Path('config/interventions').glob('*.py'))
    print(f"Found {len(config_files)} intervention configs")
    
    for config_file in config_files:
        if config_file.name == '__init__.py':
            continue
            
        print(f"\nProcessing {config_file.name}")
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
        
        # Generate report with validated data model
        report = model.generate_full_report(global_config.model_dump())
        
        # Validate economic impacts
        validation_messages = validate_economic_impacts(
            healthcare_savings=report.metrics.annual_healthcare_savings,
            gdp_impact=report.metrics.total_gdp_impact,
            medicare_savings=report.metrics.annual_medicare_savings,
            qalys=report.metrics.total_qalys,
            population=pop_params.total_population,
            base_healthcare_cost=econ_params.annual_healthcare_cost,
            base_gdp=25e12,  # US GDP ~$25T
            base_medicare=1e12,  # Medicare spending ~$1T
        )
        
        # Add validation warnings to report
        report.validation_warnings = format_validation_messages(validation_messages)
        
        # Generate markdown report
        report_path = generate_report(intervention_config.model_dump(), model, report, global_config.model_dump())
        print(f"Generated report: {report_path}")
        
        if validation_messages:
            print("⚠️ Report contains validation warnings - some calculations exceed realistic bounds")

if __name__ == '__main__':
    main() 