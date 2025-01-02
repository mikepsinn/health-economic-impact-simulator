"""Streamlit app for economic impact visualization."""

import streamlit as st
import importlib.util
import sys
from pathlib import Path
from typing import Dict, Any

from src.models.base_model import BaseImpactModel
from src.models.parameters import (
    BasePopulationParams,
    BaseEconomicParams,
    BaseInterventionParams
)
from src.utils.reporting import generate_report

def load_python_config(path: Path) -> Dict[str, Any]:
    """Load configuration from Python file."""
    spec = importlib.util.spec_from_file_location("config", path)
    if not spec or not spec.loader:
        raise ImportError(f"Could not load {path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules["config"] = module
    spec.loader.exec_module(module)
    
    return module.config.model_dump()

def main():
    """Main Streamlit app."""
    st.title("Health Economic Impact Simulator")
    st.write("Analyze economic impacts of longevity interventions")
    
    # Load base configuration
    base_config_path = Path("config/global_parameters.py")
    base_config = load_python_config(base_config_path)
    
    # Find all intervention configs
    config_dir = Path("config/interventions")
    config_files = list(config_dir.glob("*.py"))
    
    # Sidebar for intervention selection
    st.sidebar.title("Intervention Selection")
    selected_file = st.sidebar.selectbox(
        "Choose intervention",
        [f.stem for f in config_files],
        format_func=lambda x: x.title()
    )
    
    # Load selected intervention
    intervention_path = config_dir / f"{selected_file}.py"
    intervention_config = load_python_config(intervention_path)
    
    # Create model parameters
    intervention_params = BaseInterventionParams.from_config(
        intervention_config=intervention_config,
        base_config=base_config
    )
    
    population_params = BasePopulationParams(**base_config['population'])
    economic_params = BaseEconomicParams(**base_config['economics'])
    
    # Create and run model
    model = BaseImpactModel(
        population_params=population_params,
        economic_params=economic_params,
        intervention_params=intervention_params
    )
    
    # Generate report
    report = model.generate_full_report(base_config)
    
    # Display key metrics
    st.header("Key Economic Impacts")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Annual Healthcare Savings",
            f"${report.metrics.annual_healthcare_savings / 1e9:.1f}B"
        )
        st.metric(
            "Medicare Cost Reduction",
            f"${report.metrics.annual_medicare_savings / 1e9:.1f}B"
        )
    
    with col2:
        st.metric(
            "Total GDP Impact",
            f"${report.metrics.total_gdp_impact / 1e9:.1f}B"
        )
        st.metric(
            "QALYs Gained",
            f"{report.metrics.total_qalys:,.0f}"
        )
    
    # Display validation warnings
    if report.validation_warnings:
        st.warning(report.validation_warnings)
    
    # Show intervention details
    st.header("Intervention Details")
    st.write(f"**Description:** {intervention_config['description']}")
    
    effects = intervention_config['default_effects']
    
    # Physical effects
    if effects.get('physical'):
        st.subheader("Physical Effects")
        st.write(f"- Muscle mass change: {effects['physical']['muscle_mass_change']:+.1f} lbs")
        st.write(f"- Fat mass change: {effects['physical']['fat_mass_change']:+.1f} lbs")
    
    # Cognitive effects
    if effects.get('cognitive'):
        st.subheader("Cognitive Effects")
        st.write(f"- IQ increase: {effects['cognitive']['iq_increase']:+.1f} points")
        st.write(f"- Alzheimer's reduction: {effects['cognitive']['alzheimers_reduction']:.1f}%")
    
    # Kidney effects
    if effects.get('kidney'):
        st.subheader("Kidney Effects")
        st.write(f"- eGFR improvement: {effects['kidney']['egfr_improvement']:+.1f} mL/min/1.73m²")
        st.write(f"- CKD progression reduction: {effects['kidney']['ckd_progression_reduction']:.1f}%")
    
    # Longevity effects
    st.subheader("Longevity Effects")
    st.write(f"- Lifespan increase: {effects['longevity']['lifespan_increase']:.1f}%")
    st.write(f"- Healthspan improvement: {effects['longevity']['healthspan_improvement']:.1f}%")
    
    # Healthcare effects
    st.subheader("Healthcare Effects")
    st.write(f"- Hospital visit reduction: {effects['healthcare']['hospital_visit_reduction']:.1f}%")

if __name__ == "__main__":
    main() 