#!/usr/bin/env python3
"""
Generate economic impact reports for interventions.
"""

import os
from pathlib import Path
from datetime import datetime

from models.follistatin_model import (
    FollistatinImpactModel,
    FollistatinParams,
    BasePopulationParams,
    BaseEconomicParams
)
from utils.report_generator import generate_intervention_report
from config_loader import load_base_parameters, load_interventions

def get_report_filename(intervention_name: str, params: dict) -> str:
    """Generate a consistent filename based on model parameters."""
    return (
        f"{intervention_name.lower()}"
        f"_m{abs(params['physical']['muscle_mass_change']):.1f}lb"
        f"_f{abs(params['physical']['fat_mass_change']):.1f}lb"
        f"_l{params['longevity']['lifespan_increase']:.1f}pct.md"
    )

def main():
    """Generate reports for intervention analysis."""
    
    # Load configurations
    base_params = load_base_parameters()
    interventions = load_interventions()
    
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
    
    # Generate reports for each intervention
    for intervention_name, intervention_config in interventions.items():
        print(f"\nProcessing {intervention_name} intervention...")
        
        # Create intervention-specific parameters
        intervention_params = FollistatinParams(
            muscle_gain_lb=abs(intervention_config['default_effects']['physical']['muscle_mass_change']),
            fat_loss_lb=abs(intervention_config['default_effects']['physical']['fat_mass_change']),
            lifespan_increase_years=base_params['health_baselines']['average_lifespan'] * 
                                  (intervention_config['default_effects']['longevity']['lifespan_increase'] / 100.0),
            healthspan_improvement_percent=intervention_config['impact_modifiers']['health_quality'] * 100,
            savings_per_lb=10.0  # Could be added to intervention config
        )
        
        # Create model
        model = FollistatinImpactModel(pop_params, econ_params, intervention_params)
        
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
        
        report = generate_intervention_report(
            model,
            title=f"Economic Impact Analysis of {intervention_config['name']}",
            description=description.strip(),
            include_monte_carlo=True
        )
        
        # Create reports directory if it doesn't exist
        reports_dir = Path("reports/generated")
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Save report with parameter-based filename
        report_path = reports_dir / get_report_filename(intervention_name, intervention_config['default_effects'])
        
        with open(report_path, "w") as f:
            f.write(report)
        
        print(f"Report generated: {report_path}")
        print("\nReport Preview:\n")
        print(report[:500] + "...\n")

if __name__ == "__main__":
    main() 