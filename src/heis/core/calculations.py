"""Core calculation functions for the health economic impact simulator."""

import pandas as pd
from typing import Dict, Any
from ..config.loader import load_base_parameters

def format_large_number(num: float) -> str:
    """Format large numbers into B/M format."""
    abs_num = abs(num)
    if abs_num >= 1e9:
        return f"${abs_num/1e9:.1f}B"
    elif abs_num >= 1e6:
        return f"${abs_num/1e6:.1f}M"
    else:
        return f"${abs_num:,.0f}"

def calculate_impacts(intervention: Dict[Any, Any], population_type: str, base_params: Dict[Any, Any]) -> Dict[str, float]:
    """Calculate economic and health impacts of an intervention."""
    pop = base_params['population'][population_type]
    effects = intervention['default_effects']
    modifiers = intervention['impact_modifiers']
    
    medicare_savings = 0
    gdp_impact = 0
    qaly_impact = 0
    
    # Calculate Medicare impact from hospital visits
    if 'healthcare' in effects:
        hospital_reduction = effects['healthcare']['hospital_visit_reduction'] / 100
        medicare_savings += (
            pop * 
            base_params['economics']['medicare_per_capita'] * 
            base_params['health_baselines']['medicare_enrollment_rate'] *
            hospital_reduction
        )
    
    # Calculate cognitive impacts
    if 'cognitive' in effects:
        # IQ impact on GDP
        if 'iq_increase' in effects['cognitive']:
            iq_impact = effects['cognitive']['iq_increase'] * modifiers.get('iq_to_gdp', 0)
            gdp_impact += pop * base_params['economics']['gdp_per_capita'] * iq_impact
        
        # Alzheimer's impact
        if 'alzheimers_reduction' in effects['cognitive'] and population_type == 'over_60':
            alz_reduction = effects['cognitive']['alzheimers_reduction'] / 100
            medicare_savings += (
                base_params['economics']['alzheimers_annual_cost'] * 
                alz_reduction * 
                modifiers.get('alzheimers_to_medicare', 0)
            )
    
    # Calculate kidney disease impacts
    if 'kidney' in effects and 'ckd_progression_reduction' in effects['kidney']:
        ckd_reduction = effects['kidney']['ckd_progression_reduction'] / 100
        medicare_savings += (
            base_params['economics']['ckd_annual_cost'] * 
            ckd_reduction * 
            modifiers.get('kidney_to_medicare', 0)
        )
    
    # Calculate GDP impact from longevity
    if 'longevity' in effects:
        lifespan_impact = effects['longevity']['lifespan_increase'] / 100
        gdp_impact += (
            pop * 
            base_params['economics']['gdp_per_capita'] * 
            lifespan_impact * 
            modifiers.get('lifespan_to_gdp', 0.8)
        )
    
    # Calculate QALYs
    qaly_base = pop * base_params['health_baselines']['average_lifespan']
    qaly_impact = qaly_base * modifiers.get('health_quality', 0)
    if 'longevity' in effects:
        qaly_impact += qaly_base * (effects['longevity']['lifespan_increase'] / 100)
    
    return {
        'Medicare Savings': medicare_savings,
        'GDP Impact': gdp_impact,
        'QALY Impact': qaly_impact
    }

def calculate_time_series(intervention: Dict[Any, Any], population_type: str, 
                         base_params: Dict[Any, Any], years: int = 10, 
                         growth_rate: float = 0.02) -> pd.DataFrame:
    """Calculate impact projections over time."""
    annual_impact = calculate_impacts(intervention, population_type, base_params)
    
    years_range = range(years)
    cumulative_data = []
    
    for year in years_range:
        compound_factor = 1 + (year * growth_rate)
        
        medicare_savings = annual_impact['Medicare Savings'] * compound_factor
        gdp_impact = annual_impact['GDP Impact'] * compound_factor
        qaly_impact = annual_impact['QALY Impact'] * compound_factor
        
        cumulative_medicare = medicare_savings * (year + 1)
        cumulative_gdp = gdp_impact * (year + 1)
        cumulative_qaly = qaly_impact * (year + 1)
        
        cumulative_data.append({
            'Year': year + 1,
            'Annual Medicare Savings': medicare_savings,
            'Cumulative Medicare Savings': cumulative_medicare,
            'Annual GDP Impact': gdp_impact,
            'Cumulative GDP Impact': cumulative_gdp,
            'Annual QALY Impact': qaly_impact,
            'Cumulative QALY Impact': cumulative_qaly
        })
    
    return pd.DataFrame(cumulative_data)

def calculate_sensitivity_scenarios(intervention: Dict[Any, Any], population_type: str,
                                 base_params: Dict[Any, Any], effect_mult: float,
                                 growth_rate: float) -> pd.DataFrame:
    """Calculate sensitivity analysis scenarios."""
    scenarios = {
        'Conservative': {'effect_mult': effect_mult * 0.8, 'growth': growth_rate * 0.8},
        'Base Case': {'effect_mult': effect_mult, 'growth': growth_rate},
        'Optimistic': {'effect_mult': effect_mult * 1.2, 'growth': growth_rate * 1.2}
    }
    
    results = {}
    for scenario, params in scenarios.items():
        modified_intervention = intervention.copy()
        for category in modified_intervention['default_effects']:
            if isinstance(modified_intervention['default_effects'][category], dict):
                for key in modified_intervention['default_effects'][category]:
                    modified_intervention['default_effects'][category][key] *= params['effect_mult']
        
        df = calculate_time_series(
            modified_intervention,
            population_type,
            base_params,
            years=10,
            growth_rate=params['growth']
        )
        results[scenario] = df.iloc[-1]
    
    return pd.DataFrame(results).T 