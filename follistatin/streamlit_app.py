import streamlit as st
import numpy as np
from follistatin_model import (
    cumulative_savings_from_body_comp_change,
    added_gdp_from_increased_lifespan,
    medicare_savings
)

st.set_page_config(page_title="Follistatin Gene Therapy Impact Model", layout="wide")

st.title("Follistatin Gene Therapy Impact Model")
st.markdown("Adjust the parameters below to see the economic impact of follistatin gene therapy.")

# Create columns for input parameters
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Population Parameters")
    us_population = st.number_input(
        "US Population",
        value=332_000_000,
        step=1_000_000,
        format="%d"
    )
    medicare_beneficiaries = st.number_input(
        "Medicare Beneficiaries",
        value=64_000_000,
        step=1_000_000,
        format="%d"
    )

with col2:
    st.subheader("Body Composition")
    muscle_gain = st.number_input("Average Muscle Gain (lbs)", value=2.0, step=0.1)
    fat_loss = st.number_input("Average Fat Loss (lbs)", value=2.0, step=0.1)
    savings_per_lb = st.number_input("Healthcare Savings per lb ($)", value=10.0, step=0.5)

with col3:
    st.subheader("Lifespan & Productivity")
    baseline_lifespan = st.number_input("Baseline Lifespan (years)", value=77.0, step=0.1)
    lifespan_increase_percent = st.number_input("Lifespan Increase (%)", value=2.5, step=0.1)
    workforce_fraction = st.number_input("Workforce Fraction", value=0.5, step=0.05)
    annual_productivity = st.number_input(
        "Annual Productivity per Worker ($)",
        value=70000.0,
        step=1000.0,
        format="%f"
    )

# Medicare parameters
st.subheader("Medicare Parameters")
col4, col5 = st.columns(2)

with col4:
    annual_medicare_cost_per_person = st.number_input(
        "Annual Medicare Cost per Person ($)",
        value=14000.0,
        step=100.0
    )

with col5:
    medicare_cost_reduction_percent = st.number_input(
        "Medicare Cost Reduction (%)",
        value=5.0,
        step=0.1
    ) / 100.0

# Calculate results
additional_years = baseline_lifespan * (lifespan_increase_percent / 100.0)

total_savings_body_comp = cumulative_savings_from_body_comp_change(
    us_population, muscle_gain, fat_loss, savings_per_lb
)

total_added_gdp = added_gdp_from_increased_lifespan(
    us_population, additional_years, workforce_fraction, annual_productivity
)

annual_medicare_savings = medicare_savings(
    medicare_beneficiaries,
    annual_medicare_cost_per_person,
    medicare_cost_reduction_percent
)

# Display results
st.header("Results")
st.markdown("---")

col6, col7, col8 = st.columns(3)

with col6:
    st.metric(
        "Annual Healthcare Savings",
        f"${total_savings_body_comp/1e9:.2f}B",
        "From Body Composition Changes"
    )

with col7:
    st.metric(
        "Added GDP (Cumulative)",
        f"${total_added_gdp/1e12:.2f}T",
        f"From {lifespan_increase_percent}% Lifespan Increase"
    )

with col8:
    st.metric(
        "Annual Medicare Savings",
        f"${annual_medicare_savings/1e9:.2f}B",
        "From Healthier Population"
    )

# Add explanatory notes
st.markdown("---")
st.markdown("""
### Notes
- All calculations are simplified estimates and should be used for exploratory purposes only
- GDP impact is cumulative over the additional lifespan years
- Healthcare savings are calculated on an annual basis
- Medicare savings assume uniform cost reduction across the beneficiary population
""") 