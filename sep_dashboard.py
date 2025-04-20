import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="Smart ICU Dashboard", page_icon="🧠")

st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0f4c81;
        }
        .alert-low { color: green; }
        .alert-moderate { color: orange; }
        .alert-high { color: red; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>AI-Powered ICU Risk Dashboard</div>", unsafe_allow_html=True)
st.caption("Monitoring common ICU risks with vital sign trends and intelligent alerts.")

# Simulate trend data
def simulate_trend(base, variation=5):
    trend = base + np.cumsum(np.random.normal(0, variation, 10))
    return np.round(trend, 1)

# Simulate patient vitals
def generate_vitals():
    return {
        "HR": random.randint(60, 140),
        "BP_sys": random.randint(85, 120),
        "BP_dia": random.randint(55, 85),
        "Temp": round(random.uniform(36.0, 40.0), 1),
        "SpO2": random.randint(88, 100),
        "RR": random.randint(12, 28),
        "Lactate": round(random.uniform(0.5, 4.5), 2)
    }

# Determine risk level
def assess_risk(condition, vitals):
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
    return random.choice(["Low", "Moderate", "High"])

# Display trend chart
def show_trend_chart(title, values):
    fig, ax = plt.subplots(figsize=(2.5, 1.5))
    ax.plot(values, color="#0f4c81", linewidth=2)
    ax.set_title(title, fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    st.pyplot(fig)

# Conditions to monitor
icu_conditions = [
    "Sepsis", "ARDS", "Cardiac Arrest", "Kidney Injury", "Liver Failure",
    "Pulmonary Embolism", "Stroke", "Hypoglycemia", "Hyperkalemia",
    "Hemorrhage", "Pneumonia", "Shock"
]

cols = st.columns(3)

for i, condition in enumerate(icu_conditions):
    vitals = generate_vitals()
    risk = assess_risk(condition, vitals)
    color_class = f"alert-{risk.lower()}"

    with cols[i % 3]:
        st.markdown(f"<h4>{condition}</h4>", unsafe_allow_html=True)
        st.markdown(f"<b>Risk Level:</b> <span class='{color_class}'>{risk}</span>", unsafe_allow_html=True)
        st.markdown("<b>Current Vitals:</b>", unsafe_allow_html=True)
        st.write(f"HR: {vitals['HR']} bpm")
        st.write(f"BP: {vitals['BP_sys']}/{vitals['BP_dia']}")
        st.write(f"Temp: {vitals['Temp']} °C")
        st.write(f"SpO2: {vitals['SpO2']}%")
        st.write(f"RR: {vitals['RR']} bpm")
        st.write(f"Lactate: {vitals['Lactate']} mmol/L")

        st.markdown("**Vital Trends:**")
        show_trend_chart("Heart Rate", simulate_trend(vitals['HR']))
        show_trend_chart("SpO2", simulate_trend(vitals['SpO2'], variation=1))

st.markdown("""
---
<i>Note: This is a simulated dashboard for proof-of-concept purposes. All data is randomized.</i>
""", unsafe_allow_html=True)


