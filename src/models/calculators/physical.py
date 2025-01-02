"""Physical impact calculator."""

from typing import Dict, TextIO

from src.utils.reporting.formatters import format_currency, format_equation
from . import BaseCalculator

class PhysicalCalculator(BaseCalculator):
    """Calculator for physical intervention impacts."""

    def calculate(self, params: Dict) -> Dict:
        """Calculate impacts from physical changes."""
        muscle_change = params.get('muscle_mass_change_lb', 0)
        fat_change = params.get('fat_mass_change_lb', 0)
        
        # Calculate healthcare savings from body composition changes
        muscle_savings = (
            self.pop.target_population * 
            muscle_change * 
            self.healthcare.savings_per_lb_muscle
        )
        
        fat_savings = (
            self.pop.target_population * 
            abs(fat_change) * 
            self.healthcare.savings_per_lb_fat
        )
        
        return {
            'muscle_savings': muscle_savings,
            'fat_savings': fat_savings,
            'total_savings': muscle_savings + fat_savings
        }
    
    def write_calculations(self, f: TextIO, params: Dict, results: Dict) -> None:
        """Write physical impact calculations to report."""
        f.write("### Physical Impact Calculations\n")
        f.write("Healthcare savings from body composition changes:\n\n")
        
        # Muscle mass impact
        equation = "Muscle Savings = Population × Muscle_Change × $12/lb"
        f.write(format_equation(equation))
        f.write(f"\nMuscle-related savings: {format_currency(results['muscle_savings'])}\n\n")
        
        # Fat mass impact
        equation = "Fat Savings = Population × Fat_Change × $8/lb"
        f.write(format_equation(equation))
        f.write(f"\nFat-related savings: {format_currency(results['fat_savings'])}\n")
        f.write(f"Total composition savings: {format_currency(results['total_savings'])}\n\n") 