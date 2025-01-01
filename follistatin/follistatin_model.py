#!/usr/bin/env python3
"""
Follistatin Gene Therapy Impact Model
-------------------------------------
A template Python script that calculates:
1) Cumulative benefits from muscle gain/fat loss.
2) GDP impact from 2.5% lifespan increase.
3) Medicare spending changes.
"""

import numpy as np

def cumulative_savings_from_body_comp_change(
    population, muscle_gain_lb, fat_loss_lb, savings_per_lb
):
    """
    Calculates the total annual healthcare savings from changes in body composition.
    
    :param population: Total population (int)
    :param muscle_gain_lb: Average muscle gain (in lbs) per individual
    :param fat_loss_lb: Average fat loss (in lbs) per individual
    :param savings_per_lb: Estimated annual cost savings per pound improved
    :return: Float (Total annual savings in USD)
    """
    return population * (muscle_gain_lb + fat_loss_lb) * savings_per_lb


def added_gdp_from_increased_lifespan(
    population, increase_lifespan_years, workforce_fraction, annual_productivity
):
    """
    Rough estimate of cumulative GDP gain from increased lifespan.
    (Assuming all extra years are somewhat economically productive.)
    
    :param population: Total population (int)
    :param increase_lifespan_years: Additional years of life (float)
    :param workforce_fraction: Fraction of population contributing to workforce
    :param annual_productivity: Average annual productivity (in USD)
    :return: Float (Cumulative added GDP in USD)
    """
    return population * workforce_fraction * increase_lifespan_years * annual_productivity


def medicare_savings(
    medicare_population, annual_medicare_cost_per_person, reduction_percent
):
    """
    Calculates reduction in Medicare spending based on a given percentage reduction.
    
    :param medicare_population: Number of Medicare beneficiaries (int)
    :param annual_medicare_cost_per_person: Average annual cost per beneficiary (float)
    :param reduction_percent: Percentage reduction in costs (0.01 = 1%)
    :return: Float (Total reduced spending in USD)
    """
    return medicare_population * annual_medicare_cost_per_person * reduction_percent


if __name__ == "__main__":
    # --- User-Defined Inputs / Assumptions ---
    us_population = 332e6
    medicare_beneficiaries = 64e6
    
    # Body Composition Changes
    muscle_gain = 2.0     # lb
    fat_loss = 2.0        # lb
    savings_per_lb = 10.0 # USD per pound improvement (example)
    
    # Lifespan Increase
    baseline_lifespan = 77.0           # years
    lifespan_increase_percent = 2.5    # percent
    additional_years = baseline_lifespan * (lifespan_increase_percent / 100.0)
    
    # GDP & Productivity Assumptions
    workforce_fraction = 0.5
    annual_productivity = 70000.0      # USD per worker per year
    
    # Medicare Cost Assumptions
    annual_medicare_cost_per_person = 14000.0
    medicare_cost_reduction_percent = 0.05  # 5% cost reduction
    
    # --- Calculations ---
    
    # 1) Annual Cumulative Savings from Body Composition Changes
    total_savings_body_comp = cumulative_savings_from_body_comp_change(
        us_population, muscle_gain, fat_loss, savings_per_lb
    )
    
    # 2) Cumulative GDP Gain from Increased Lifespan
    total_added_gdp = added_gdp_from_increased_lifespan(
        us_population, additional_years, workforce_fraction, annual_productivity
    )
    
    # 3) Annual Medicare Spending Reduction from Healthier Population
    annual_medicare_savings = medicare_savings(
        medicare_beneficiaries,
        annual_medicare_cost_per_person,
        medicare_cost_reduction_percent
    )
    
    # --- Output Results ---
    print(f"=== Follistatin Gene Therapy Impact Model ===\n")
    print(f"1) Annual Healthcare Savings (Body Composition): ${total_savings_body_comp/1e9:.2f} billion")
    print(f"2) Added GDP from 2.5% Lifespan Increase: ${total_added_gdp/1e12:.2f} trillion (cumulative)")
    print(f"3) Annual Medicare Spending Reduction: ${annual_medicare_savings/1e9:.2f} billion\n")
