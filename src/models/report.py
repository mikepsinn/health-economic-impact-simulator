"""Report data models."""

from typing import Optional, Dict
from pydantic import BaseModel, Field, validator
from decimal import Decimal

class BenefitMetrics(BaseModel):
    """Individual benefit category metrics."""
    gdp_impact: float = Field(description="GDP impact in dollars")
    healthcare_savings: float = Field(description="Healthcare cost savings in dollars")
    medicare_savings: float = Field(description="Medicare savings in dollars")
    qaly_improvement: float = Field(description="Quality-adjusted life years gained")

class ReportMetrics(BaseModel):
    """Core economic impact metrics for the report."""
    annual_healthcare_savings: float = Field(description="Total annual healthcare system savings in dollars")
    total_gdp_impact: float = Field(description="Total GDP impact in dollars")
    annual_medicare_savings: float = Field(description="Total annual Medicare savings in dollars")
    total_qalys: float = Field(description="Total quality-adjusted life years gained")
    
    @validator('annual_healthcare_savings', 'total_gdp_impact', 'annual_medicare_savings')
    def validate_positive_dollars(cls, v: float) -> float:
        """Ensure monetary values are positive."""
        if v < 0:
            raise ValueError("Monetary values must be positive")
        return v
    
    @validator('total_qalys')
    def validate_positive_qalys(cls, v: float) -> float:
        """Ensure QALY values are positive."""
        if v < 0:
            raise ValueError("QALY values must be positive")
        return v

class DetailedBenefits(BaseModel):
    """Detailed breakdown of benefits by category."""
    cognitive_benefits: Optional[BenefitMetrics] = None
    kidney_benefits: Optional[BenefitMetrics] = None
    physical_benefits: Optional[BenefitMetrics] = None
    longevity_benefits: Optional[BenefitMetrics] = None
    healthcare_benefits: Optional[BenefitMetrics] = None
    total_benefits: BenefitMetrics = Field(description="Combined benefits across all categories")

class Report(BaseModel):
    """Complete report data model."""
    metrics: ReportMetrics
    benefits: DetailedBenefits
    validation_warnings: Optional[str] = Field(default="", description="Validation warnings if any bounds are exceeded")
    
    class Config:
        """Pydantic config."""
        validate_assignment = True
        extra = "forbid"  # Prevent additional fields from being added 