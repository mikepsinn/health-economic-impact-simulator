"""Test parameters with source documentation."""

from typing import Dict, Any

FOLLISTATIN_PARAMS = {
    "muscle_gain_lbs": {
        "value": 2.0,
        "source": "docs/references/muscle-fat.md",
        "notes": "Demonstrated muscle mass gain in clinical trials"
    },
    "fat_reduction_lbs": {
        "value": 2.0,
        "source": "docs/references/2-lb-fat-reduction.md",
        "notes": "Average fat mass reduction across population"
    },
    "obesity_cost_per_lb": {
        "value": 150.0,
        "source": "docs/references/economic-modeling.md",
        "notes": "Annual healthcare cost attributed to each pound of excess fat"
    },
    "productivity_per_muscle_lb": {
        "value": 0.001,
        "source": "docs/references/economic-modeling.md",
        "notes": "Productivity increase per pound of muscle mass"
    }
}

KLOTHO_PARAMS = {
    "iq_increase": {
        "value": 3.5,
        "source": "docs/references/klotho-neuroinflammation.md",
        "notes": "Average cognitive function improvement (2-5 point range)"
    },
    "alzheimers_delay_years": {
        "value": 2.0,
        "source": "docs/references/klotho.md",
        "notes": "Delay in Alzheimer's progression"
    },
    "kidney_delay_years": {
        "value": 2.0,
        "source": "docs/references/klotho-savings.md",
        "notes": "Delay in kidney disease progression"
    },
    "alzheimers_annual_cost": {
        "value": 355e9,
        "source": "docs/references/klotho-50-50-savings.md",
        "notes": "Total US annual Alzheimer's cost"
    }
}

LIFESPAN_PARAMS = {
    "lifespan_increase_pct": {
        "value": 2.5,
        "source": "docs/references/economic-modeling.md",
        "notes": "Percentage increase in lifespan"
    },
    "workforce_participation_rate": {
        "value": 0.63,
        "source": "docs/references/economic-modeling.md",
        "notes": "US workforce participation rate"
    },
    "qaly_value": {
        "value": 100000,
        "source": "docs/references/economic-modeling.md",
        "notes": "Value of one quality-adjusted life year"
    }
}

STUDY_PARAMS = {
    "biomarkers": {
        "value": ["eGFR", "cystatin_C", "muscle_mass", "body_fat"],
        "source": "docs/references/klotho.md",
        "notes": "Key biomarkers for tracking outcomes"
    },
    "min_followup_years": {
        "value": 2.0,
        "source": "docs/references/economic-modeling.md",
        "notes": "Minimum years needed for economic impact assessment"
    }
} 