"""Configuration loading functions for the health economic impact simulator."""

import yaml
from typing import Dict, Any
from pathlib import Path

def load_yaml_file(file_path: str) -> Dict[Any, Any]:
    """Load a YAML file and return its contents as a dictionary."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def load_base_parameters() -> Dict[Any, Any]:
    """Load base parameters from the configuration file."""
    config_path = Path(__file__).parent.parent.parent.parent / 'config' / 'parameters.yaml'
    return load_yaml_file(str(config_path))

def load_interventions() -> Dict[Any, Any]:
    """Load intervention definitions from the configuration file."""
    config_path = Path(__file__).parent.parent.parent.parent / 'config' / 'interventions.yaml'
    return load_yaml_file(str(config_path))

# Import parameter ranges from parameter_definitions
from ..core.parameter_definitions import PARAMETER_RANGES, MODIFIER_RANGES 