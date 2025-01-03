# Follistatin Lifespan Impact Analysis
Generated on: 2025-01-02

## Study Parameters
- Target Population: 334,000,000 individuals
- Lifespan Increase: 2.5%


# Lifespan Impact Analysis Report

## Executive Summary
Analysis of economic impacts from a **2.5%** increase in lifespan across a population of **334,000,000** individuals, focusing on GDP contribution and Medicare impacts. Based on current demographic and economic data from authoritative sources.

## Methodology & Calculations

### 1. Additional Years of Life (Per Person)
```
additional_years = base_life_expectancy × (lifespan_increase_pct / 100)
= 77.5 × (2.5/100)
= 1.9 years
```

### 2. Discount Factor
```
discount_factor = 1 / (1 + discount_rate)^additional_years
= 1 / (1 + 0.03)^1.9
= 0.9443
```

### 3. GDP Impact (Population-wide, Discounted)
```
productive_years = additional_years × workforce_participation
= 1.9 × 0.62
= 1.2 years per person

gdp_impact = productive_years × gdp_per_capita × discount_factor × population_size
= 1.2 × 70000 × 0.9443 × 334,000,000
= $26,521,970,315,212
```

### 4. Medicare Savings (Population-wide, Discounted)
```
medicare_savings = additional_years × medicare_spending × discount_factor × population_size
= 1.9 × 12000 × 0.9443 × 334,000,000
= $7,333,263,681,625
```

### 5. Private Insurance Savings (Population-wide, Discounted)
```
private_insurance_savings = additional_years × (medicare_spending × 0.8) × discount_factor × population_size
= 1.9 × (12000 × 0.8) × 0.9443 × 334,000,000
= $5,866,610,945,300
```

### 6. Social Security Savings (Population-wide, Discounted)
```
social_security_savings = additional_years × 15000 × discount_factor × population_size
= 1.9 × 15000 × 0.9443 × 334,000,000
= $9,166,579,602,032
```

### 7. Medicare Total Annual Spend Impact (Discounted)
```
medicare_spend_impact = medicare_total_annual_spend × (lifespan_increase_pct / 100) × discount_factor
= 829,000,000,000 × (2.5/100) × 0.9443
= $19,571,423,579
```

### 8. Total Economic Impact (Population-wide, Discounted)
```
total_economic_impact = gdp_impact + medicare_savings + private_insurance_savings + social_security_savings
= 26,521,970,315,212 + 7,333,263,681,625 + 5,866,610,945,300 + 9,166,579,602,032
= $48,888,424,544,170
```

## Input Parameters
| Parameter | Value | Source |
|-----------|-------|---------|
| Population Size | 334,000,000 | Model Input |
| Lifespan Increase | 2.5% | Model Input |
| Base Life Expectancy | 77.5 years | CDC, 2023 |
| GDP per Capita | $70,000 | BEA, 2023 |
| Workforce Participation | 62% | BLS, 2023 |
| Annual Medicare Spending | $12,000 | CMS, 2023 |
| Total Medicare Annual Spend | $829,000,000,000 | CMS, 2023 |
| Discount Rate | 3% | White House CEA, 2023 |

## Results Summary
*All values discounted at 3% per year for population of 334,000,000*

| Metric | Value |
|--------|--------|
| Additional Years of Life (per person) | 1.9 years |
| GDP Impact | $26,521,970,315,212 |
| Medicare Savings | $7,333,263,681,625 |
| Private Insurance Savings | $5,866,610,945,300 |
| Social Security Savings | $9,166,579,602,032 |
| Medicare Total Annual Spend Impact | $19,571,423,579 |
| **Total Economic Impact** | **$48,888,424,544,170** |

## Sensitivity Analysis
The model demonstrates:
- Linear relationship between lifespan increase and economic benefits
- Greatest impact seen in workforce participation rate
- Medicare savings scale proportionally with additional years
- Population size directly scales all economic impacts except Medicare total annual spend

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

