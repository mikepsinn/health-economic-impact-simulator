import pandas as pd
from model import ModelParameters, MarkovModel, EconomicCalculator

def run_medicare_analysis():
    # Load Medicare population data
    pop_data = pd.read_csv('data/medicare_population.csv')
    total_population = pop_data['base_population'].sum()
    
    # Initialize model with Medicare parameters
    params = ModelParameters()
    params.population_size = total_population
    
    # Run simulations
    model = MarkovModel(params)
    model.build_transition_matrix()
    results = model.run_cohort_simulation()
    
    # Calculate discounted outcomes
    results['discounted_qalys'] = results['qalys'] / (1 + params.discount_rate)**results['year']
    results['discounted_costs'] = results['costs'] / (1 + params.discount_rate)**results['year']
    
    # Calculate cumulative outcomes
    cumulative = results[['discounted_qalys', 'discounted_costs']].cumsum()
    results = pd.concat([results, cumulative.add_prefix('cumulative_')], axis=1)
    
    # Save results
    import os
    os.makedirs('output', exist_ok=True)
    results.to_csv('output/medicare_impact_results.csv', index=False)
    print(f"Analysis complete. Results saved to output/medicare_impact_results.csv")

if __name__ == "__main__":
    run_medicare_analysis()