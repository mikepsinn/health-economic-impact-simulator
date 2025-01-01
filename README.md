# Health and Economic Impact Simulator

This project is a web app that calculates the health and economic impact of therapeutic interventions, with a focus on Medicare spending implications.

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

This MVP version focuses on essential calculations while maintaining flexibility for future complexity additions.




