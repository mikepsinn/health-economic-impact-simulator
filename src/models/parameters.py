"""Parameter classes for economic impact models."""

from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class TotalBenefits:
    """Combined benefits from all effects."""
    gdp_impact: float
    healthcare_savings: float
    medicare_savings: float
    qaly_improvement: float

@dataclass
class CognitiveParams:
    """Parameters for cognitive effects."""
    iq_increase: float  # points
    alzheimers_reduction: float  # percentage
    
    def __post_init__(self):
        if not -5 <= self.iq_increase <= 10:
            raise ValueError("IQ increase must be between -5 and +10 points")
        if not 0 <= self.alzheimers_reduction <= 50:
            raise ValueError("Alzheimer's reduction must be between 0 and 50%")

@dataclass
class KidneyParams:
    """Parameters for kidney function effects."""
    egfr_improvement: float  # mL/min/1.73m²
    ckd_progression_reduction: float  # percentage
    
    def __post_init__(self):
        if not -5 <= self.egfr_improvement <= 30:
            raise ValueError("eGFR improvement must be between -5 and +30 mL/min/1.73m²")
        if not 0 <= self.ckd_progression_reduction <= 50:
            raise ValueError("CKD progression reduction must be between 0 and 50%")

@dataclass
class PhysicalParams:
    """Parameters for physical effects."""
    muscle_mass_change_lb: float  # Positive = gain, negative = loss
    fat_mass_change_lb: float    # Positive = gain, negative = loss
    
    def __post_init__(self):
        if not -10 <= self.muscle_mass_change_lb <= 10:
            raise ValueError("Muscle mass change must be between -10 and +10 lbs")
        if not -30 <= self.fat_mass_change_lb <= 10:
            raise ValueError("Fat mass change must be between -30 and +10 lbs")

@dataclass
class LongevityParams:
    """Parameters for longevity effects."""
    lifespan_increase_percent: float  # percentage
    healthspan_improvement_percent: float  # percentage
    
    def __post_init__(self):
        if not 0 <= self.lifespan_increase_percent <= 20:
            raise ValueError("Lifespan increase must be between 0 and 20%")
        if not 0 <= self.healthspan_improvement_percent <= 100:
            raise ValueError("Health improvement must be between 0 and 100%")

@dataclass
class HealthcareParams:
    """Parameters for healthcare utilization effects."""
    hospital_visit_reduction_percent: float  # percentage
    savings_per_lb: float = 10.0  # Default $10 savings per pound improvement
    cost_per_hospital_visit: float = 12000.0  # Default $12,000 per visit
    
    def __post_init__(self):
        if not 0 <= self.hospital_visit_reduction_percent <= 100:
            raise ValueError("Hospital visit reduction must be between 0 and 100%")
        if self.savings_per_lb < 0:
            raise ValueError("Savings per pound must be non-negative")
        if self.cost_per_hospital_visit < 0:
            raise ValueError("Cost per hospital visit must be non-negative")

@dataclass
class ImpactModifiers:
    """Coefficients that modify how effects translate to outcomes."""
    iq_to_gdp: float  # GDP increase per IQ point
    kidney_to_medicare: float  # Medicare savings from kidney improvement
    alzheimers_to_medicare: float  # Medicare savings from Alzheimer's reduction
    health_quality: float  # Quality of life improvement
    lifespan_to_gdp: float  # GDP conversion from lifespan increase
    
    def __post_init__(self):
        if not 0 <= self.iq_to_gdp <= 0.1:
            raise ValueError("IQ to GDP modifier must be between 0 and 0.1")
        if not 0 <= self.kidney_to_medicare <= 1:
            raise ValueError("Kidney to Medicare modifier must be between 0 and 1")
        if not 0 <= self.alzheimers_to_medicare <= 1:
            raise ValueError("Alzheimer's to Medicare modifier must be between 0 and 1")
        if not 0 <= self.health_quality <= 1:
            raise ValueError("Health quality modifier must be between 0 and 1")
        if not 0 <= self.lifespan_to_gdp <= 1:
            raise ValueError("Lifespan to GDP modifier must be between 0 and 1")

