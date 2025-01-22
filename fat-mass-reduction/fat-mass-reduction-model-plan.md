# README: Fat-Mass Reduction Health and Economic Impact Analysis

## 1. Overview
Framework for estimating the health and economic impact of X pounds of fat-mass reduction across populations

## 2. Input Parameters
Key parameters to collect:
- Population demographics (age, gender, ethnicity)
- Baseline obesity rates and BMI distribution
- Current healthcare costs for obesity-related conditions

### 2.1 Model Architecture
- Type: Discrete-time Markov cohort model with 1-year cycles
- Time Horizon: 20-year base case (10-30y sensitivity)
- States: Healthy, Obese, Comorbidities, Post-Intervention, Dead
- Discount Rates: 3% base case (0-5% sensitivity range)
- Therapy efficacy data (X pounds reduction)
- Therapy costs (one-time vs ongoing)
- Discount rates for future costs/benefits

## 3. Outcome Metrics  
Core metrics to calculate:
- Quality-Adjusted Life Years (QALYs) gained
- Healthcare cost savings (short and long-term)
- Return on Investment (ROI) calculations
- Budget impact analysis
- Cost-effectiveness ratios (ICERs)

## 4. Calculation Methodology
Standard formulas:
- QALY = (Utility gain) × (Years of benefit)
- Cost savings = (Reduced healthcare utilization) × (Unit costs)  
- ROI = (Total benefits - Total costs) / Total costs
- ICER = (Cost of therapy - Cost of standard care) / (QALY therapy - QALY standard care)

## 5. Example Analysis
Sample calculations using:
- Medicare population data
- Typical obesity-related costs
- Projected therapy outcomes

## 6. References

1. [A cost-benefit analysis framework for preventive health interventions](https://pubmed.ncbi.nlm.nih.gov/34923970/)  
   Deakin Health Economics framework for evaluating preventive interventions

2. [ICER's Reference Case for Economic Evaluations](https://icer.org/wp-content/uploads/2024/02/ICER-Reference-Case_2024.pdf)  
   Standard methodology for QALY calculations and ICER analysis

3. [Systematic review of long-term effects](https://pubmed.ncbi.nlm.nih.gov/15147610/)  
   Cost-effectiveness analysis showing £2329 per life-year gained from weight loss

4. [Economic evaluations of obesity interventions](https://onlinelibrary.wiley.com/doi/10.1111/obr.13597)  
   Quantifies QALY gains from specific pound reductions in weight

5. [Impact of metabolic surgery on costs](https://www.sciencedirect.com/science/article/pii/S1550728921004950)  
   Long-term health economic model comparing weight loss methods
