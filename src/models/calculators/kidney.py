"""Kidney impact calculator."""

from typing import Dict, TextIO

from src.utils.reporting.formatters import format_currency, format_equation, format_number
from . import BaseCalculator

class KidneyCalculator(BaseCalculator):
    """Calculator for kidney intervention impacts."""

    def calculate(self, params: Dict) -> Dict:
        """Calculate impacts from kidney function changes."""
        egfr_improvement = params.get('egfr_improvement', 0)
        ckd_reduction = params.get('ckd_progression_reduction', 0) / 100
        
        # Calculate Medicare savings from improved kidney function
        medicare_savings = (
            self.pop.medicare_beneficiaries * 
            ckd_reduction * 
            self.modifiers.kidney_to_medicare * 
            self.healthcare.annual_ckd_cost
        )
        
        # Calculate QALYs from kidney improvements
        qalys = (
            self.pop.target_population * 
            (egfr_improvement * 0.02 + ckd_reduction * 0.1) * 
            self.modifiers.health_quality
        )
        
        return {
            'medicare_savings': medicare_savings,
            'qalys_gained': qalys
        }
    
    def write_calculations(self, f: TextIO, params: Dict, results: Dict) -> None:
        """Write kidney impact calculations to report."""
        f.write("### Kidney Function Impact Calculations\n")
        
        # Medicare savings
        f.write("Medicare savings from reduced CKD progression:\n\n")
        equation = "Medicare Savings = Beneficiaries × CKD_Reduction × Cost × Medicare_Impact"
        f.write(format_equation(equation))
        f.write(f"\nAnnual Medicare savings: {format_currency(results['medicare_savings'])}\n\n")
        
        # QALY impact
        f.write("Quality-adjusted life years gained from kidney improvements:\n\n")
        equation = "QALYs = Population × (eGFR_Effect + CKD_Effect) × Health_Quality"
        f.write(format_equation(equation))
        f.write(f"\nTotal QALYs gained: {format_number(results['qalys_gained'])}\n\n") 