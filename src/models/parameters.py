"""Parameter classes for economic impact models."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, validator, computed_field

class CognitiveParams(BaseModel):
    """Parameters for cognitive effects."""
    iq_increase: float = Field(description="IQ increase in points")
    alzheimers_reduction: float = Field(description="Alzheimer's progression reduction percentage")
    
    @validator('iq_increase')
    def validate_iq(cls, v: float) -> float:
        """Validate IQ increase."""
        if not -5 <= v <= 10:
            raise ValueError("IQ increase must be between -5 and +10 points")
        return v
        
    @validator('alzheimers_reduction')
    def validate_alzheimers(cls, v: float) -> float:
        """Validate Alzheimer's reduction."""
        if not 0 <= v <= 50:
            raise ValueError("Alzheimer's reduction must be between 0 and 50%")
        return v

class KidneyParams(BaseModel):
    """Parameters for kidney function effects."""
    egfr_improvement: float = Field(description="eGFR improvement in mL/min/1.73m²")
    ckd_progression_reduction: float = Field(description="CKD progression reduction percentage")
    
    @validator('egfr_improvement')
    def validate_egfr(cls, v: float) -> float:
        """Validate eGFR improvement."""
        if not -5 <= v <= 30:
            raise ValueError("eGFR improvement must be between -5 and +30 mL/min/1.73m²")
        return v
        
    @validator('ckd_progression_reduction')
    def validate_ckd(cls, v: float) -> float:
        """Validate CKD reduction."""
        if not 0 <= v <= 50:
            raise ValueError("CKD progression reduction must be between 0 and 50%")
        return v

class PhysicalParams(BaseModel):
    """Parameters for physical effects."""
    muscle_mass_change_lb: float = Field(description="Muscle mass change in pounds (positive = gain)")
    fat_mass_change_lb: float = Field(description="Fat mass change in pounds (positive = gain)")
    
    @validator('muscle_mass_change_lb')
    def validate_muscle(cls, v: float) -> float:
        """Validate muscle mass change."""
        if not -10 <= v <= 10:
            raise ValueError("Muscle mass change must be between -10 and +10 lbs")
        return v
        
    @validator('fat_mass_change_lb')
    def validate_fat(cls, v: float) -> float:
        """Validate fat mass change."""
        if not -30 <= v <= 10:
            raise ValueError("Fat mass change must be between -30 and +10 lbs")
        return v

class LongevityParams(BaseModel):
    """Parameters for longevity effects."""
    lifespan_increase_years: float = Field(description="Lifespan increase in years")
    healthspan_improvement_percent: float = Field(description="Healthspan improvement percentage")
    
    @validator('lifespan_increase_years')
    def validate_lifespan(cls, v: float) -> float:
        """Validate lifespan increase."""
        if not 0 <= v <= 10:
            raise ValueError("Lifespan increase must be between 0 and 10 years")
        return v
        
    @validator('healthspan_improvement_percent')
    def validate_healthspan(cls, v: float) -> float:
        """Validate healthspan improvement."""
        if not 0 <= v <= 100:
            raise ValueError("Healthspan improvement must be between 0 and 100%")
        return v

class HealthcareParams(BaseModel):
    """Parameters for healthcare utilization effects."""
    hospital_visit_reduction_percent: float = Field(description="Hospital visit reduction percentage")
    annual_hospital_visits: int = Field(description="Annual hospital visits")
    annual_alzheimers_cost: float = Field(description="Annual Alzheimer's cost")
    annual_ckd_cost: float = Field(description="Annual CKD cost")
    cost_per_hospital_visit: float = Field(description="Cost per hospital visit")
    savings_per_lb_muscle: float = Field(description="Healthcare savings per pound of muscle")
    savings_per_lb_fat: float = Field(description="Healthcare savings per pound of fat loss")
    
    @validator('hospital_visit_reduction_percent')
    def validate_reduction(cls, v: float) -> float:
        """Validate hospital visit reduction."""
        if not 0 <= v <= 50:
            raise ValueError("Hospital visit reduction must be between 0 and 50%")
        return v
        
    @validator('annual_hospital_visits', 'annual_alzheimers_cost', 'annual_ckd_cost', 'cost_per_hospital_visit')
    def validate_positive(cls, v: float) -> float:
        """Validate positive values."""
        if v <= 0:
            raise ValueError("Healthcare costs must be positive")
        return v

