#!/usr/bin/env python3
"""
Generate economic impact reports for interventions.
"""

import os
from pathlib import Path
from datetime import datetime
import importlib
import sys

from config_loader import load_base_parameters, load_interventions
from models.base_model import BasePopulationParams, BaseEconomicParams

def get_report_filename(intervention_name: str, params: dict) -> str:
    """Generate a consistent filename based on model parameters."""
    effects = params['default_effects']
    return (
        f"{intervention_name.lower()}"
        f"_m{abs(effects['physical']['muscle_mass_change']):.1f}lb"
        f"_f{abs(effects['physical']['fat_mass_change']):.1f}lb"
        f"_l{effects['longevity']['lifespan_increase']:.1f}pct.md"
    )

def get_model_class(intervention_name: str):
    """Dynamically import and return the model class for an intervention."""
    try:
        module = importlib.import_module(f"models.{intervention_name.lower()}_model")
        model_class = getattr(module, f"{intervention_name.capitalize()}ImpactModel")
        param_class = getattr(module, f"{intervention_name.capitalize()}Params")
        return model_class, param_class
    except (ImportError, AttributeError) as e:
        print(f"Warning: No specific model found for {intervention_name}. Error: {e}")
        print("Using base model instead.")
        from models.base_model import BaseImpactModel, BaseInterventionParams
        return BaseImpactModel, BaseInterventionParams

def create_intervention_params(param_class, intervention_config, base_params):
    """Create intervention parameters from config."""
    effects = intervention_config['default_effects']
    modifiers = intervention_config['impact_modifiers']
    
    return param_class(
        muscle_gain_lb=abs(effects['physical']['muscle_mass_change']),
        fat_loss_lb=abs(effects['physical']['fat_mass_change']),
        lifespan_increase_years=base_params['health_baselines']['average_lifespan'] * 
                              (effects['longevity']['lifespan_increase'] / 100.0),
        healthspan_improvement_percent=modifiers['health_quality'] * 100,
        savings_per_lb=10.0  # Could be added to intervention config
    )

def main():
    """Generate reports for all configured interventions."""
    print("\nHealth Economic Impact Simulator - Report Generation")
    print("=" * 50)
    
    # Load configurations
    base_params = load_base_parameters()
    interventions = load_interventions()
    
    if not interventions:
        print("\nError: No intervention configurations found.")
        print("Please add intervention config files to config/interventions/")
        sys.exit(1)
    
    # Initialize base parameters
    pop_params = BasePopulationParams(
        total_population=base_params['population']['total_us'],
        target_population=base_params['population']['adult'],
        medicare_beneficiaries=int(base_params['population']['total_us'] * 
                                 base_params['health_baselines']['medicare_enrollment_rate']),
        workforce_fraction=0.5  # Could be added to base_parameters.yml
    )
    
    econ_params = BaseEconomicParams(
        annual_healthcare_cost=base_params['economics']['medicare_per_capita'],
        annual_productivity=base_params['economics']['gdp_per_capita'],
        discount_rate=0.03  # Could be added to base_parameters.yml
    )
    
    # Create reports directory
    reports_dir = Path("reports/generated")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate reports for each intervention
    print(f"\nFound {len(interventions)} intervention configurations.")
    
    for intervention_name, intervention_config in interventions.items():
        print(f"\nProcessing {intervention_name} intervention...")
        
        try:
            # Get appropriate model class
            model_class, param_class = get_model_class(intervention_name)
            
            # Create intervention-specific parameters
            intervention_params = create_intervention_params(
                param_class, intervention_config, base_params
            )
            
            # Create model
            model = model_class(pop_params, econ_params, intervention_params)
            
            # Generate report
            description = f"""
This report analyzes the economic and health impacts of {intervention_config['name']}: {intervention_config['description']}.

Key effects analyzed:
1. Body composition changes: {intervention_config['default_effects']['physical']['muscle_mass_change']} lb muscle, 
   {intervention_config['default_effects']['physical']['fat_mass_change']} lb fat
2. Longevity impact: {intervention_config['default_effects']['longevity']['lifespan_increase']}% lifespan increase
3. Healthcare utilization: {intervention_config['default_effects']['healthcare']['hospital_visit_reduction']}% reduction in hospital visits

The analysis includes direct healthcare savings, GDP impact from increased productive years, 
and Medicare spending reductions from improved health outcomes.
"""
            
            from utils.report_generator import generate_intervention_report
            report = generate_intervention_report(
                model,
                title=f"Economic Impact Analysis of {intervention_config['name']}",
                description=description.strip(),
                include_monte_carlo=True
            )
            
            # Save report with parameter-based filename
            report_path = reports_dir / get_report_filename(intervention_name, intervention_config)
            
            with open(report_path, "w") as f:
                f.write(report)
            
            print(f"Report generated: {report_path}")
            print("\nReport Preview:\n")
            print(report[:500] + "...\n")
            
        except Exception as e:
            print(f"Error processing {intervention_name}: {str(e)}")
            print("Continuing with next intervention...")
            continue
    
    print("\nReport generation complete.")
    print("=" * 50)

if __name__ == "__main__":
    main() 