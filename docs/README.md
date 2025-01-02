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
│       └── template.yml
├── src/                       # Source code
│   ├── models/               # Impact calculation models
│   │   └── base_model.py     # Core impact calculation model
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
  total: 331900000
  target: 258300000
  medicare_beneficiaries: 73000000
  workforce_fraction: 0.5

economics:
  annual_healthcare_cost: 12500
  annual_productivity: 65000
  discount_rate: 0.03
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
  healthcare:
    hospital_visit_reduction: 15.0  # percentage

impact_modifiers:
  health_quality: 0.05  # 5% improvement in quality of life
```

## Adding New Interventions

1. Copy the template from `config/interventions/template.yml`
2. Follow the schema defined in `config/schema.json`
3. Include all required parameters:
   - Physical effects
   - Longevity impacts
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

The system automatically generates reports for all configured interventions:

```bash
# Set Python path
$env:PYTHONPATH = "."  # Windows
export PYTHONPATH=.    # Unix

# Generate reports
python src/generate_report.py
```

Reports include:
1. Summary of Economic Impacts
   - Annual Healthcare Savings
   - GDP Impact
   - Medicare Savings
   - QALYs Gained
2. Intervention Parameters
   - Physical Effects
   - Longevity Impact
   - Health Improvements
3. Population Parameters
   - Target Population
   - Medicare Beneficiaries
   - Workforce Statistics
4. Economic Parameters
   - Healthcare Costs
   - Productivity Metrics
   - Discount Rates

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

## Impact Calculations

The system uses a unified model (`src/models/base_model.py`) to calculate:

1. **Healthcare Savings**
   - Body composition improvements
   - Reduced hospital visits
   - Medicare cost reductions

2. **GDP Impact**
   - Increased productive years
   - Workforce participation
   - Time-discounted value

3. **Quality of Life**
   - QALYs gained
   - Health improvements
   - Longevity benefits

## Best Practices

1. **Parameter Updates**
   - Keep base parameters current with latest US statistics
   - Document sources for parameter values
   - Use conservative estimates

2. **Adding Interventions**
   - Start with the template.yml
   - Include all required parameters
   - Document assumptions clearly

3. **Report Generation**
   - Generate reports after parameter updates
   - Compare results across interventions
   - Archive reports with parameter versions

## Troubleshooting

Common issues and solutions:

1. **Configuration Validation Errors**
   ```
   ValueError: Configuration validation failed
   ```
   - Check if all required parameters are present
   - Verify values are within allowed ranges
   - Ensure correct units are used

2. **Import Errors**
   ```
   ImportError: No module named 'src'
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