class ImpactModifiers(BaseModel):
    """Impact modifiers for benefit calculations."""
    iq_to_gdp: float = Field(description="GDP impact per IQ point")
    kidney_to_medicare: float = Field(description="Medicare savings from kidney improvements")
    alzheimers_to_medicare: float = Field(description="Medicare savings from reduced Alzheimer's")
    health_quality: float = Field(description="Health quality multiplier")
    lifespan_to_gdp: float = Field(description="GDP impact from increased lifespan")

class BasePopulationParams(BaseModel):
    """Base population parameters."""
    total_population: int = Field(description="Total US population")
    target_population: int = Field(description="Target population for intervention")
    medicare_beneficiaries: int = Field(description="Number of Medicare beneficiaries")
    workforce_fraction: float = Field(description="Fraction of population in workforce")
    
    @validator('target_population')
    def validate_target(cls, v: int, values: Dict) -> int:
        """Validate target population."""
        if 'total_population' in values and v > values['total_population']:
            raise ValueError("Target population cannot exceed total population")
        return v

class BaseEconomicParams(BaseModel):
    """Base economic parameters."""
    annual_healthcare_cost: float = Field(description="Annual healthcare cost per person")
    annual_productivity: float = Field(description="Annual productivity per worker")
    discount_rate: float = Field(description="Annual discount rate")
    
    @validator('annual_healthcare_cost', 'annual_productivity')
    def validate_positive(cls, v: float) -> float:
        """Validate positive values."""
        if v <= 0:
            raise ValueError("Economic values must be positive")
        return v
        
    @validator('discount_rate')
    def validate_rate(cls, v: float) -> float:
        """Validate discount rate."""
        if not 0 <= v <= 0.2:
            raise ValueError("Discount rate must be between 0 and 20%")
        return v

class BaseInterventionParams(BaseModel):
    """Base intervention parameters."""
    cognitive: Optional[CognitiveParams] = None
    kidney: Optional[KidneyParams] = None
    physical: Optional[PhysicalParams] = None
    longevity: LongevityParams
    healthcare: HealthcareParams
    modifiers: ImpactModifiers
    
    @computed_field
    @property
    def lifespan_increase_years(self) -> float:
        """Get lifespan increase in years."""
        return self.longevity.lifespan_increase_years
    
    @classmethod
    def from_config(cls, intervention_config: Dict, base_config: Dict) -> 'BaseInterventionParams':
        """Create parameters from configuration."""
        effects = intervention_config.get('default_effects', {})
        if not effects:
            raise ValueError("No effects found in intervention config")
        
        # Extract parameters from config
        cognitive = None
        if effects.get('cognitive'):
            cognitive = CognitiveParams(
                iq_increase=effects['cognitive']['iq_increase'],
                alzheimers_reduction=effects['cognitive']['alzheimers_reduction']
            )
        
        kidney = None
        if effects.get('kidney'):
            kidney = KidneyParams(
                egfr_improvement=effects['kidney']['egfr_improvement'],
                ckd_progression_reduction=effects['kidney']['ckd_progression_reduction']
            )
        
        physical = None
        if effects.get('physical'):
            physical = PhysicalParams(
                muscle_mass_change_lb=effects['physical']['muscle_mass_change'],
                fat_mass_change_lb=effects['physical']['fat_mass_change']
            )
        
        # Convert longevity parameters
        if not effects.get('longevity'):
            raise ValueError("Longevity effects are required")
        longevity = LongevityParams(
            lifespan_increase_years=effects['longevity']['lifespan_increase'] * 79.1 / 100,  # Convert % to years
            healthspan_improvement_percent=effects['longevity']['healthspan_improvement']
        )
        
        # Convert healthcare parameters
        if not effects.get('healthcare'):
            raise ValueError("Healthcare effects are required")
        healthcare_params = base_config['healthcare'].copy()
        healthcare_params['hospital_visit_reduction_percent'] = effects['healthcare']['hospital_visit_reduction']
        healthcare = HealthcareParams(**healthcare_params)
        
        modifiers = ImpactModifiers(**base_config['impact_modifiers'])
        
        return cls(
            cognitive=cognitive,
            kidney=kidney,
            physical=physical,
            longevity=longevity,
            healthcare=healthcare,
            modifiers=modifiers
        ) 