@dataclass
class BasePopulationParams:
    """Base population parameters that all models should use."""
    total_population: int
    target_population: int
    medicare_beneficiaries: Optional[int] = None
    workforce_fraction: Optional[float] = None
    
    def __post_init__(self):
        if self.medicare_beneficiaries is None:
            self.medicare_beneficiaries = int(self.total_population * 0.186)  # Default Medicare enrollment rate
        if self.workforce_fraction is None:
            self.workforce_fraction = 0.5  # Default workforce participation
        
        if self.target_population > self.total_population:
            raise ValueError("Target population cannot exceed total population")
        if self.medicare_beneficiaries > self.total_population:
            raise ValueError("Medicare beneficiaries cannot exceed total population")
        if not 0 <= self.workforce_fraction <= 1:
            raise ValueError("Workforce fraction must be between 0 and 1")

@dataclass
class BaseEconomicParams:
    """Base economic parameters that all models should use."""
    annual_healthcare_cost: float
    annual_productivity: float
    discount_rate: float = 0.03  # Default 3% discount rate
    
    def __post_init__(self):
        if self.annual_healthcare_cost <= 0:
            raise ValueError("Healthcare cost must be positive")
        if self.annual_productivity <= 0:
            raise ValueError("Productivity must be positive")
        if not 0 <= self.discount_rate <= 0.2:
            raise ValueError("Discount rate must be between 0 and 20%")

@dataclass
class BaseInterventionParams:
    """Complete set of intervention parameters."""
    longevity: LongevityParams
    healthcare: HealthcareParams
    modifiers: ImpactModifiers
    cognitive: Optional[CognitiveParams] = None
    kidney: Optional[KidneyParams] = None
    physical: Optional[PhysicalParams] = None

    @property
    def lifespan_increase_years(self) -> float:
        """Convert lifespan increase from percentage to years."""
        return 79.1 * (self.longevity.lifespan_increase_percent / 100.0)  # Using standard life expectancy

    @classmethod
    def from_config(cls, config: Dict[str, Any], base_params: Dict[str, Any]) -> 'BaseInterventionParams':
        """Create parameters from configuration."""
        effects = config['default_effects']
        modifiers = base_params['impact_modifiers']  # Now using global modifiers
        
        # Create optional parameter objects if present in config
        cognitive = CognitiveParams(
            iq_increase=effects['cognitive']['iq_increase'],
            alzheimers_reduction=effects['cognitive']['alzheimers_reduction']
        ) if effects.get('cognitive') else None
        
        kidney = KidneyParams(
            egfr_improvement=effects['kidney']['egfr_improvement'],
            ckd_progression_reduction=effects['kidney']['ckd_progression_reduction']
        ) if effects.get('kidney') else None
        
        physical = PhysicalParams(
            muscle_mass_change_lb=effects['physical']['muscle_mass_change'],
            fat_mass_change_lb=effects['physical']['fat_mass_change']
        ) if effects.get('physical') else None
        
        return cls(
            longevity=LongevityParams(
                lifespan_increase_percent=effects['longevity']['lifespan_increase'],
                healthspan_improvement_percent=effects['longevity']['healthspan_improvement']
            ),
            healthcare=HealthcareParams(
                hospital_visit_reduction_percent=effects['healthcare']['hospital_visit_reduction']
            ),
            modifiers=ImpactModifiers(
                iq_to_gdp=modifiers['iq_to_gdp'],
                kidney_to_medicare=modifiers['kidney_to_medicare'],
                alzheimers_to_medicare=modifiers['alzheimers_to_medicare'],
                health_quality=modifiers['health_quality'],
                lifespan_to_gdp=modifiers['lifespan_to_gdp']
            ),
            cognitive=cognitive,
            kidney=kidney,
            physical=physical
        ) 