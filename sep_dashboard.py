import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import datetime

st.set_page_config(layout="wide", page_title="Sepsis ICU Monitor")

REFRESH_INTERVAL = 1
if "last_refresh_time" not in st.session_state:
    st.session_state.last_refresh_time = time.time()

elapsed_time = time.time() - st.session_state.last_refresh_time
if elapsed_time > REFRESH_INTERVAL:
    st.session_state.last_refresh_time = time.time()
    st.rerun()

# Initialize session state
if "trend_data" not in st.session_state:
    st.session_state.trend_data = {
        "timestamps": [],
        "HR": [],
        "BP_sys": [],
        "BP_dia": [],
        "Temp": [],
        "SpO2": [],
        "RR": [],
        "Lactate": [],
        "WBC": []
    }

# Simulate vitals
bp_sys = random.randint(90, 140)
bp_dia = random.randint(60, 90)
vitals = {
    "HR": random.randint(60, 130),
    "BP_sys": bp_sys,
    "BP_dia": bp_dia,
    "Temp": round(random.uniform(36.0, 40.5), 1),
    "SpO2": random.randint(85, 100),
    "RR": random.randint(12, 28),
    "Lactate": round(random.uniform(0.5, 5.0), 2),
    "WBC": round(random.uniform(4.0, 20.0), 1)
}

now = datetime.datetime.now().strftime("%H:%M:%S")
st.session_state.trend_data["timestamps"].append(now)
for key in vitals:
    st.session_state.trend_data[key].append(vitals[key])
    if len(st.session_state.trend_data[key]) > 1440:
        st.session_state.trend_data[key].pop(0)
if len(st.session_state.trend_data["timestamps"]) > 1440:
    st.session_state.trend_data["timestamps"].pop(0)

# Risk assessment
def get_alert(v):
    score = 0
    score += v["HR"] > 110
    score += v["Temp"] > 38.5
    score += v["SpO2"] < 92
    score += v["Lactate"] > 2.5
    score += v["BP_sys"] < 95
    score += v["WBC"] > 12 or v["WBC"] < 4
    if score >= 5:
        return "🔴 High", "#ffcccc"
    elif score >= 3:
        return "🟠 Moderate", "#fff3cd"
    else:
        return "🟢 Low", "#d4edda"

alert_level, bg_color = get_alert(vitals)

# UI layout
st.markdown(f"""
    <div style='background-color: {bg_color}; padding: 1rem; border-radius: 10px;'>
        <h2>🧠 Sepsis Monitoring Dashboard</h2>
        <h4>Status: {alert_level}</h4>
    </div>
    <br>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("Heart Rate (HR)", f"{vitals['HR']} bpm")
col2.metric("Blood Pressure", f"{vitals['BP_sys']}/{vitals['BP_dia']}")
col3.metric("Temperature", f"{vitals['Temp']} °C")
col1.metric("SpO₂", f"{vitals['SpO2']}%")
col2.metric("Respiratory Rate", f"{vitals['RR']} bpm")
col3.metric("Lactate", f"{vitals['Lactate']} mmol/L")
col1.metric("WBC Count", f"{vitals['WBC']} x10⁹/L")

# Trend chart
with st.expander("📈 Show 24h Vital Trends", expanded=True):
    fig, ax = plt.subplots(figsize=(12, 4))
    t = st.session_state.trend_data["timestamps"][-100:]
    for key in ["HR", "Temp", "SpO2", "RR", "Lactate", "BP_sys", "WBC"]:
        y = st.session_state.trend_data[key][-100:]
        ax.plot(t, y, label=key)
    ax.legend()
    ax.set_xticks(t[::max(1, len(t)//10)])
    ax.set_xticklabels(t[::max(1, len(t)//10)], rotation=45)
    st.pyplot(fig)

st.caption("Auto-refreshing every 1 second · Sepsis focus · Simulated vitals")
