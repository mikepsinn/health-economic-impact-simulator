# Health and Economic Impact Simulator

This project is a web app that calculates the health and economic impact of therapeutic interventions, with a focus on Medicare spending implications.

## Quick Start Guide

See [docs/QUICKSTART.md](docs/QUICKSTART.md)

## How it works

The simulator:
1. Takes a therapeutic intervention (e.g. Follistatin, Klotho, Thymosin-alpha-1)
2. Allows input of key biomarkers and metrics:
   - Physical metrics (muscle mass, fat mass)
   - Biomarkers (eGFR, cystatin C)
   - Cognitive measures (IQ changes)
   - Disease progression rates (e.g. Alzheimer's, kidney disease)
   - Lifespan changes
3. Analyzes impact across different population segments:
   - Total US population
   - Age-specific groups (e.g. over 60)
   - Adult population
4. Calculates economic outcomes focused on:
   - Medicare total annual spending changes
   - GDP impact
   - Healthcare system cost savings
5. Provides a simple web interface to:
   - Modify parameters in real-time
   - View results and projections
   - Export data for study design and reporting

## Developer Implementation Guide

### Application Structure
```
/src
  /config
    - base_parameters.yml    # Default population parameters
    - interventions/         # One YAML file per intervention
      - follistatin.yml
      - klotho.yml
      - thymosin.yml
  /components
    - ParameterForm.tsx     # Input form for modifying parameters
    - ResultsDisplay.tsx    # Display calculations and graphs
    - Report.tsx           # Formatted report for agencies
  /utils
    - calculations.ts      # Implementation of formulas
    - formatters.ts       # Data formatting for display
```

### Intervention YAML Structure
```yaml
name: "Follistatin"
description: "Muscle growth and fat reduction therapeutic"
default_effects:
  muscle_mass_change: 2.0  # lbs
  fat_mass_change: -2.0    # lbs
  lifespan_increase: 2.5   # percentage
  biomarkers:
    egfr_change: 5.0
    cystatin_c_change: -0.2
```

### Single Page Layout
1. Intervention selector dropdown
2. Parameter adjustment panel
3. Real-time results display
4. Report generation button

## Input Parameters

### Population Parameters
- Total population size
- Age distribution
- Current Medicare spending per capita
- Current GDP per capita
- Baseline health metrics by age group

### Intervention Effects
- Muscle mass change (lbs)
- Fat mass change (lbs)
- Lifespan increase (%)
- IQ change (points)
- Disease progression modifiers (%)
- Biomarker changes:
  - eGFR change
  - Cystatin C change

## Output Calculations

### Economic Impact
1. Medicare Spending Change ($)
   ```
   Δ Medicare = Population × (Current Medicare per capita × Health Impact Modifier)
   ```

2. GDP Impact ($)
   ```
   Δ GDP = Population × (GDP per capita × Lifespan Increase × Productivity Modifier)
   ```

3. QALYs
   ```
   Δ QALYs = Population × (Lifespan Change + Health Quality Modifier)
   ```

### Health Metrics
1. Population Health Impact
   ```
   Total Health Benefit = Σ(Individual Benefits × Population Distribution)
   ```

2. Healthcare Utilization
   ```
   Δ Hospital Visits = Population × (Baseline Rate × Health Impact Modifier)
   ```

## Report Format

The generated report will include:
1. Executive Summary
   - Intervention name and description
   - Key findings in bullet points
2. Economic Impact Section
   - Medicare savings projections
   - GDP impact estimates
3. Health Impact Section
   - Population health benefits
   - Healthcare system effects
4. Methodology Summary
   - Key parameters used
   - Calculation approach

## Key Features

- Real-time calculation updates
- Study data integration capabilities
- Focus on Medicare spending implications
- Population-level impact analysis
- Designed to inform future clinical studies and research priorities

## Primary Metrics

1. Changes in Medicare spending
2. GDP impact
3. Quality Adjusted Life Years (QALYs)
4. Healthcare utilization metrics (e.g. hospital visits, hip fractures)


