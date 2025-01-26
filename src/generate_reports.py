"""Script to generate all impact reports."""

import pytest
import sys
from pathlib import Path
from typing import List, Dict, Any
import json

def run_tests() -> None:
    """Run all tests to generate reports."""
    pytest.main(["tests/test_impact_reports.py", "-v"])

def generate_summary() -> None:
    """Generate a summary of all reports."""
    report_dir = Path("docs/reports/generated")
    summary_path = report_dir / "00_summary.md"
    
    # Collect all reports
    reports = list(report_dir.glob("*.md"))
    reports = [r for r in reports if not r.name.startswith("00_")]
    
    with open(summary_path, "w") as f:
        f.write("# Health Economic Impact Summary\n\n")
        
        # Answer each question from questions.md
        f.write("## Gene Therapy Impacts\n\n")
        
        # 1. Follistatin
        f.write("### 1. Follistatin Therapy (2 lb muscle gain, 2 lb fat reduction)\n")
        f.write("See [detailed report](follistatin_impact.md)\n")
        f.write("- Healthcare cost reduction from obesity impacts\n")
        f.write("- Workforce productivity improvements\n")
        f.write("- Medicare savings from reduced comorbidities\n\n")
        
        # 2. Lifespan Extension
        f.write("### 2. Lifespan Extension (2.5%)\n")
        f.write("See [detailed report](lifespan_impact.md)\n")
        f.write("- GDP increase from extended workforce participation\n")
        f.write("- Medicare savings from delayed age-related care\n")
        f.write("- Economic value of additional healthy years\n\n")
        
        # 3. Klotho
        f.write("### 3. Klotho Therapy\n")
        f.write("See [detailed report](klotho_impact.md)\n")
        f.write("- Cognitive function value (2-5 IQ points)\n")
        f.write("- Dementia care cost reduction (2-year delay)\n")
        f.write("- Medicare savings from delayed ESRD\n\n")
        
        # Study Design
        f.write("## Clinical Study Considerations\n")
        f.write("See [detailed report](study_design.md)\n")
        f.write("- Biomarker correlation analysis\n")
        f.write("- Age group stratification recommendations\n")
        f.write("- Follow-up duration requirements\n\n")
        
        # Sensitivity Analysis
        f.write("## Implementation Framework\n")
        f.write("See sensitivity analysis reports:\n")
        f.write("- [Follistatin Sensitivity](follistatin_sensitivity.md)\n")
        f.write("- [Klotho Sensitivity](klotho_sensitivity.md)\n")
        f.write("- [Lifespan Sensitivity](lifespan_sensitivity.md)\n\n")
        
        # Sources
        f.write("## Reference Documentation\n")
        refs_dir = Path("docs/references")
        for ref in refs_dir.glob("*.md"):
            f.write(f"- [{ref.stem}]({ref.relative_to(Path('docs'))})\n")

def main() -> None:
    """Generate all reports."""
    print("Generating impact reports...")
    
    # Create output directory
    report_dir = Path("docs/reports/generated")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Run tests to generate individual reports
    run_tests()
    
    # Generate summary report
    generate_summary()
    
    print("\nReport generation complete. See docs/reports/generated/ for results.")

if __name__ == "__main__":
    main() 