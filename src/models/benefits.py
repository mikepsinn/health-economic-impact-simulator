"""Benefit calculation result models."""

from typing import Optional
from pydantic import BaseModel, Field

class BenefitMetrics(BaseModel):
    """Base metrics for all benefit calculations."""
    gdp_impact: float = Field(default=0.0, description="GDP impact in dollars")
    healthcare_savings: float = Field(default=0.0, description="Healthcare cost savings in dollars")
    medicare_savings: float = Field(default=0.0, description="Medicare savings in dollars")
    qaly_improvement: float = Field(default=0.0, description="Quality-adjusted life years gained")

class CognitiveBenefits(BenefitMetrics):
    """Benefits from cognitive improvements."""
    pass

class KidneyBenefits(BenefitMetrics):
    """Benefits from kidney function improvements."""
    pass

class PhysicalBenefits(BenefitMetrics):
    """Benefits from physical composition changes."""
    pass

class LongevityBenefits(BenefitMetrics):
    """Benefits from increased lifespan."""
    pass

class HealthcareBenefits(BenefitMetrics):
    """Benefits from reduced healthcare utilization."""
    hospital_savings: float = Field(description="Savings from reduced hospital visits") 