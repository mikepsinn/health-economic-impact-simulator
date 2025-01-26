"""Base model for all impact calculations."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod

class BaseParameters(BaseModel):
    """Base parameters shared across all models."""
    population_size: int = Field(default=331900000, description="Total US population")
    medicare_population: int = Field(default=73000000, description="Population over 60")
    adult_population: int = Field(default=258300000, description="Adult population (18+)")
    medicare_per_capita: float = Field(default=12500, description="Annual Medicare spending per beneficiary")
    gdp_per_capita: float = Field(default=65000, description="US GDP per capita")
    discount_rate: float = Field(default=0.03, description="Annual discount rate for future values")
    time_horizon_years: int = Field(default=10, description="Time horizon for calculations in years")

class BaseImpactModel(ABC):
    """Abstract base class for all impact models."""
    
    def __init__(self, params: Optional[BaseParameters] = None):
        self.params = params or BaseParameters()
        
    @abstractmethod
    def calculate_impacts(self) -> Dict[str, Any]:
        """Calculate health and economic impacts."""
        pass
    
    def calculate_npv(self, annual_value: float, years: int) -> float:
        """Calculate net present value of future cash flows."""
        npv = 0
        for year in range(years):
            npv += annual_value / ((1 + self.params.discount_rate) ** year)
        return npv
    
    def calculate_medicare_savings(self, reduction_percentage: float) -> float:
        """Calculate Medicare savings based on a reduction percentage."""
        annual_savings = (
            self.params.medicare_population * 
            self.params.medicare_per_capita * 
            reduction_percentage
        )
        return self.calculate_npv(annual_savings, self.params.time_horizon_years)
    
    def calculate_gdp_impact(self, productivity_increase: float) -> float:
        """Calculate GDP impact from productivity changes."""
        annual_impact = (
            self.params.adult_population * 
            self.params.gdp_per_capita * 
            productivity_increase
        )
        return self.calculate_npv(annual_impact, self.params.time_horizon_years) 