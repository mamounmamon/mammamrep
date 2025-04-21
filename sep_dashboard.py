import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import time
import datetime

st.set_page_config(layout="wide", page_title="Advanced ICU Sepsis & Condition Dashboard")

# Constants
REFRESH_INTERVAL = 1
MAX_HISTORY = 300

# Auto-refresh placeholder
st_autorefresh = st.empty()

# Initialize state with all metrics
METRICS = [
    "HR", "Temp", "RR", "SpO2", "Lactate", "BP_sys",
    "WBC", "Platelets", "Creatinine", "Bilirubin", "MAP", "GCS",
    "Glucose", "Urine_Output", "INR", "FiO2", "pH", "PaCO2"
]

if "trend_data" not in st.session_state:
    st.session_state.trend_data = {metric: [] for metric in ["timestamps"] + METRICS + ["Sepsis_Risk", "ARDS_Risk"]}

# Simulate vitals

def simulate_vitals():
    return {
        "HR": random.randint(60, 140),
        "Temp": round(random.uniform(36.0, 40.0), 1),
        "RR": random.randint(10, 30),
        "SpO2": random.randint(85, 100),
        "Lactate": round(random.uniform(0.5, 4.5), 2),
        "BP_sys": random.randint(90, 140),
        "WBC": round(random.uniform(4.0, 15.0), 1),
        "Platelets": random.randint(100, 400),
        "Creatinine": round(random.uniform(0.5, 2.5), 2),
        "Bilirubin": round(random.uniform(0.2, 3.0), 2),
        "MAP": round(random.uniform(60, 100), 1),
        "GCS": random.randint(3, 15),
        "Glucose": round(random.uniform(3.0, 15.0), 1),
        "Urine_Output": round(random.uniform(0.2, 2.5), 2),
        "INR": round(random.uniform(0.9, 3.5), 2),
        "FiO2": round(random.uniform(21, 100), 1),
        "pH": round(random.uniform(7.2, 7.55), 2),
        "PaCO2": round(random.uniform(25, 55), 1)
    }

# Update vitals

def update_data():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    vitals = simulate_vitals()

    st.session_state.trend_data["timestamps"].append(now)

    for k, v in vitals.items():
      #  st.session_state.trend_data[k].append(v)

    # Risk calculations
    sepsis_score = 0
    ards_score = 0

    # Sepsis criteria
    if vitals["HR"] > 120 or vitals["HR"] < 60: sepsis_score += 1
    if vitals["Temp"] > 39 or vitals["Temp"] < 36: sepsis_score += 1
    if vitals["RR"] > 25 or vitals["RR"] < 12: sepsis_score += 1
    if vitals["SpO2"] < 90: sepsis_score += 1
    if vitals["Lactate"] > 2.5: sepsis_score += 1
    if vitals["BP_sys"] < 100: sepsis_score += 1
    if vitals["WBC"] < 4 or vitals["WBC"] > 12: sepsis_score += 1
    if vitals["Creatinine"] > 1.5: sepsis_score += 1
    if vitals["Bilirubin"] > 2.0: sepsis_score += 1
    if vitals["Platelets"] < 150: sepsis_score += 1
    if vitals["MAP"] < 65: sepsis_score += 1
    if vitals["GCS"] < 13: sepsis_score += 1

    # ARDS criteria (simplified)
    if vitals["FiO2"] > 50: ards_score += 1
    if vitals["pH"] < 7.3: ards_score += 1
    if vitals["PaCO2"] > 50: ards_score += 1
    if vitals["SpO2"] < 90: ards_score += 1

    st.session_state.trend_data["Sepsis_Risk"].append(int((sepsis_score / 12) * 100))
    st.session_state.trend_data["ARDS_Risk"].append(int((ards_score / 4) * 100))

    # Truncate history
    for key in st.session_state.trend_data:
        if len(st.session_state.trend_data[key]) > MAX_HISTORY:
            st.session_state.trend_data[key] = st.session_state.trend_data[key][-MAX_HISTORY:]

# update_data()

# Layout
st.title("🧠 ICU Condition Intelligence Dashboard")

# Alerts
risk_col1, risk_col2 = st.columns(2)
sepsis = st.session_state.trend_data["Sepsis_Risk"][-1]
ards = st.session_state.trend_data["ARDS_Risk"][-1]

if sepsis >= 80:
    risk_col1.error("🚨 Sepsis Risk ≥ 80%! Action Required", icon="⚠️")
if ards >= 75:
    risk_col2.warning("⚠️ ARDS Risk High! Monitor Closely", icon="❗")

# Key metrics
metrics_grid = st.columns(4)
data = st.session_state.trend_data
latest_values = {k: v[-1] for k, v in data.items() if k != "timestamps"}

for i, (k, v) in enumerate(latest_values.items()):
    label = k.replace("_", " ")
    metrics_grid[i % 4].metric(label, str(v))

# Trend plots
with st.expander("📈 Trend Analysis Charts", expanded=True):
    fig, axs = plt.subplots(4, 2, figsize=(15, 10))
    axes = axs.flatten()
    for i, k in enumerate(METRICS[:8]):
        axes[i].plot(data["timestamps"], data[k], label=k)
        axes[i].set_title(k)
        axes[i].tick_params(axis='x', rotation=45, labelsize=7)
        axes[i].grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig)

    fig2, axs2 = plt.subplots(2, 1, figsize=(15, 5))
    axs2[0].plot(data["timestamps"], data["Sepsis_Risk"], color="darkred", linewidth=2, label="Sepsis Risk")
    axs2[1].plot(data["timestamps"], data["ARDS_Risk"], color="darkblue", linewidth=2, label="ARDS Risk")
    for ax in axs2:
        ax.set_ylim([0, 100])
        ax.grid(True, linestyle=":", alpha=0.5)
        ax.tick_params(axis='x', rotation=45, labelsize=7)
    axs2[0].set_title("Sepsis Risk Trend")
    axs2[1].set_title("ARDS Risk Trend")
    plt.tight_layout()
    st.pyplot(fig2)

# Data Export
with st.expander("⬇️ Export Data"):
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download ICU Data as CSV",
        data=csv,
        file_name="icu_data.csv",
        mime="text/csv"
    )

# Refresh page
time.sleep(REFRESH_INTERVAL)
st.rerun()
