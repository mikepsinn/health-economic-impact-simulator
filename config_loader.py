import yaml
from pathlib import Path
from typing import Dict, Any

def load_yaml(file_path: str) -> Dict[Any, Any]:
    """Load a YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_base_parameters() -> Dict[Any, Any]:
    """Load base parameters from config."""
    return load_yaml('config/base_parameters.yml')

def load_interventions() -> Dict[str, Dict[Any, Any]]:
    """Load all intervention configurations."""
    interventions = {}
    interventions_dir = Path('config/interventions')
    for file in interventions_dir.glob('*.yml'):
        interventions[file.stem] = load_yaml(str(file))
    return interventions

# Default ranges for parameter adjustments
PARAMETER_RANGES = {
    'muscle_mass_change': (-5.0, 10.0, 0.5),
    'fat_mass_change': (-10.0, 5.0, 0.5),
    'iq_increase': (0.0, 10.0, 0.5),
    'alzheimers_reduction': (0.0, 50.0, 5.0),
    'egfr_improvement': (0.0, 15.0, 0.5),
    'ckd_progression_reduction': (0.0, 50.0, 5.0),
    'lifespan_increase': (0.0, 5.0, 0.1),
    'hospital_visit_reduction': (0.0, 50.0, 5.0)
}

# Impact modifier ranges
MODIFIER_RANGES = {
    'min_value': 0.0,
    'max_value': 1.0,
    'step': 0.05
} 