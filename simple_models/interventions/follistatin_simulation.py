from outcomes.muscle_mass_model import MuscleMassInterventionModel
from outcomes.lifespan_model import LifespanImpactModel, generate_report as generate_lifespan_report
import os
from datetime import datetime

def save_follistatin_reports(muscle_mass_lbs=2.0, lifespan_increase_pct=2.5, population_size=334000000, output_path='.'):
    """Save separate follistatin reports for muscle mass and lifespan impacts"""
    # Create follistatin output directory
    follistatin_dir = os.path.join(output_path, 'reports', 'follistatin')
    os.makedirs(follistatin_dir, exist_ok=True)
    
    # Initialize models
    muscle_model = MuscleMassInterventionModel(muscle_mass_lbs)
    lifespan_model = LifespanImpactModel()
    
    # Generate and save muscle mass report
    muscle_filename = f'follistatin_muscle_m+{muscle_mass_lbs}lb_p{population_size}.md'
    muscle_filepath = os.path.join(follistatin_dir, muscle_filename)
    muscle_results = muscle_model.generate_report(population_size)
    
    muscle_report = f"""# Follistatin Muscle Mass Impact Analysis
Generated on: {datetime.now().strftime('%Y-%m-%d')}

## Study Parameters
- Target Population: {population_size:,} individuals
- Muscle Mass Increase: {muscle_mass_lbs} lbs per person

{muscle_results}
"""
    
    with open(muscle_filepath, 'w', encoding='utf-8') as f:
        f.write(muscle_report)
    
    # Generate and save lifespan report
    lifespan_filename = f'follistatin_lifespan_l{lifespan_increase_pct}pct_p{population_size}.md'
    lifespan_filepath = os.path.join(follistatin_dir, lifespan_filename)
    lifespan_results = generate_lifespan_report(lifespan_increase_pct, population_size)
    
    lifespan_report = f"""# Follistatin Lifespan Impact Analysis
Generated on: {datetime.now().strftime('%Y-%m-%d')}

## Study Parameters
- Target Population: {population_size:,} individuals
- Lifespan Increase: {lifespan_increase_pct}%

{lifespan_results}
"""
    
    with open(lifespan_filepath, 'w', encoding='utf-8') as f:
        f.write(lifespan_report)
    
    return muscle_filepath, lifespan_filepath

if __name__ == "__main__":
    # Generate and save the reports with default parameters
    muscle_path, lifespan_path = save_follistatin_reports()
    print(f"Muscle mass report saved to: {muscle_path}")
    print(f"Lifespan report saved to: {lifespan_path}") 