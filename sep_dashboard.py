import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("ICU AI Risk Dashboard")
st.markdown("Simulated monitoring of critical ICU conditions with vitals and trend charts.")

# Simulate time-series vitals
def simulate_trends():
    time = np.arange(0, 10)
    trend = np.cumsum(np.random.normal(0, 1, 10))
    return time, trend

# Simulate current vital signs
def generate_vitals(condition):
    vitals = {
        "HR": random.randint(60, 140),
        "BP_sys": random.randint(85, 120),
        "BP_dia": random.randint(55, 85),
        "Temp": round(random.uniform(36.0, 40.0), 1),
        "SpO2": random.randint(88, 100),
        "RR": random.randint(12, 28),
        "Lactate": round(random.uniform(0.5, 4.5), 2)
    }
    return vitals

# Determine alert level
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
    else:
        return random.choice(["Low", "Moderate", "High"])

# Plot trend
def plot_trend(title, trend_data):
    fig, ax = plt.subplots(figsize=(2.5, 1.5))
    time, values = trend_data
    ax.plot(time, values, color="blue", linewidth=2)
    ax.set_title(title, fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    st.pyplot(fig)

# ICU conditions
icu_conditions = [
    "Sepsis", "ARDS", "Cardiac Arrest", "Kidney Injury", "Liver Failure",
    "Pulmonary Embolism", "Stroke", "Hypoglycemia", "Hyperkalemia",
    "Hemorrhage", "Pneumonia", "Shock"
]

cols = st.columns(3)

for i, condition in enumerate(icu_conditions):
    vitals = generate_vitals(condition)
    alert = determine_alert(vitals, condition)
    color = {"Low": "green", "Moderate": "orange", "High": "red"}[alert]

    with cols[i % 3]:
        st.markdown(f"### {condition}")
        st.markdown(f"**Alert:** <span style='color:{color}'>{alert}</span>", unsafe_allow_html=True)
        st.write(f"- HR: {vitals['HR']} bpm")
        st.write(f"- BP: {vitals['BP_sys']}/{vitals['BP_dia']}")
        st.write(f"- Temp: {vitals['Temp']} °C")
        st.write(f"- SpO2: {vitals['SpO2']}%")
        st.write(f"- RR: {vitals['RR']} bpm")
        st.write(f"- Lactate: {vitals['Lactate']} mmol/L")

        st.markdown("**Vital Trends:**")
        plot_trend("Heart Rate", simulate_trends())
        plot_trend("SpO2", simulate_trends())

st.markdown("---")
st.caption("Vitals are randomly generated for prototyping. This dashboard simulates ICU monitoring with basic trend tracking.")
