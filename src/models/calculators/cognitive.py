"""Cognitive impact calculator."""

from typing import Dict, TextIO

from src.utils.reporting.formatters import format_currency, format_equation, format_number
from . import BaseCalculator

class CognitiveCalculator(BaseCalculator):
    """Calculator for cognitive intervention impacts."""

    def calculate(self, params: Dict) -> Dict:
        """Calculate impacts from cognitive changes."""
        iq_increase = params.get('iq_increase', 0)
        alzheimers_reduction = params.get('alzheimers_reduction', 0) / 100
        
        # Calculate GDP impact from IQ improvement
        gdp_impact = (
            self.pop.target_population * 
            iq_increase * 
            self.modifiers.iq_to_gdp * 
            self.econ.annual_productivity
        )
        
        # Calculate Medicare savings from reduced Alzheimer's
        alzheimers_savings = (
            self.pop.medicare_beneficiaries * 
            alzheimers_reduction * 
            self.modifiers.alzheimers_to_medicare * 
            self.healthcare.annual_alzheimers_cost
        )
        
        # Calculate QALYs from cognitive improvements
        qalys = (
            self.pop.target_population * 
            (iq_increase * 0.01 + alzheimers_reduction * 0.05) * 
            self.modifiers.health_quality
        )
        
        return {
            'gdp_impact': gdp_impact,
            'alzheimers_savings': alzheimers_savings,
            'qalys_gained': qalys
        }
    
    def write_calculations(self, f: TextIO, params: Dict, results: Dict) -> None:
        """Write cognitive impact calculations to report."""
        f.write("### Cognitive Impact Calculations\n")
        
        # GDP impact from IQ increase
        f.write("Economic gains from improved cognitive function:\n\n")
        equation = "GDP Impact = Population × IQ_Increase × IQ_to_GDP × Annual_Productivity"
        f.write(format_equation(equation))
        f.write(f"\nAnnual GDP impact: {format_currency(results['gdp_impact'])}\n\n")
        
        # Medicare savings from Alzheimer's reduction
        f.write("Medicare savings from reduced Alzheimer's progression:\n\n")
        equation = "Alzheimer's Savings = Beneficiaries × Reduction × Cost × Medicare_Impact"
        f.write(format_equation(equation))
        f.write(f"\nAnnual Medicare savings: {format_currency(results['alzheimers_savings'])}\n\n")
        
        # QALY impact
        f.write("Quality-adjusted life years gained from cognitive improvements:\n\n")
        equation = "QALYs = Population × (IQ_Effect + Alzheimer's_Effect) × Health_Quality"
        f.write(format_equation(equation))
        f.write(f"\nTotal QALYs gained: {format_number(results['qalys_gained'])}\n\n") 