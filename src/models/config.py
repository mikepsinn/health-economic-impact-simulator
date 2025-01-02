"""Typed configuration models."""

from typing import List, Optional
from pydantic import BaseModel, Field, validator

class CognitiveEffects(BaseModel):
    """Cognitive intervention effects."""
    iq_increase: float = Field(..., ge=-5, le=10, description="IQ point increase")
    alzheimers_reduction: float = Field(..., ge=0, le=50, description="Alzheimer's progression reduction percentage")

class KidneyEffects(BaseModel):
    """Kidney function effects."""
    egfr_improvement: float = Field(..., ge=-5, le=30, description="eGFR improvement in mL/min/1.73m²")
    ckd_progression_reduction: float = Field(..., ge=0, le=50, description="CKD progression reduction percentage")

class PhysicalEffects(BaseModel):
    """Physical composition effects."""
    muscle_mass_change: float = Field(..., ge=-10, le=10, description="Muscle mass change in pounds")
    fat_mass_change: float = Field(..., ge=-30, le=10, description="Fat mass change in pounds")

class LongevityEffects(BaseModel):
    """Longevity and healthspan effects."""
    lifespan_increase: float = Field(..., ge=0, le=20, description="Lifespan increase percentage")
    healthspan_improvement: float = Field(..., ge=0, le=100, description="Percentage of lifespan increase that is healthy")

class HealthcareEffects(BaseModel):
    """Healthcare utilization effects."""
    hospital_visit_reduction: float = Field(..., ge=0, le=100, description="Hospital visit reduction percentage")

class BiomarkerEffects(BaseModel):
    """Optional biomarker effects."""
    egfr_change: Optional[float] = Field(None, description="eGFR change in mL/min/1.73m²")
    cystatin_c_change: Optional[float] = Field(None, description="Cystatin C change in mg/L")
    creatinine_change: Optional[float] = Field(None, description="Creatinine change in mg/dL")
    other_markers: Optional[dict] = Field(default_factory=dict, description="Other biomarker changes")

class InterventionEffects(BaseModel):
    """Complete set of intervention effects."""
    cognitive: Optional[CognitiveEffects] = None
    kidney: Optional[KidneyEffects] = None
    physical: Optional[PhysicalEffects] = None
    longevity: LongevityEffects
    healthcare: HealthcareEffects
    biomarkers: Optional[BiomarkerEffects] = None

class InterventionConfig(BaseModel):
    """Intervention-specific configuration."""
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    default_effects: InterventionEffects
    references: List[str] = Field(default_factory=list)

    @validator('name')
    def name_must_be_valid(cls, v):
        """Validate intervention name."""
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return v.strip()

class PopulationConfig(BaseModel):
    """Population parameters configuration."""
    total: int = Field(..., gt=0)
    target: int = Field(..., gt=0)
    medicare_beneficiaries: int = Field(..., gt=0)
    workforce_fraction: float = Field(..., ge=0, le=1)

    @validator('target')
    def target_must_be_valid(cls, v, values):
        """Validate target population."""
        if 'total' in values and v > values['total']:
            raise ValueError("Target population cannot exceed total population")
        return v

class EconomicsConfig(BaseModel):
    """Economic parameters configuration."""
    annual_healthcare_cost: float = Field(..., gt=0)
    annual_productivity: float = Field(..., gt=0)
    discount_rate: float = Field(..., ge=0, le=0.2)

class HealthcareConfig(BaseModel):
    """Healthcare system parameters configuration."""
    annual_hospital_visits: int = Field(..., gt=0)
    annual_alzheimers_cost: float = Field(..., ge=0)
    annual_ckd_cost: float = Field(..., ge=0)
    savings_per_lb_muscle: float = Field(..., ge=0)
    savings_per_lb_fat: float = Field(..., ge=0)

class ImpactModifiers(BaseModel):
    """Global impact conversion modifiers."""
    iq_to_gdp: float = Field(..., ge=0, le=0.1, description="GDP increase per IQ point")
    kidney_to_medicare: float = Field(..., ge=0, le=1, description="Medicare savings from kidney improvement")
    alzheimers_to_medicare: float = Field(..., ge=0, le=1, description="Medicare savings from Alzheimer's reduction")
    health_quality: float = Field(..., ge=0, le=1, description="Quality of life improvement")
    lifespan_to_gdp: float = Field(..., ge=0, le=1, description="GDP conversion from lifespan increase")

class BaseConfig(BaseModel):
    """Global configuration parameters."""
    population: PopulationConfig
    economics: EconomicsConfig
    healthcare: HealthcareConfig
    impact_modifiers: ImpactModifiers 