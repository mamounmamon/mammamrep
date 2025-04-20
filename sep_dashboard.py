import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# Streamlit config
st.set_page_config(layout="wide", page_title="ICU AI Dashboard")

# Style
st.markdown("""
    <style>
    .big-title { font-size: 36px; font-weight: 700; margin-bottom: 0; }
    .metric-label { font-weight: bold; margin-top: 8px; }
    .card { border-radius: 16px; padding: 1rem; box-shadow: 0 2px 6px rgba(0,0,0,0.08); background-color: #fff; margin-bottom: 1rem; }
    .alert-low { color: green; }
    .alert-moderate { color: orange; }
    .alert-high { color: red; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="big-title">🧠 ICU AI Risk Dashboard</p>', unsafe_allow_html=True)
st.caption("Live-like vitals and trend monitoring for 12 critical ICU conditions")

# ICU Conditions
icu_conditions = [
    "Sepsis", "ARDS", "Cardiac Arrest", "Kidney Injury", "Liver Failure",
    "Pulmonary Embolism", "Stroke", "Hypoglycemia", "Hyperkalemia",
    "Hemorrhage", "Pneumonia", "Shock"
]

# Simulated vitals
def simulate_vitals():
    return {
        "HR": random.randint(60, 140),
        "BP": f"{random.randint(90, 120)}/{random.randint(60, 85)}",
        "Temp": round(random.uniform(36.0, 40.0), 1),
        "SpO2": random.randint(88, 100),
        "RR": random.randint(10, 28),
        "Lactate": round(random.uniform(0.5, 4.5), 2)
    }

# Alert logic
def alert_level(vitals):
    if vitals["Temp"] > 38.5 and vitals["HR"] > 110 and vitals["Lactate"] > 2.5:
        return "🔴 High", "alert-high"
    elif vitals["Temp"] > 37.8 or vitals["SpO2"] < 94:
        return "🟠 Moderate", "alert-moderate"
    else:
        return "🟢 Low", "alert-low"

# Trend chart
def plot_trend():
    fig, ax = plt.subplots(figsize=(2.5, 0.7))
    y = np.cumsum(np.random.normal(0, 1, 12)) + 100
    ax.plot(y, color='deepskyblue', linewidth=2)
    ax.axis('off')
    st.pyplot(fig, use_container_width=True)

# Display dashboard
cols = st.columns(3)

for idx, condition in enumerate(icu_conditions):
    vitals = simulate_vitals()
    alert, alert_class = alert_level(vitals)

    with cols[idx % 3]:
        with st.container():
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"#### {condition} <span class='{alert_class}'>{alert}</span>", unsafe_allow_html=True)

            st.markdown("<div class='metric-label'>Vitals:</div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            col1.metric("HR", f"{vitals['HR']} bpm")
            col2.metric("BP", vitals["BP"])
            col3.metric("Temp", f"{vitals['Temp']} °C")
            col1.metric("SpO₂", f"{vitals['SpO2']}%")
            col2.metric("RR", f"{vitals['RR']}")
            col3.metric("Lactate", f"{vitals['Lactate']} mmol/L")

            st.markdown("Trend: Heart Rate (simulated)")
            plot_trend()

            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Refresh the page (F5 or rerun) to simulate new vitals.")
