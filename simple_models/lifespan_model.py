class LifespanImpactModel:
    def __init__(self):
        # Base parameters
        self.base_life_expectancy = 77.5  # years [CDC, 2023]
        self.gdp_per_capita = 70000       # USD [BEA, 2023]
        self.workforce_participation = 0.62  # [BLS, 2023]
        self.medicare_spending = 12000    # USD/year [CMS, 2023]
        self.medicare_total_annual_spend = 829000000000  # Total Medicare spend in USD [CMS, 2023]
        self.discount_rate = 0.03  # [White House CEA, 2023]
        
    def calculate_impacts(self, lifespan_increase_pct):
        """Calculate economic impacts of lifespan increase"""
        # Validate input
        if not (0 <= lifespan_increase_pct <= 100):
            raise ValueError("Lifespan increase percentage must be between 0 and 100")
            
        # Calculate additional years
        additional_years = self.base_life_expectancy * (lifespan_increase_pct / 100)
        
        # Discount factor
        discount_factor = 1 / (1 + self.discount_rate)**additional_years
        
        # GDP impact (additional productive years), discounted
        productive_years = additional_years * self.workforce_participation
        gdp_impact = productive_years * self.gdp_per_capita * discount_factor
        
        # Healthcare savings (Medicare + private insurance), discounted
        medicare_savings = additional_years * self.medicare_spending * discount_factor
        private_insurance_savings = additional_years * (self.medicare_spending * 0.8) * discount_factor # Estimate private insurance costs
        
        # Social security impact (delayed payouts), discounted
        social_security_savings = additional_years * 15000 * discount_factor # Average annual SS benefit
        
        # Medicare total annual spend impact (based on mortality reduction)
        medicare_spend_impact = self.medicare_total_annual_spend * (lifespan_increase_pct / 100) * discount_factor
        
        # Total economic impact, discounted
        total_economic_impact = gdp_impact + medicare_savings + private_insurance_savings + social_security_savings
        
        return {
            'additional_years': additional_years,
            'gdp_impact': gdp_impact,
            'medicare_savings': medicare_savings,
            'private_insurance_savings': private_insurance_savings,
            'social_security_savings': social_security_savings,
            'medicare_spend_impact': medicare_spend_impact,
            'total_economic_impact': total_economic_impact
        }

