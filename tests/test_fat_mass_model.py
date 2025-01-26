import pytest
from model import ModelParameters, MarkovModel, EconomicCalculator
import numpy as np

class TestModelParameters:
    def test_default_params(self):
        params = ModelParameters()
        assert params.time_horizon == 20
        assert params.discount_rate == 0.03
        assert len(params.age_distribution) == 3

class TestMarkovModel:
    @pytest.fixture
    def model(self):
        params = ModelParameters()
        return MarkovModel(params)
    
    def test_transition_matrix_stochastic(self, model):
        model.build_transition_matrix()
        for row in model.transition_matrix:
            assert np.isclose(row.sum(), 1.0, atol=1e-6)

class TestEconomicCalculator:
    def test_icer_calculation(self):
        result = EconomicCalculator.calculate_icer(
            intervention_cost=1e6,
            control_cost=8e5,
            intervention_qaly=5000,
            control_qaly=4500
        )
        assert result == (1e6 - 8e5) / (5000 - 4500)
    
    def test_roi_calculation(self):
        assert EconomicCalculator.calculate_roi(1.5e6, 1e6) == 0.5

if __name__ == "__main__":
    pytest.main(["-v"])