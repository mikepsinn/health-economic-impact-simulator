import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.parameters = self._load_yaml('model_parameters.yaml')
        
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load and parse a YAML file."""
        file_path = self.config_dir / filename
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_parameter(self, category: str, parameter: str = None) -> Any:
        """Get a parameter value with optional subcategory."""
        if parameter is None:
            return self.parameters[category]
        return self.parameters[category][parameter]
    
    def get_category_metadata(self, category: str) -> Dict[str, Any]:
        """Get all metadata (source, evidence) for a parameter category."""
        param_data = self.parameters[category]
        return {
            'source': param_data['source'],
            'source_url': param_data['source_url'],
            'evidence': param_data['evidence']
        }

# Example usage:
if __name__ == '__main__':
    config = ConfigLoader()
    
    # Get mortality rates with all metadata
    mortality_rates = config.get_parameter('mortality_rates')
    metadata = config.get_category_metadata('mortality_rates')
    
    print(f"Mortality rates: {mortality_rates}")
    print(f"Source: {metadata['source']}")
    print(f"Evidence: {metadata['evidence']['quote']}") 