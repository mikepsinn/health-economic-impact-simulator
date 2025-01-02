# Health Economic Impact Simulator

This project simulates and analyzes the economic impacts of various health interventions on the US healthcare system, focusing on metrics like healthcare savings, GDP impact, and Medicare spending.

## Project Structure

```
health-economic-impact-simulator/
├── config/                     # Configuration files
│   ├── base_parameters.yml    # Base economic and population parameters
│   ├── schema.json           # JSON Schema for config validation
│   └── interventions/        # Intervention-specific configs
│       ├── follistatin.yml
│       └── klotho.yml
├── src/                       # Source code
│   ├── models/               # Impact calculation models
│   │   ├── base_model.py
│   │   └── follistatin_model.py
│   └── utils/                # Utility functions
│       ├── report_generator.py
│       └── stratification.py
├── reports/                   # Generated reports
│   ├── generated/            # Auto-generated analysis reports
│   └── interventions/        # Detailed intervention reports
└── docs/                     # Documentation
```

## Configuration

### Base Parameters (`config/base_parameters.yml`)
Contains foundational parameters for calculations:
- Population statistics
- Economic parameters (GDP, healthcare costs)
- Health baseline rates

Example:
```yaml
population:
  total_us: 331900000
  over_60: 73000000
  adult: 258300000

economics:
  medicare_per_capita: 12500
  gdp_per_capita: 65000
```

### Intervention Configuration (`config/interventions/*.yml`)
Define intervention-specific parameters:
- Physical effects (e.g., muscle/fat changes)
- Longevity impacts
- Biomarker changes
- Healthcare utilization changes
- Impact modifiers

Example:
```yaml
name: "Follistatin"
description: "Muscle growth and fat reduction therapeutic protein"

default_effects:
  physical:
    muscle_mass_change: 2.0  # lbs
    fat_mass_change: -2.0    # lbs
  longevity:
    lifespan_increase: 2.5   # percentage
```

## Adding New Interventions

1. Create a new YAML file in `config/interventions/`
2. Follow the schema defined in `config/schema.json`
3. Include all required parameters:
   - Physical effects
   - Longevity impacts
   - Biomarker changes
   - Healthcare utilization
   - Impact modifiers

Example workflow:
```bash
# 1. Copy template
cp config/interventions/template.yml config/interventions/new_intervention.yml

# 2. Edit parameters
edit config/interventions/new_intervention.yml

# 3. Generate report
python src/generate_report.py
```

## Generating Reports

Reports are generated automatically for all configured interventions:

```bash
# Set Python path
$env:PYTHONPATH = "."  # Windows
export PYTHONPATH=.    # Unix

# Generate reports
python src/generate_report.py
```

Reports include:
1. Executive Summary
2. Methodology
3. Results Analysis
4. Uncertainty Analysis
5. Discussion
6. Conclusions
7. Recommendations

## Parameter Validation

All configuration files are validated against `config/schema.json`, which defines:
- Required parameters
- Valid value ranges
- Parameter descriptions
- Units of measurement

The validation ensures:
- Type checking (number, integer, string)
- Range validation (minimum/maximum values)
- Required field checking
- Structural validation

## Customizing Analysis

### Monte Carlo Simulation
Adjust parameter variations in `src/utils/report_generator.py`:
```python
param_variations = {
    'muscle_gain_lb': 0.1,  # 10% variation
    'fat_loss_lb': 0.1,
    'lifespan_increase_years': 0.15,
    'savings_per_lb': 0.2
}
```

### Impact Modifiers
Modify how intervention effects translate to outcomes in the intervention config:
```yaml
impact_modifiers:
  muscle_to_falls: 0.1      # Each lb of muscle reduces falls by 10%
  lifespan_to_gdp: 0.8      # 80% of lifespan increase converts to GDP
  health_quality: 0.05      # 5% improvement in quality of life
```

## Best Practices

1. **Parameter Updates**
   - Keep base parameters current with latest US statistics
   - Document sources for parameter values
   - Update ranges based on latest research

2. **Adding Interventions**
   - Use conservative estimates for effects
   - Include all relevant impact pathways
   - Document assumptions clearly

3. **Report Generation**
   - Generate reports for each major parameter update
   - Compare results across different interventions
   - Archive reports with parameter versions

## Troubleshooting

Common issues and solutions:

1. **Configuration Validation Errors**
   ```
   ValueError: Configuration validation failed: 'physical' is a required property
   ```
   - Check if all required parameters are present
   - Verify values are within allowed ranges
   - Ensure correct units are used

2. **Import Errors**
   ```
   ImportError: attempted relative import beyond top-level package
   ```
   - Set PYTHONPATH correctly
   - Check file structure matches project layout
   - Verify import statements use correct paths

3. **Report Generation Issues**
   - Ensure all dependencies are installed
   - Check file permissions for output directories
   - Verify configuration files are valid YAML

## Contributing

1. Follow the existing code structure
2. Update documentation for new features
3. Add validation rules for new parameters
4. Include sources for parameter values
5. Test with multiple intervention types 