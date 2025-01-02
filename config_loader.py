import yaml
import json
from pathlib import Path
from typing import Dict, Any
from jsonschema import validate, ValidationError

def load_schema() -> Dict[Any, Any]:
    """Load the JSON schema for config validation."""
    with open('config/schema.json', 'r') as file:
        return json.load(file)

def load_yaml(file_path: str) -> Dict[Any, Any]:
    """Load a YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def validate_config(config: Dict[Any, Any], schema_section: str) -> None:
    """Validate config against schema section."""
    schema = load_schema()
    if schema_section not in schema["definitions"]:
        raise ValueError(f"Unknown schema section: {schema_section}")
    
    try:
        validate(instance=config, schema=schema["definitions"][schema_section])
    except ValidationError as e:
        raise ValueError(f"Configuration validation failed: {str(e)}")

def load_base_parameters() -> Dict[Any, Any]:
    """Load and validate base parameters from config."""
    config = load_yaml('config/base_parameters.yml')
    validate_config(config, "base_parameters")
    return config

def load_interventions() -> Dict[str, Dict[Any, Any]]:
    """Load and validate all intervention configurations."""
    interventions = {}
    interventions_dir = Path('config/interventions')
    for file in interventions_dir.glob('*.yml'):
        config = load_yaml(str(file))
        validate_config(config, "intervention")
        interventions[file.stem] = config
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