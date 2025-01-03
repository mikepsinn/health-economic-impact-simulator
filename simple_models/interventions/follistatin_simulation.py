from outcomes.muscle_mass_model import MuscleMassInterventionModel
from outcomes.lifespan_model import LifespanImpactModel, generate_report as generate_lifespan_report
import os
from datetime import datetime

def generate_follistatin_report(muscle_mass_lbs=2.0, lifespan_increase_pct=2.5, population_size=100000):
    """Generate a comprehensive report on follistatin's impact combining muscle mass and lifespan effects"""
    
    # Initialize models
    muscle_model = MuscleMassInterventionModel(muscle_mass_lbs)
    lifespan_model = LifespanImpactModel()
    
    # Get individual reports
    muscle_results = muscle_model.generate_report(population_size)
    lifespan_results = generate_lifespan_report(lifespan_increase_pct, population_size)
    
    # Create combined report
    report = f"""
# Follistatin Intervention Analysis Report
Generated on: {datetime.now().strftime('%Y-%m-%d')}

## Study Parameters
- Target Population: {population_size:,} individuals
- Muscle Mass Increase: {muscle_mass_lbs} lbs per person
- Lifespan Increase: {lifespan_increase_pct}%

## Muscle Mass Impact Analysis
{muscle_results}

## Lifespan Impact Analysis
{lifespan_results}
"""
    return report

def save_follistatin_report(muscle_mass_lbs=2.0, lifespan_increase_pct=2.5, population_size=334000000, output_path='.'):
    """Save the follistatin report to a markdown file"""
    # Create output directory if it doesn't exist
    if output_path != '.':
        os.makedirs(output_path, exist_ok=True)
    
    # Generate filename with all parameters
    filename = f'follistatin_m+{muscle_mass_lbs}lb_l{lifespan_increase_pct}pct_p{population_size}.md'
    filepath = os.path.join(output_path, filename)
    
    # Generate and save the report
    report_content = generate_follistatin_report(muscle_mass_lbs, lifespan_increase_pct, population_size)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return filepath

if __name__ == "__main__":
    # Generate and save the report with default parameters
    report_path = save_follistatin_report()
    print(f"Report saved to: {report_path}") 