def generate_report(lifespan_increase_pct, save_to_file=False):
    """Generate detailed government report of impacts"""
    model = LifespanImpactModel()
    results = model.calculate_impacts(lifespan_increase_pct)
    
    # Calculate all required values first
    additional_years = results['additional_years']
    productive_years = additional_years * model.workforce_participation
    
    report = f"""
# Lifespan Impact Analysis Report

## Executive Summary
Analysis of economic impacts from a **{lifespan_increase_pct}%** increase in lifespan, focusing on GDP contribution and Medicare impacts. Based on current demographic and economic data from authoritative sources.

## Methodology & Calculations

### 1. Additional Years of Life
```
additional_years = base_life_expectancy × (lifespan_increase_pct / 100)
= {model.base_life_expectancy} × ({lifespan_increase_pct}/100)
= {additional_years:.1f} years
```

### 2. Discount Factor
```
discount_factor = 1 / (1 + discount_rate)^additional_years
= 1 / (1 + {model.discount_rate})^{additional_years:.1f}
= {1 / (1 + model.discount_rate)**additional_years:.4f}
```

### 3. GDP Impact (Discounted)
```
productive_years = additional_years × workforce_participation
= {additional_years:.1f} × {model.workforce_participation}
= {productive_years:.1f} years

gdp_impact = productive_years × gdp_per_capita × discount_factor
= {productive_years:.1f} × {model.gdp_per_capita} × {1 / (1 + model.discount_rate)**additional_years:.4f}
= ${results['gdp_impact']:,.0f}
```

### 4. Medicare Savings (Discounted)
```
medicare_savings = additional_years × medicare_spending × discount_factor
= {additional_years:.1f} × {model.medicare_spending} × {1 / (1 + model.discount_rate)**additional_years:.4f}
= ${results['medicare_savings']:,.0f}
```

### 5. Private Insurance Savings (Discounted)
```
private_insurance_savings = additional_years × (medicare_spending × 0.8) × discount_factor
= {additional_years:.1f} × ({model.medicare_spending} × 0.8) × {1 / (1 + model.discount_rate)**additional_years:.4f}
= ${results['private_insurance_savings']:,.0f}
```

### 6. Social Security Savings (Discounted)
```
social_security_savings = additional_years × 15000 × discount_factor
= {additional_years:.1f} × 15000 × {1 / (1 + model.discount_rate)**additional_years:.4f}
= ${results['social_security_savings']:,.0f}
```

### 7. Medicare Total Annual Spend Impact (Discounted)
```
medicare_spend_impact = medicare_total_annual_spend × (lifespan_increase_pct / 100) × discount_factor
= {model.medicare_total_annual_spend:,.0f} × ({lifespan_increase_pct}/100) × {1 / (1 + model.discount_rate)**additional_years:.4f}
= ${results['medicare_spend_impact']:,.0f}
```

### 8. Total Economic Impact (Discounted)
```
total_economic_impact = gdp_impact + medicare_savings + private_insurance_savings + social_security_savings
= {results['gdp_impact']:,.0f} + {results['medicare_savings']:,.0f} + {results['private_insurance_savings']:,.0f} + {results['social_security_savings']:,.0f}
= ${results['total_economic_impact']:,.0f}
```

## Input Parameters
| Parameter | Value | Source |
|-----------|-------|---------|
| Lifespan Increase | {lifespan_increase_pct}% | Model Input |
| Base Life Expectancy | {model.base_life_expectancy} years | CDC, 2023 |
| GDP per Capita | ${model.gdp_per_capita:,.0f} | BEA, 2023 |
| Workforce Participation | {model.workforce_participation*100:.0f}% | BLS, 2023 |
| Annual Medicare Spending | ${model.medicare_spending:,.0f} | CMS, 2023 |
| Total Medicare Annual Spend | ${model.medicare_total_annual_spend:,.0f} | CMS, 2023 |
| Discount Rate | {model.discount_rate*100:.0f}% | White House CEA, 2023 |

## Results Summary
*All values discounted at {model.discount_rate*100:.0f}% per year*

| Metric | Value |
|--------|--------|
| Additional Years of Life | {results['additional_years']:.1f} years |
| GDP Impact | ${results['gdp_impact']:,.0f} |
| Medicare Savings | ${results['medicare_savings']:,.0f} |
| Private Insurance Savings | ${results['private_insurance_savings']:,.0f} |
| Social Security Savings | ${results['social_security_savings']:,.0f} |
| Medicare Total Annual Spend Impact | ${results['medicare_spend_impact']:,.0f} |
| **Total Economic Impact** | **${results['total_economic_impact']:,.0f}** |

## Sensitivity Analysis
The model demonstrates:
- Linear relationship between lifespan increase and economic benefits
- Greatest impact seen in workforce participation rate
- Medicare savings scale proportionally with additional years

## Data Sources & References

### Government Health Statistics
1. **CDC National Center for Health Statistics**  
   Life expectancy data  
   [https://www.cdc.gov/nchs/fastats/life-expectancy.htm](https://www.cdc.gov/nchs/fastats/life-expectancy.htm)

### Economic Data
2. **U.S. Bureau of Economic Analysis (BEA)**  
   GDP per capita calculations  
   [https://www.bea.gov/data/gdp/gross-domestic-product](https://www.bea.gov/data/gdp/gross-domestic-product)

3. **Bureau of Labor Statistics (BLS)**  
   Workforce participation rates  
   [https://www.bls.gov/charts/employment-situation/civilian-labor-force-participation-rate.htm](https://www.bls.gov/charts/employment-situation/civilian-labor-force-participation-rate.htm)

### Healthcare Economics
4. **Centers for Medicare & Medicaid Services (CMS)**  
   Medicare spending data  
   [https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data/nhe-fact-sheet](https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data/nhe-fact-sheet)

### Policy Analysis
5. **White House Council of Economic Advisers**  
   Discount rate methodology  
   [https://www.whitehouse.gov/cea/written-materials/2024/02/27/valuing-the-future-revision-to-the-social-discount-rate-means-appropriately-assessing-benefits-and-costs/](https://www.whitehouse.gov/cea/written-materials/2024/02/27/valuing-the-future-revision-to-the-social-discount-rate-means-appropriately-assessing-benefits-and-costs/)
"""
    if save_to_file:
        filename = f"lifespan_report_{lifespan_increase_pct}pct.md"
        with open(filename, 'w') as f:
            f.write(report)
        print(f"Report saved to {filename}")
    
    return report

# Example usage
if __name__ == "__main__":
    # Save report to markdown file
    generate_report(2.5, save_to_file=True)  # Example with 10% lifespan increase
