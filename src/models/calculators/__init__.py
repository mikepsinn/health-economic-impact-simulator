"""Impact calculators for different intervention pathways."""

from abc import ABC, abstractmethod
from typing import TextIO, Dict

from src.models.parameters import (
    BasePopulationParams,
    BaseEconomicParams,
    HealthcareParams,
    ImpactModifiers
)

class BaseCalculator(ABC):
    """Base class for impact calculators."""
    
    def __init__(
        self,
        pop: BasePopulationParams,
        econ: BaseEconomicParams,
        healthcare: HealthcareParams,
        modifiers: ImpactModifiers
    ):
        self.pop = pop
        self.econ = econ
        self.healthcare = healthcare
        self.modifiers = modifiers
    
    @abstractmethod
    def calculate(self, params: Dict) -> Dict:
        """Calculate impacts from intervention parameters."""
        pass

    @abstractmethod
    def write_calculations(self, f: TextIO, params: Dict, results: Dict) -> None:
        """Write calculation details to report file.
        
        Args:
            f: Report file handle
            params: Input parameters used in calculations
            results: Results from calculate() method
        """
        pass

from .physical import PhysicalCalculator
from .cognitive import CognitiveCalculator
from .kidney import KidneyCalculator
from .longevity import LongevityCalculator
from .healthcare import HealthcareCalculator

__all__ = [
    'BaseCalculator',
    'PhysicalCalculator',
    'CognitiveCalculator',
    'KidneyCalculator',
    'LongevityCalculator',
    'HealthcareCalculator'
] 