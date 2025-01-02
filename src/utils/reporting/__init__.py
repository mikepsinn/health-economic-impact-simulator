"""Report generation utilities."""

from .report_generator import generate_report
from .writers import (
    write_executive_summary,
    write_study_design,
    write_intervention_analysis,
    write_economic_calculations
)

__all__ = [
    'generate_report',
    'write_executive_summary',
    'write_study_design',
    'write_intervention_analysis',
    'write_economic_calculations'
] 