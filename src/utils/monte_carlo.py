"""
Monte Carlo simulation utilities for economic impact models.
"""

from typing import Dict, List, Callable, Any
import numpy as np
import pandas as pd

def run_monte_carlo(
    base_params: Dict[str, float],
    param_variations: Dict[str, float],
    calculate_impacts: Callable[[Dict[str, float]], Dict[str, float]],
    n_simulations: int = 1000,
    random_seed: int = None
) -> Dict[str, pd.DataFrame]:
    """
    Run Monte Carlo simulation with parameter variations.
    
    Args:
        base_params: Dictionary of base parameter values
        param_variations: Dictionary of parameter names and their standard deviations (as fraction of base value)
        calculate_impacts: Function that calculates impacts given parameters
        n_simulations: Number of Monte Carlo simulations to run
        random_seed: Random seed for reproducibility
    
    Returns:
        Dictionary of DataFrames containing simulation results for each metric
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    results = {}
    
    for _ in range(n_simulations):
        # Generate random variations of parameters
        current_params = base_params.copy()
        for param, std in param_variations.items():
            if param in current_params:
                variation = np.random.normal(1, std)
                current_params[param] *= variation
        
        # Calculate impacts with varied parameters
        impacts = calculate_impacts(current_params)
        
        # Store results
        for metric, value in impacts.items():
            if metric not in results:
                results[metric] = []
            results[metric].append(value)
    
    # Convert results to DataFrames
    return {k: pd.DataFrame(v) for k, v in results.items()}

def calculate_confidence_intervals(
    results: Dict[str, pd.DataFrame],
    confidence_level: float = 0.95
) -> Dict[str, Dict[str, float]]:
    """
    Calculate confidence intervals for Monte Carlo results.
    
    Args:
        results: Dictionary of simulation results
        confidence_level: Confidence level (e.g., 0.95 for 95% CI)
    
    Returns:
        Dictionary of confidence intervals for each metric
    """
    confidence_intervals = {}
    
    for metric, data in results.items():
        lower_percentile = (1 - confidence_level) / 2 * 100
        upper_percentile = (1 + confidence_level) / 2 * 100
        
        confidence_intervals[metric] = {
            'mean': data.mean().iloc[0],
            'std': data.std().iloc[0],
            'lower_ci': np.percentile(data, lower_percentile),
            'upper_ci': np.percentile(data, upper_percentile)
        }
    
    return confidence_intervals 