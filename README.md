# Health Economic Impact Simulator

A comprehensive simulation framework for analyzing the economic impact of gene therapies and life extension technologies.

## Project Structure

```
├── src/                          # Core simulation code
│   ├── models/                   # Simulation models
│   │   ├── gene_therapy/        # Gene-specific intervention models
│   │   ├── economic/           # Economic impact calculations
│   │   └── clinical/           # Clinical trial and biomarker analysis
│   ├── analysis/                # Analysis frameworks
│   └── utils/                   # Shared utilities
├── config/                       # Configuration files
├── data/                        # Data sources and preprocessing
├── tests/                       # Test suite
└── docs/                        # Documentation
```

## Key Features

1. Gene Therapy Impact Models
   - Follistatin therapy impact on healthcare costs and productivity
   - Lifespan extension economic benefits
   - Klotho therapy cognitive and health outcomes

2. Economic Analysis
   - Healthcare cost reduction modeling
   - Workforce productivity impact
   - Medicare savings calculations
   - GDP impact analysis

3. Clinical Study Design
   - Biomarker correlation analysis
   - Population stratification
   - Outcome tracking frameworks

4. Implementation Tools
   - Sensitivity analysis
   - Model validation
   - Stakeholder reporting

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure
4. Run tests: `pytest tests/`

## Usage

See `QUICKSTART.md` for detailed usage instructions and examples.

## How it works

The simulator:
1. Takes a therapeutic intervention (e.g. Follistatin, Klotho)
2. Analyzes intervention effects across multiple domains:
   - Physical changes (muscle mass, fat mass)
   - Longevity impacts (lifespan increase)
   - Biomarker changes (eGFR, cystatin C)
   - Healthcare utilization (hospital visits)
3. Calculates economic impacts:
   - Medicare spending changes
   - GDP impact from increased lifespan
   - Healthcare system cost savings
4. Performs uncertainty analysis:
   - Monte Carlo simulations
   - Parameter sensitivity analysis
   - Confidence intervals

## Configuration Structure

### Base Parameters (`config/base_parameters.yml`)
```yaml
population:
  total_us: 331900000    # Total US population
  over_60: 73000000      # Population over 60
  adult: 258300000       # Adult population (18+)

economics:
  medicare_per_capita: 12500     # Annual Medicare spending per beneficiary
  gdp_per_capita: 65000         # US GDP per capita
  alzheimers_annual_cost: 355B  # Total US annual cost
  ckd_annual_cost: 87B         # Total US annual cost

health_baselines:
  hospital_visits_per_year: 0.125  # Average per person
  average_lifespan: 79.1          # Years
  medicare_enrollment_rate: 0.186  # Percentage of population
```

### Intervention Configuration (`config/interventions/*.yml`)
```yaml
name: "Intervention Name"
description: "Brief description of mechanism"

default_effects:
  physical:
    muscle_mass_change: 2.0  # lbs (positive = gain)
    fat_mass_change: -2.0    # lbs (negative = loss)
    
  longevity:
    lifespan_increase: 2.5   # percentage
    
  biomarkers:
    egfr_change: 5.0         # mL/min/1.73m²
    cystatin_c_change: -0.2  # mg/L

  healthcare:
    hospital_visit_reduction: 15.0  # percentage reduction
    
impact_modifiers:
  muscle_to_falls: 0.1       # Falls reduced per lb muscle
  lifespan_to_gdp: 0.8      # GDP impact fraction
  health_quality: 0.05      # QALY improvement
  kidney_to_medicare: 0.10  # Medicare cost reduction
```

## Economic Impact Calculations

### Medicare Spending Impact
```
Annual Medicare Savings = 
    Medicare Beneficiaries × 
    Annual Cost per Beneficiary × 
    (Health Quality Improvement + Biomarker Impact)

Where:
- Health Quality Improvement = impact_modifiers.health_quality
- Biomarker Impact = kidney_to_medicare × normalized_biomarker_change
```

### GDP Impact
```
GDP Impact = 
    Target Population × 
    Workforce Fraction × 
    GDP per Capita × 
    Lifespan Increase × 
    Lifespan to GDP Modifier × 
    Discount Factor

Where:
- Lifespan Increase = default_effects.longevity.lifespan_increase
- Lifespan to GDP Modifier = impact_modifiers.lifespan_to_gdp
- Discount Factor accounts for future value depreciation
```

### Healthcare Cost Savings
```
Annual Healthcare Savings = 
    Target Population × 
    (Muscle Mass Change + Fat Mass Change) × 
    Savings per Pound

Additional Savings from Hospital Reduction =
    Population × 
    Baseline Hospital Visits × 
    Hospital Visit Reduction × 
    Cost per Visit
```

## Generated Reports

Reports are automatically generated for each intervention in `reports/generated/` with filenames encoding key parameters:
```
{intervention_name}_m{muscle_change}lb_f{fat_change}lb_l{lifespan_increase}pct.md
```

Each report includes:
1. Executive Summary
   - Intervention description
   - Key findings
2. Methodology
   - Population parameters
   - Economic parameters
   - Intervention parameters
3. Results Analysis
   - Healthcare savings
   - GDP impact
   - Medicare spending changes
4. Uncertainty Analysis
   - Monte Carlo results
   - Parameter variations
   - Confidence intervals
5. Discussion & Recommendations

## Usage

1. Configure intervention parameters:
```bash
# Copy template
cp config/interventions/template.yml config/interventions/new_intervention.yml

# Edit parameters
edit config/interventions/new_intervention.yml
```

2. Generate reports:
```bash
# Set Python path
$env:PYTHONPATH = "."  # Windows
export PYTHONPATH=.    # Unix

# Generate reports
python src/generate_report.py
```

## Adding New Interventions

1. Create configuration file in `config/interventions/`
2. Follow schema in `config/schema.json`
3. Implement intervention-specific model (optional):
   ```python
   # models/new_intervention_model.py
   from models.base_model import BaseImpactModel, BaseInterventionParams
   
   class NewInterventionParams(BaseInterventionParams):
       # Add intervention-specific parameters
   
   class NewInterventionModel(BaseImpactModel):
       # Add intervention-specific calculations
   ```

## Validation

All configurations are validated against `config/schema.json`, which defines:
- Required parameters
- Valid value ranges
- Parameter descriptions
- Units of measurement

## Future Enhancements

Planned features:
1. Additional impact pathways:
   - Cognitive function (IQ changes)
   - Disease progression modifiers
   - Quality of life metrics
2. Enhanced analysis:
   - Age-stratified impacts
   - Regional variations
   - Demographic subgroups
3. Integration capabilities:
   - Clinical trial data import
   - Real-time parameter updates
   - Comparative intervention analysis




