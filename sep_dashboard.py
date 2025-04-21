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
expected_keys = ["timestamps", "HR", "Temp", "RR", "SpO2", "Lactate", "BP_sys"]

if "trend_data" not in st.session_state:
    st.session_state.trend_data = {}

for key in expected_keys:
    if key not in st.session_state.trend_data:
        st.session_state.trend_data[key] = []

# Simulate new vitals
def simulate_vitals():
    bp_sys = random.randint(90, 140)
    return {
        "HR": random.randint(60, 140),
        "Temp": round(random.uniform(36.0, 40.0), 1),
        "RR": random.randint(10, 30),
        "SpO2": random.randint(85, 100),
        "Lactate": round(random.uniform(0.5, 4.5), 2),
        "BP_sys": bp_sys
    }

# Update data
def update_data():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    vitals = simulate_vitals()
    st.session_state.trend_data["timestamps"].append(now)
    for k, v in vitals.items():
        st.session_state.trend_data[k].append(v)
        if len(st.session_state.trend_data[k]) > 300:
            st.session_state.trend_data[k].pop(0)
    if len(st.session_state.trend_data["timestamps"]) > 300:
        st.session_state.trend_data["timestamps"].pop(0)

update_data()

# Calculate risk level
latest = st.session_state.trend_data
hr = latest["HR"][-1]
temp = latest["Temp"][-1]
rr = latest["RR"][-1]
spo2 = latest["SpO2"][-1]
lactate = latest["Lactate"][-1]
bp = latest["BP_sys"][-1]

# Simple risk calculation based on thresholds
risk_score = 0
risk_score += 1 if hr > 120 or hr < 60 else 0
risk_score += 1 if temp > 39 or temp < 36 else 0
risk_score += 1 if rr > 25 or rr < 12 else 0
risk_score += 1 if spo2 < 90 else 0
risk_score += 1 if lactate > 2.5 else 0
risk_score += 1 if bp < 100 else 0

risk_percent = int((risk_score / 6) * 100)
if risk_percent < 30:
    risk_color = "green"
elif risk_percent < 70:
    risk_color = "orange"
else:
    risk_color = "red"

# Display dashboard
st.title("🦠 Live Sepsis Monitoring Dashboard")
st.markdown(f"### 🔥 Risk Level: <span style='color:{risk_color}; font-size: 24px;'>{risk_percent}%</span>", unsafe_allow_html=True)

# Vital metrics
col1, col2, col3 = st.columns(3)
data = st.session_state.trend_data

col1.metric("Heart Rate (HR)", f"{data['HR'][-1]} bpm")
col2.metric("Temperature (°C)", f"{data['Temp'][-1]}")
col3.metric("Respiratory Rate (RR)", f"{data['RR'][-1]}")

col1.metric("Oxygen Saturation (SpO₂)", f"{data['SpO2'][-1]} %")
col2.metric("Lactate (mmol/L)", f"{data['Lactate'][-1]}")
col3.metric("Systolic BP", f"{data['BP_sys'][-1]} mmHg")

# Combined trend chart
fig, ax = plt.subplots(figsize=(10, 4))
colors = {
    "HR": "red", "Temp": "orange", "RR": "green",
    "SpO2": "blue", "Lactate": "purple", "BP_sys": "gray"
}

for key in ["HR", "Temp", "RR", "SpO2", "Lactate", "BP_sys"]:
    ax.plot(data["timestamps"], data[key], label=key, color=colors[key], linewidth=1)

ax.set_xticks(data["timestamps"][::max(1, len(data["timestamps"])//8)])
ax.set_xticklabels(data["timestamps"][::max(1, len(data["timestamps"])//8)], rotation=45, fontsize=8)
ax.set_yticks([])
ax.set_facecolor("#f5f5f5")
ax.legend(loc="upper left", fontsize=8)
ax.set_title("Sepsis Vital Trends (Live)", fontsize=12)
st.pyplot(fig, use_container_width=True)

# Auto-refresh (simulate live data)
time.sleep(REFRESH_INTERVAL)
st.experimental_rerun()
