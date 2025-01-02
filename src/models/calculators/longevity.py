"""Longevity impact calculator."""

from typing import Dict, TextIO

from src.utils.reporting.formatters import format_currency, format_equation, format_number
from . import BaseCalculator

class LongevityCalculator(BaseCalculator):
    """Calculator for longevity intervention impacts."""

    def calculate(self, params: Dict) -> Dict:
        """Calculate impacts from longevity changes."""
        lifespan_increase = params.get('lifespan_increase_years', 0)
        health_improvement = params.get('healthspan_improvement_percent', 0) / 100
        
        # Calculate GDP impact from extended productive years
        working_years = lifespan_increase * self.pop.workforce_fraction
        annual_gdp = self.pop.target_population * working_years * self.econ.annual_productivity
        lifetime_gdp = annual_gdp * self.modifiers.lifespan_to_gdp
        
        # Calculate QALYs from extended life and improved health
        qalys = (
            self.pop.target_population * 
            lifespan_increase * 
            (1 + health_improvement * self.modifiers.health_quality)
        )
        
        return {
            'working_years': working_years,
            'annual_gdp_impact': annual_gdp,
            'lifetime_gdp_impact': lifetime_gdp,
            'qalys_gained': qalys
        }
    
    def write_calculations(self, f: TextIO, params: Dict, results: Dict) -> None:
        """Write longevity impact calculations to report."""
        f.write("### Longevity Impact Calculations\n")
        f.write("Economic gains from increased productive lifespan:\n\n")
        
        # GDP impact
        equation = "GDP Impact = Population × Workforce_Fraction × Lifespan_Increase × Annual_Productivity"
        f.write(format_equation(equation))
        f.write(f"\nAdditional productive years: {results['working_years']:.2f}\n")
        f.write(f"Annual GDP impact: {format_currency(results['annual_gdp_impact'])}\n")
        f.write(f"Lifetime GDP impact: {format_currency(results['lifetime_gdp_impact'])}\n\n")
        
        # QALY impact
        f.write("Quality-adjusted life years gained:\n\n")
        equation = "QALYs = Population × Lifespan_Increase × (1 + Health_Quality_Improvement)"
        f.write(format_equation(equation))
        f.write(f"\nTotal QALYs gained: {format_number(results['qalys_gained'])}\n\n") 