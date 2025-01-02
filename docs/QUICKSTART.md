# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- PowerShell (Windows) or Terminal (Mac/Linux)
- Git (for cloning the repository)

## Setup

1. **Clone the repository**
   ```powershell
   git clone https://github.com/mikepsinn/health-economic-impact-simulator
   cd health-economic-impact-simulator
   ```

2. **Create and activate virtual environment**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```powershell
   # Using python -m pip ensures we're using the correct pip installation
   python -m pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Streamlit app**
   ```powershell
   # Using python -m streamlit ensures we're using the correct Python environment
   python -m streamlit run app.py
   ```
   The app will open in your default web browser at http://localhost:8501

   If the app doesn't open automatically, manually visit http://localhost:8501 in your browser.

2. **Using the Interface**
   - Select an intervention from the sidebar dropdown
   - Choose a population segment
   - Adjust parameters using the sliders
   - View real-time updates to calculations and visualizations

## Key Features

- **Impact Analysis**: View Medicare savings, GDP impact, and QALY improvements
- **Interactive Charts**: Explore data through various visualizations
- **Sensitivity Analysis**: Test different scenarios and assumptions
- **Mobile-Friendly**: Optimized for both desktop and mobile viewing

## Parameter Adjustments

The app allows you to modify:
- Effect parameters (muscle mass, fat mass, IQ, etc.)
- Impact modifiers (cost savings, GDP effects)
- Sensitivity analysis settings
- Time horizon for projections

## Troubleshooting

1. **App won't start**
   - Ensure Python and all dependencies are installed
   - Check if port 8501 is available
   - Verify virtual environment is activated

2. **Visualizations not loading**
   - Clear browser cache
   - Refresh the page
   - Check console for any JavaScript errors

3. **Calculation errors**
   - Verify parameter inputs are within valid ranges
   - Check for any missing required fields
   - Ensure population segment is selected

## Getting Help

- Check the full documentation in `/docs`
- Review error messages in the terminal
- Consult the workflow diagram in `workflow.md`

## Next Steps

After getting familiar with the basic functionality:
1. Explore sensitivity analysis features
2. Review methodology documentation
3. Experiment with different population segments
4. Try various intervention scenarios 