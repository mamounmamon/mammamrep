import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import datetime

st.set_page_config(layout="wide", page_title="Live Sepsis Dashboard")

# Auto-refresh every 1 second
st_autorefresh = st.empty()
REFRESH_INTERVAL = 1

# Initialize session state
expected_keys = [
    "timestamps", "HR", "Temp", "RR", "SpO2", "Lactate", "BP_sys",
    "WBC", "Platelets", "Creatinine", "Bilirubin", "MAP", "GCS", "Risk"
]

if "trend_data" not in st.session_state:
    st.session_state.trend_data = {}

for key in expected_keys:
    if key not in st.session_state.trend_data:
        st.session_state.trend_data[key] = []

# Simulate new vitals
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
        "GCS": random.randint(3, 15)
    }

# Update data
def update_data():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    vitals = simulate_vitals()

    # Ensure timestamps are updated first
    st.session_state.trend_data["timestamps"].append(now)

    # Store vitals
    for k, v in vitals.items():
        st.session_state.trend_data[k].append(v)

    # Risk calculation
    risk_score = 0
    risk_score += 1 if vitals["HR"] > 120 or vitals["HR"] < 60 else 0
    risk_score += 1 if vitals["Temp"] > 39 or vitals["Temp"] < 36 else 0
    risk_score += 1 if vitals["RR"] > 25 or vitals["RR"] < 12 else 0
    risk_score += 1 if vitals["SpO2"] < 90 else 0
    risk_score += 1 if vitals["Lactate"] > 2.5 else 0
    risk_score += 1 if vitals["BP_sys"] < 100 else 0
    risk_score += 1 if vitals["WBC"] < 4 or vitals["WBC"] > 12 else 0
    risk_score += 1 if vitals["Creatinine"] > 1.5 else 0
    risk_score += 1 if vitals["Bilirubin"] > 2.0 else 0
    risk_score += 1 if vitals["Platelets"] < 150 else 0
    risk_score += 1 if vitals["MAP"] < 65 else 0
    risk_score += 1 if vitals["GCS"] < 13 else 0

    risk_percent = int((risk_score / 12) * 100)
    st.session_state.trend_data["Risk"].append(risk_percent)

    # Trim all lists to the same length (max 300)
    max_len = 300
    for key in expected_keys:
        if len(st.session_state.trend_data[key]) > max_len:
            st.session_state.trend_data[key] = st.session_state.trend_data[key][-max_len:]

update_data()

# Display risk alert
current_risk = st.session_state.trend_data["Risk"][-1]
if current_risk >= 80:
    st.error("🚨 High Risk Alert: Risk exceeds 80%! Immediate attention required!", icon="⚠️")

# Display dashboard
st.title("🦠 Live Sepsis Monitoring Dashboard")

risk_color = "green" if current_risk < 30 else "orange" if current_risk < 70 else "red"
st.markdown(f"### 🔥 Risk Level: <span style='color:{risk_color}; font-size: 24px;'>{current_risk}%</span>", unsafe_allow_html=True)

# Vital metrics
cols = st.columns(4)
data = st.session_state.trend_data

metrics = [
    ("Heart Rate (HR)", f"{data['HR'][-1]} bpm"),
    ("Temperature (°C)", f"{data['Temp'][-1]}"),
    ("Respiratory Rate (RR)", f"{data['RR'][-1]}"),
    ("Oxygen Saturation (SpO₂)", f"{data['SpO2'][-1]} %"),
    ("Lactate (mmol/L)", f"{data['Lactate'][-1]}"),
    ("Systolic BP", f"{data['BP_sys'][-1]} mmHg"),
    ("WBC (x10⁹/L)", f"{data['WBC'][-1]}"),
    ("Platelets (x10⁹/L)", f"{data['Platelets'][-1]}"),
    ("Creatinine (mg/dL)", f"{data['Creatinine'][-1]}"),
    ("Bilirubin (mg/dL)", f"{data['Bilirubin'][-1]}"),
    ("MAP (mmHg)", f"{data['MAP'][-1]}"),
    ("GCS", f"{data['GCS'][-1]}")
]

for i, (label, value) in enumerate(metrics):
    cols[i % 4].metric(label, value)

# Combined vitals trend chart
fig, ax = plt.subplots(figsize=(12, 5))
colors = {
    "HR": "red", "Temp": "orange", "RR": "green",
    "SpO2": "blue", "Lactate": "purple", "BP_sys": "gray",
    "WBC": "brown", "Platelets": "olive", "Creatinine": "cyan",
    "Bilirubin": "magenta", "MAP": "teal", "GCS": "black"
}

for key in expected_keys[1:-1]:  # Skip timestamps and Risk
    ax.plot(data["timestamps"], data[key], label=key, color=colors.get(key, "black"), linewidth=1)

ax.set_xticks(data["timestamps"][::max(1, len(data["timestamps"])//10)])
ax.set_xticklabels(data["timestamps"][::max(1, len(data["timestamps"])//10)], rotation=45, fontsize=8)
ax.set_facecolor("#f5f5f5")
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend(loc="upper left", fontsize=7)
ax.set_title("Sepsis Vital Trends (Live)", fontsize=12)
st.pyplot(fig, use_container_width=True)

# Risk trend line chart
fig2, ax2 = plt.subplots(figsize=(12, 2.5))
ax2.plot(data["timestamps"], data["Risk"], color="darkred", linewidth=2)
ax2.axhline(y=80, color="red", linestyle="--", linewidth=1)
ax2.axhline(y=50, color="orange", linestyle="--", linewidth=1)
ax2.axhline(y=30, color="green", linestyle="--", linewidth=1)
ax2.set_ylim([0, 100])
ax2.set_xticks(data["timestamps"][::max(1, len(data["timestamps"])//10)])
ax2.set_xticklabels(data["timestamps"][::max(1, len(data["timestamps"])//10)], rotation=45, fontsize=8)
ax2.set_title("Risk Score Trend (%)", fontsize=11)
ax2.grid(True, linestyle=":", alpha=0.6)
st.pyplot(fig2, use_container_width=True)

# Auto-refresh (simulate live data)
time.sleep(REFRESH_INTERVAL)
st.rerun()
