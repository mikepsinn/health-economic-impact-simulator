#!/usr/bin/env python3
"""Report generation script."""

import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any

from src.models.base_model import BaseImpactModel
from src.models.parameters import (
    BasePopulationParams,
    BaseEconomicParams,
    BaseInterventionParams
)
from src.utils.reporting import generate_report

def load_python_config(path: Path) -> Dict[str, Any]:
    """Load configuration from Python file."""
    print(f"Loading config from {path}")
    spec = importlib.util.spec_from_file_location("config", path)
    if not spec or not spec.loader:
        raise ImportError(f"Could not load {path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules["config"] = module
    spec.loader.exec_module(module)
    
    return module.config.model_dump()

def main() -> None:
    """Generate reports for all interventions."""
    # Load base configuration
    base_config_path = Path("config/global_parameters.py")
    base_config = load_python_config(base_config_path)
    
    # Find all intervention configs
    config_dir = Path("config/interventions")
    config_files = list(config_dir.glob("*.py"))
    print(f"\nFound {len(config_files)} intervention configs\n")
    
    # Process each intervention
    for config_path in config_files:
        print(f"Processing {config_path.name}")
        
        # Load intervention config
        intervention_config = load_python_config(config_path)
        
        # Create model parameters
        intervention_params = BaseInterventionParams.from_config(
            intervention_config=intervention_config,
            base_config=base_config
        )
        
        population_params = BasePopulationParams(**base_config['population'])
        economic_params = BaseEconomicParams(**base_config['economics'])
        
        # Create and run model
        model = BaseImpactModel(
            population_params=population_params,
            economic_params=economic_params,
            intervention_params=intervention_params
        )
        
        # Generate report
        report = model.generate_full_report(base_config)
        
        # Check for validation warnings
        if report.validation_warnings:
            print("⚠️ Report contains validation warnings - some calculations exceed realistic bounds")
        
        # Write report to file
        report_path = generate_report(intervention_config, model, report, base_config)
        print(f"Generated report: {report_path}\n")

if __name__ == "__main__":
    main() 