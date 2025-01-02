"""Healthcare impact calculator."""

from typing import Dict, TextIO

from src.utils.reporting.formatters import format_currency, format_equation, format_number
from . import BaseCalculator

class HealthcareCalculator(BaseCalculator):
    """Calculator for healthcare intervention impacts."""

    def calculate(self, params: Dict) -> Dict:
        """Calculate impacts from healthcare utilization changes."""
        visit_reduction = params.get('hospital_visit_reduction_percent', 0) / 100
        
        # Calculate baseline hospital visits
        baseline_visits = (
            self.pop.target_population * 
            self.healthcare.annual_hospital_visits / 
            self.pop.total_population
        )
        
        # Calculate savings from reduced visits
        visit_savings = (
            baseline_visits * 
            visit_reduction * 
            self.healthcare.cost_per_hospital_visit
        )
        
        # Calculate QALYs from reduced hospitalizations
        qalys = (
            self.pop.target_population * 
            visit_reduction * 
            0.05 * 
            self.modifiers.health_quality
        )
        
        return {
            'baseline_visits': baseline_visits,
            'visits_reduced': baseline_visits * visit_reduction,
            'visit_savings': visit_savings,
            'qalys_gained': qalys
        }
    
    def write_calculations(self, f: TextIO, params: Dict, results: Dict) -> None:
        """Write healthcare impact calculations to report."""
        f.write("### Healthcare Utilization Impact Calculations\n")
        
        # Hospital visit reduction
        f.write("Savings from reduced hospital visits:\n\n")
        equation = "Visit Savings = Baseline_Visits × Visit_Reduction × Cost_per_Visit"
        f.write(format_equation(equation))
        f.write(f"\nBaseline annual visits: {format_number(results['baseline_visits'])}\n")
        f.write(f"Visits reduced: {format_number(results['visits_reduced'])}\n")
        f.write(f"Annual savings: {format_currency(results['visit_savings'])}\n\n")
        
        # QALY impact
        f.write("Quality-adjusted life years gained from reduced hospitalizations:\n\n")
        equation = "QALYs = Population × Visit_Reduction × Health_Effect × Quality_Factor"
        f.write(format_equation(equation))
        f.write(f"\nTotal QALYs gained: {format_number(results['qalys_gained'])}\n\n") 