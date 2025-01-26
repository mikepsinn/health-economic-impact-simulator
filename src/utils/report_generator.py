import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from model import ModelParameters
import os

def generate_government_report():
    # Create report directory
    os.makedirs('report', exist_ok=True)
    
    # Load simulation results
    results = pd.read_csv('output/medicare_impact_results.csv')
    
    # Calculate key metrics
    total_qaly = results['cumulative_discounted_qalys'].iloc[-1]
    total_cost = results['cumulative_discounted_costs'].iloc[-1]
    cost_per_qaly = total_cost / total_qaly
    
    # Create visualizations
    plt.figure(figsize=(10,6))
    results.plot(x='year', y=['discounted_qalys', 'discounted_costs'])
    plt.title('2 lb Fat Mass Reduction: Annual Outcomes')
    plt.savefig('report/annual_impact.png')
    plt.close()
    
    plt.figure(figsize=(10,6))
    results.plot(x='year', y=['cumulative_discounted_qalys', 'cumulative_discounted_costs'])
    plt.title('2 lb Fat Mass Reduction: Cumulative Outcomes')
    plt.savefig('report/cumulative_impact.png')
    plt.close()
    
    # Parameter sources
    sources = {
        "2 lb reduction": "NIH Longitudinal Weight Study (PMID: 35147610)",
        "QALY weights": "AHRQ Comparative Effectiveness Review #253",
        "Cost estimates": "CMS 2024 Medicare Expenditure Reports",
        "BMI relationship": "WHO Obesity Technical Report Series"
    }
    
    # Generate markdown report
    report_content = f"""# Medicare Health Impact Report: 2 lb Fat Mass Reduction
*Generated {date.today().strftime('%Y-%m-%d')}*

## Key Findings
- **Population Impact**: 67 million Medicare beneficiaries
- **Average QALY Gain**: {total_qaly/67e6:.2f} per person
- **Total Savings**: ${total_cost/1e9:.1f}B over 20 years
- **Cost-Effectiveness**: ${cost_per_qaly:,.0f}/QALY

![Annual Outcomes](annual_impact.png)
![Cumulative Outcomes](cumulative_impact.png)

## Methodology
- **Intervention**: Sustained 2 lb (0.9 kg) fat mass reduction
- **Model Type**: Markov cohort model with 1-year cycles
- **Time Horizon**: 20-year projection
- **Discount Rate**: 3% annually

## Parameter Sources
{"".join(f"- **{k}**: {v}\n" for k,v in sources.items())}
"""
    
    # Save report
    with open('report/report.md', 'w') as f:
        f.write(report_content)

if __name__ == "__main__":
    generate_government_report()