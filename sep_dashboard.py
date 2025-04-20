import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(layout="wide")

st.title("ICU AI Risk Dashboard")
st.markdown("A simulated dashboard for monitoring multiple critical conditions in the ICU, including vital trends.")

# Function to simulate vitals
def generate_vitals(condition):
    # Simulate realistic ICU vitals
    vitals = {
        "HR": random.randint(60, 140),
        "BP": f"{random.randint(85, 120)}/{random.randint(55, 85)}",
        "Temp": round(random.uniform(36.0, 40.0), 1),
        "SpO2": random.randint(88, 100),
        "RR": random.randint(12, 28),
        "Lactate": round(random.uniform(0.5, 4.5), 2)
    }
    return vitals

# Function to determine alert level based on example rules
def determine_alert(vitals, condition):
    if condition == "Sepsis":
        if vitals["Temp"] > 38.3 and vitals["HR"] > 100 and vitals["Lactate"] > 2.0:
            return "High"
        elif vitals["Temp"] > 37.5:
            return "Moderate"
        else:
            return "Low"
    elif condition == "ARDS":
        if vitals["SpO2"] < 92 and vitals["RR"] > 22:
            return "High"
        elif vitals["SpO2"] < 94:
            return "Moderate"
        else:
            return "Low"
    elif condition == "Cardiac Arrest":
        if vitals["HR"] < 40 or vitals["SpO2"] < 90:
            return "High"
        else:
            return "Low"
    # Add more logic per condition
    else:
        return random.choice(["Low", "Moderate", "High"])

# 12 common ICU conditions
icu_conditions = [
    "Sepsis", "ARDS", "Cardiac Arrest", "Kidney Injury", "Liver Failure",
    "Pulmonary Embolism", "Stroke", "Hypoglycemia", "Hyperkalemia",
    "Hemorrhage", "Pneumonia", "Shock"
]

# Layout: 3 boxes per row
cols = st.columns(3)

for i, condition in enumerate(icu_conditions):
    vitals = generate_vitals(condition)
    alert = determine_alert(vitals, condition)
    status_color = {"Low": "green", "Moderate": "orange", "High": "red"}[alert]

    with cols[i % 3]:
        st.markdown(f"### {condition}")
        st.markdown(f"**Alert Level:** <span style='color:{status_color}; font-weight:bold'>{alert}</span>", unsafe_allow_html=True)
        st.markdown("**Vitals Monitored:**")
        st.write(f"- HR: {vitals['HR']} bpm")
        st.write(f"- BP: {vitals['BP']}")
        st.write(f"- Temp: {vitals['Temp']} °C")
        st.write(f"- SpO2: {vitals['SpO2']}%")
        st.write(f"- RR: {vitals['RR']} bpm")
        st.write(f"- Lactate: {vitals['Lactate']} mmol/L")

st.markdown("---")
st.caption("Note: This is a prototype simulation. Data is randomly generated to reflect condition-specific patterns.")

