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

def main():
    """Generate reports for intervention analysis."""
    
    # Initialize model parameters
    pop_params = BasePopulationParams(
        total_population=332_000_000,
        target_population=332_000_000,  # Assuming universal treatment
        medicare_beneficiaries=64_000_000,
        workforce_fraction=0.5
    )
    
    econ_params = BaseEconomicParams(
        annual_healthcare_cost=14_000,  # Average Medicare cost per beneficiary
        annual_productivity=70_000,     # Average annual productivity per worker
        discount_rate=0.03             # 3% annual discount rate
    )
    
    intervention_params = FollistatinParams(
        muscle_gain_lb=2.0,
        fat_loss_lb=2.0,
        lifespan_increase_years=1.925,  # 2.5% of 77 years
        healthspan_improvement_percent=5.0,
        savings_per_lb=10.0
    )
    
    # Create model
    model = FollistatinImpactModel(pop_params, econ_params, intervention_params)
    
    # Generate report
    description = """
This report analyzes two key questions about potential interventions:

1. What is the cumulative benefit if an intervention increases muscle mass by 2 lb 
   and decreases fat mass by 2 lb over the entire US population?

2. What are the GDP and Medicare spending impacts if an intervention increases 
   lifespan by 2.5%?

The analysis includes direct healthcare savings, GDP impact from increased productive 
years, and Medicare spending reductions from improved health outcomes.
"""
    
    report = generate_intervention_report(
        model,
        title="Economic Impact Analysis of Health Interventions",
        description=description.strip(),
        include_monte_carlo=True
    )
    
    # Create reports directory if it doesn't exist
    reports_dir = Path("reports/generated")
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"economic_impact_report_{timestamp}.md"
    
    with open(report_path, "w") as f:
        f.write(report)
    
    print(f"Report generated: {report_path}")
    print("\nReport Preview:\n")
    print(report[:500] + "...\n")

if __name__ == "__main__":
    main() 