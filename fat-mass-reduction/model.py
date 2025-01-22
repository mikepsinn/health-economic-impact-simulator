import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class ModelParameters:
    """Stores all input parameters for the economic model"""
    
    def __init__(self):
        # Core model parameters
        self.time_horizon: int = 20  # Years
        self.discount_rate: float = 0.03
        
        # Population parameters
        self.population_size: int = 1_000_000
        self.age_distribution: Dict[str, float] = {'65-74': 0.6, '75-84': 0.3, '85+': 0.1}
        self.baseline_bmi_dist: Dict[str, float] = {
            'Normal (18.5-24.9)': 0.2,
            'Overweight (25-29.9)': 0.3,
            'Obese I (30-34.9)': 0.3,
            'Obese II (35-39.9)': 0.15,
            'Obese III (40+)': 0.05
        }
        
        # Transition probabilities (per year)
        self.transition_probs: Dict[str, float] = {
            'healthy_to_obese': 0.05,
            'obese_to_comorbid': 0.08,
            'comorbid_to_death': 0.15,
            'post_intervention_relapse': 0.1
        }
        
        # Economic parameters ($)
        self.healthcare_costs: Dict[str, float] = {
            'healthy': 5000,
            'obese': 8000,
            'comorbid': 15000,
            'intervention': 3000  # One-time cost
        }
        
        # QALY weights
        self.qaly_weights: Dict[str, float] = {
            'healthy': 0.85,
            'obese': 0.75,
            'comorbid': 0.6,
            'post_intervention': 0.8
        }

class MarkovModel:
    """Discrete-time Markov cohort model implementation"""
    
    def __init__(self, params: ModelParameters):
        self.params = params
        self.states = ['healthy', 'obese', 'comorbid', 'post_intervention', 'dead']
        self.transition_matrix: np.ndarray = np.zeros((len(self.states), len(self.states)))
        
    def build_transition_matrix(self):
        """Construct the annual transition probability matrix"""
        # Implement transition logic based on parameters
        # Placeholder values - needs actual probability calculations
        self.transition_matrix = np.array([
            [0.8, 0.05, 0.0, 0.15, 0.0],    # Healthy
            [0.1, 0.7, 0.08, 0.1, 0.02],    # Obese
            [0.0, 0.0, 0.7, 0.1, 0.2],      # Comorbid
            [0.15, 0.05, 0.0, 0.7, 0.1],    # Post-intervention
            [0.0, 0.0, 0.0, 0.0, 1.0]       # Dead
        ])
        
    def run_cohort_simulation(self) -> pd.DataFrame:
        """Run the cohort simulation over time horizon"""
        results = []
        cohort = np.zeros(len(self.states))
        cohort[0] = self.params.population_size  # Start all in healthy state
        
        for year in range(self.params.time_horizon):
            # Apply transitions
            cohort = np.dot(cohort, self.transition_matrix)
            
            # Calculate outcomes
            qalys = self._calculate_qalys(cohort)
            costs = self._calculate_costs(cohort, year)
            
            results.append({
                'year': year + 1,
                'qalys': qalys,
                'costs': costs,
                'cohort_distribution': cohort.copy()
            })
            
        return pd.DataFrame(results)
    
    def _calculate_qalys(self, cohort: np.ndarray) -> float:
        """Calculate QALYs for current cohort distribution"""
        return sum(
            cohort[i] * self.params.qaly_weights[state]
            for i, state in enumerate(self.states[:-1])  # Exclude dead state
        )
    
    def _calculate_costs(self, cohort: np.ndarray, year: int) -> float:
        """Calculate annual healthcare costs"""
        return sum(
            cohort[i] * self.params.healthcare_costs.get(state, 0)
            for i, state in enumerate(self.states[:-1])  # Exclude dead state
        )

class EconomicCalculator:
    """Handles economic outcome calculations"""
    
    @staticmethod
    def calculate_icer(intervention_cost: float, control_cost: float,
                       intervention_qaly: float, control_qaly: float) -> float:
        """Calculate incremental cost-effectiveness ratio"""
        return (intervention_cost - control_cost) / (intervention_qaly - control_qaly)
    
    @staticmethod
    def calculate_roi(total_benefits: float, total_costs: float) -> float:
        """Calculate return on investment"""
        return (total_benefits - total_costs) / total_costs

# Example usage
if __name__ == "__main__":
    params = ModelParameters()
    model = MarkovModel(params)
    model.build_transition_matrix()
    results = model.run_cohort_simulation()
    
    print("Simulation Results:")
    print(results.head())