"""
Utilities for demographic stratification in economic impact models.
"""

from dataclasses import dataclass
from typing import List, Dict
import numpy as np

@dataclass
class AgeStratification:
    """Age-based stratification for population analysis."""
    age_groups: List[str]
    population_fractions: List[float]
    effectiveness_multipliers: List[float]

    @classmethod
    def default(cls) -> 'AgeStratification':
        """Create default age stratification."""
        return cls(
            age_groups=['0-20', '21-40', '41-60', '61-80', '80+'],
            population_fractions=[0.25, 0.25, 0.25, 0.20, 0.05],
            effectiveness_multipliers=[1.2, 1.1, 1.0, 0.9, 0.8]
        )

    def validate(self) -> bool:
        """Validate stratification parameters."""
        return (
            len(self.age_groups) == len(self.population_fractions) == len(self.effectiveness_multipliers)
            and abs(sum(self.population_fractions) - 1.0) < 0.001
            and all(0 <= f <= 1 for f in self.population_fractions)
            and all(m > 0 for m in self.effectiveness_multipliers)
        )

    def apply_stratification(
        self,
        base_value: float,
        discount_rate: float = None,
        years: int = None
    ) -> float:
        """Apply age stratification to a base value."""
        total = 0
        for frac, mult in zip(self.population_fractions, self.effectiveness_multipliers):
            value = base_value * frac * mult
            if discount_rate is not None and years is not None:
                value *= 1 / (1 + discount_rate) ** years
            total += value
        return total 