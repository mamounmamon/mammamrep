import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time

st.set_page_config(layout="wide", page_title="ICU Live Dashboard")

# Inject CSS styles
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 14px !important;
    }
    .big-title {
        font-size: 28px !important;
        font-weight: 600;
    }
    .card {
        border-radius: 16px;
        padding: 1rem;
        background-color: #f9f9f9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .alert-low { color: green; }
    .alert-moderate { color: orange; }
    .alert-high { color: red; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="big-title">🧠 ICU AI Live Dashboard</div>', unsafe_allow_html=True)
st.caption("12 ICU conditions · Live vitals · Trends for all vital signs · Refreshes every 5 seconds")

# Auto-refresh every 5 seconds
countdown = 5
if "last_refresh" not in st.session_state:
    st.session_state["last_refresh"] = time.time()

elapsed = time.time() - st.session_state["last_refresh"]
if elapsed > countdown:
    st.session_state["last_refresh"] = time.time()
    st.experimental_rerun()

# ICU conditions
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

# Alert level
def alert_level(vitals):
    if vitals["Temp"] > 38.5 and vitals["HR"] > 110 and vitals["Lactate"] > 2.5:
        return "🔴 High", "alert-high"
    elif vitals["Temp"] > 37.8 or vitals["SpO2"] < 94:
        return "🟠 Moderate", "alert-moderate"
    else:
        return "🟢 Low", "alert-low"

# Vital trend plot
def plot_vital_trends(vitals):
    fig, axs = plt.subplots(1, 5, figsize=(12, 1.5))
    vitals_trend = {
        "HR": np.cumsum(np.random.normal(0, 0.5, 15)) + vitals["HR"],
        "Temp": np.cumsum(np.random.normal(0, 0.05, 15)) + vitals["Temp"],
        "RR": np.cumsum(np.random.normal(0, 0.2, 15)) + vitals["RR"],
        "SpO2": np.cumsum(np.random.normal(0, 0.3, 15)) + vitals["SpO2"],
        "Lactate": np.cumsum(np.random.normal(0, 0.05, 15)) + vitals["Lactate"]
    }

    for ax, (label, trend) in zip(axs, vitals_trend.items()):
        ax.plot(trend, linewidth=2)
        ax.set_title(label, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        ax.set_facecolor("#f0f0f0")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

# Layout
cols = st.columns(3)

for idx, condition in enumerate(icu_conditions):
    vitals = simulate_vitals()
    alert, alert_class = alert_level(vitals)

    with cols[idx % 3]:
        with st.container():
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"**{condition}** <span class='{alert_class}'>{alert}</span>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("HR", f"{vitals['HR']} bpm")
            col2.metric("BP", vitals["BP"])
            col3.metric("Temp", f"{vitals['Temp']} °C")
            col1.metric("SpO₂", f"{vitals['SpO2']}%")
            col2.metric("RR", f"{vitals['RR']}")
            col3.metric("Lactate", f"{vitals['Lactate']} mmol/L")

            plot_vital_trends(vitals)
            st.markdown("</div>", unsafe_allow_html=True)

st.caption("Vitals auto-refresh every 5 seconds · Simulated for prototype.")
