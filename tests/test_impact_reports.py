"""Tests for generating impact reports answering questions.md."""

import pytest
from typing import Dict, Any
import json
from pathlib import Path

from src.models.gene_therapy.follistatin.follistatin_model import FollistatinModel, FollistatinParameters
from src.models.gene_therapy.klotho.klotho_model import KlothoModel, KlothoParameters
from src.models.gene_therapy.lifespan.lifespan_model import LifespanModel, LifespanParameters
from src.models.clinical.study_design import StudyDesignAnalyzer, StudyParameters
from src.analysis.sensitivity.model_sensitivity import ModelSensitivityAnalyzer
from src.models.base_model import BaseParameters

from tests.config.test_parameters import (
    FOLLISTATIN_PARAMS,
    KLOTHO_PARAMS,
    LIFESPAN_PARAMS,
    STUDY_PARAMS
)

def format_currency(value: float) -> str:
    """Format currency values in billions."""
    if value >= 1e9:
        return f"${value/1e9:.1f}B"
    elif value >= 1e6:
        return f"${value/1e6:.1f}M"
    else:
        return f"${value:,.0f}"

def save_report(name: str, results: Dict[str, Any], sources: Dict[str, Any]) -> None:
    """Save results and sources as a markdown report."""
    report_dir = Path("docs/reports/generated")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f"{name}.md"
    with open(report_path, "w") as f:
        f.write(f"# {name.replace('_', ' ').title()} Impact Report\n\n")
        
        # Write executive summary
        f.write("## Executive Summary\n")
        for key, value in results.items():
            if isinstance(value, (int, float)) and key != "parameters":
                f.write(f"- {key.replace('_', ' ').title()}: {format_currency(value)}\n")
        f.write("\n")
        
        # Write parameters and sources
        f.write("## Parameters and Sources\n")
        for param, details in sources.items():
            f.write(f"### {param}\n")
            f.write(f"- Value: {details['value']}\n")
            f.write(f"- Source: [{details['source']}]({details['source']})\n")
            f.write(f"- Notes: {details['notes']}\n\n")

def test_follistatin_impact():
    """Test Follistatin therapy impact calculations."""
    # Create parameters
    base_params = BaseParameters()
    therapy_params = FollistatinParameters(**{k: v["value"] for k, v in FOLLISTATIN_PARAMS.items()})
    
    # Calculate impacts
    model = FollistatinModel(base_params, therapy_params)
    results = model.calculate_impacts()
    
    # Generate report
    save_report("follistatin_impact", results, FOLLISTATIN_PARAMS)
    
    # Verify key metrics
    assert results["obesity_cost_reduction"] > 0
    assert results["productivity_impact"] > 0
    assert results["medicare_savings"] > 0

def test_klotho_impact():
    """Test Klotho therapy impact calculations."""
    # Create parameters
    base_params = BaseParameters()
    therapy_params = KlothoParameters(**{k: v["value"] for k, v in KLOTHO_PARAMS.items()})
    
    # Calculate impacts
    model = KlothoModel(base_params, therapy_params)
    results = model.calculate_impacts()
    
    # Generate report
    save_report("klotho_impact", results, KLOTHO_PARAMS)
    
    # Verify key metrics
    assert results["cognitive_value"] > 0
    assert results["dementia_savings"] > 0
    assert results["kidney_savings"] > 0

def test_lifespan_impact():
    """Test lifespan extension impact calculations."""
    # Create parameters
    base_params = BaseParameters()
    therapy_params = LifespanParameters(**{k: v["value"] for k, v in LIFESPAN_PARAMS.items()})
    
    # Calculate impacts
    model = LifespanModel(base_params, therapy_params)
    results = model.calculate_impacts()
    
    # Generate report
    save_report("lifespan_impact", results, LIFESPAN_PARAMS)
    
    # Verify key metrics
    assert results["gdp_increase"] > 0
    assert results["medicare_savings"] > 0
    assert results["qaly_value"] > 0

def test_study_design():
    """Test clinical study design analysis."""
    # Create parameters
    study_params = StudyParameters(**{k: v["value"] for k, v in STUDY_PARAMS.items()})
    
    # Analyze study design
    analyzer = StudyDesignAnalyzer(study_params)
    results = analyzer.analyze_study_design()
    
    # Generate report
    save_report("study_design", results, STUDY_PARAMS)
    
    # Verify key components
    assert len(results["biomarker_correlations"]) > 0
    assert "age_stratification" in results
    assert "followup_duration" in results

def test_sensitivity_analysis():
    """Test model sensitivity analysis."""
    # Create analyzers
    sensitivity = ModelSensitivityAnalyzer()
    
    # Analyze each model
    models = {
        "follistatin": FollistatinModel(),
        "klotho": KlothoModel(),
        "lifespan": LifespanModel()
    }
    
    for name, model in models.items():
        results = sensitivity.analyze_model(model.calculate_impacts)
        save_report(f"{name}_sensitivity", results, {}) 