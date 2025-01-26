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

def extract_param_values(params: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Extract just the values from parameter dictionaries."""
    return {k: v["value"] for k, v in params.items()}

def test_follistatin_impact():
    """Test follistatin impact calculations for 2lb muscle gain and 2lb fat reduction."""
    base_params = BaseParameters()
    therapy_params = FollistatinParameters(**extract_param_values(FOLLISTATIN_PARAMS))
    model = FollistatinModel(base_params=base_params, therapy_params=therapy_params)
    impacts = model.calculate_impacts()
    
    save_report("follistatin_impact", impacts, FOLLISTATIN_PARAMS)
    
    assert isinstance(impacts, dict)
    assert "healthcare_savings" in impacts
    assert "productivity_value" in impacts
    assert "medicare_savings" in impacts
    assert impacts["healthcare_savings"] > 0
    assert impacts["productivity_value"] > 0
    assert impacts["medicare_savings"] > 0

def test_klotho_impact():
    """Test klotho impact calculations for cognitive, dementia and kidney impacts."""
    base_params = BaseParameters()
    therapy_params = KlothoParameters(**extract_param_values(KLOTHO_PARAMS))
    model = KlothoModel(base_params=base_params, therapy_params=therapy_params)
    impacts = model.calculate_impacts()
    
    save_report("klotho_impact", impacts, KLOTHO_PARAMS)
    
    assert isinstance(impacts, dict)
    assert "cognitive_value" in impacts
    assert "dementia_savings" in impacts
    assert "kidney_savings" in impacts
    assert impacts["cognitive_value"] > 0
    assert impacts["dementia_savings"] > 0
    assert impacts["kidney_savings"] > 0

def test_lifespan_impact():
    """Test lifespan extension impact calculations for 2.5% increase."""
    base_params = BaseParameters()
    therapy_params = LifespanParameters(**extract_param_values(LIFESPAN_PARAMS))
    model = LifespanModel(base_params=base_params, therapy_params=therapy_params)
    impacts = model.calculate_impacts()
    
    save_report("lifespan_impact", impacts, LIFESPAN_PARAMS)
    
    assert isinstance(impacts, dict)
    assert "gdp_increase" in impacts
    assert "medicare_savings" in impacts
    assert "qaly_value" in impacts
    assert impacts["gdp_increase"] > 0
    assert impacts["medicare_savings"] > 0
    assert impacts["qaly_value"] > 0

def test_study_design():
    """Test study design analysis for clinical implementation."""
    params = StudyParameters(**extract_param_values(STUDY_PARAMS))
    analyzer = StudyDesignAnalyzer(params)
    design = analyzer.analyze_study_design()  # Fixed method name
    
    save_report("study_design", design, STUDY_PARAMS)
    
    assert isinstance(design, dict)
    assert "biomarker_correlations" in design
    assert "age_stratification" in design
    assert "followup_duration" in design
    assert len(design["biomarker_correlations"]) > 0
    assert "recommended_groups" in design["age_stratification"]
    assert design["followup_duration"]["minimum_years"] > 0

def test_sensitivity_analysis():
    """Test sensitivity analysis for all models."""
    sensitivity = ModelSensitivityAnalyzer()
    base_params = BaseParameters()
    
    models = {
        "follistatin": FollistatinModel(
            base_params=base_params,
            therapy_params=FollistatinParameters(**extract_param_values(FOLLISTATIN_PARAMS))
        ),
        "klotho": KlothoModel(
            base_params=base_params,
            therapy_params=KlothoParameters(**extract_param_values(KLOTHO_PARAMS))
        ),
        "lifespan": LifespanModel(
            base_params=base_params,
            therapy_params=LifespanParameters(**extract_param_values(LIFESPAN_PARAMS))
        )
    }
    
    for name, model in models.items():
        results = sensitivity.analyze_model(model.calculate_impacts)
        
        sources = {
            "parameters": {
                "value": list(model.therapy_params.dict().keys()),
                "source": f"docs/references/{name}.md",
                "notes": "Key model parameters analyzed for sensitivity"
            }
        }
        
        save_report(f"{name}_sensitivity", results, sources)
        
        assert isinstance(results, dict)
        assert "sensitivity_scores" in results
        assert "parameter_impacts" in results
        assert len(results["sensitivity_scores"]) > 0
        assert len(results["parameter_impacts"]) > 0 