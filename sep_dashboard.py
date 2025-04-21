import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import datetime
import pandas as pd

st.set_page_config(layout="wide", page_title="Enhanced ICU Dashboard")

# Auto-refresh interval
REFRESH_INTERVAL = 1
st_autorefresh = st.empty()

# Session state setup
metrics_keys = [
    "timestamps", "HR", "Temp", "RR", "SpO2", "FiO2", "BP_sys", "BP_dia", "PulsePressure", "MAP",
    "Lactate", "WBC", "Platelets", "Creatinine", "Bilirubin", "Glucose", "CRP", "ALT", "AST",
    "GCS", "SOFA", "qSOFA", "NEWS2", "Risk"
]

if "trend_data" not in st.session_state:
    st.session_state.trend_data = {}

for key in metrics_keys:
    if key not in st.session_state.trend_data:
        st.session_state.trend_data[key] = []

# Simulated vitals
def simulate_vitals():
    bp_sys = random.randint(90, 140)
    bp_dia = random.randint(60, 90)
    pulse_pressure = bp_sys - bp_dia
    map_val = round((bp_sys + 2 * bp_dia) / 3, 1)
    return {
        "HR": random.randint(60, 140),
        "Temp": round(random.uniform(36.0, 40.0), 1),
        "RR": random.randint(10, 30),
        "SpO2": random.randint(85, 100),
        "FiO2": random.choice([21, 30, 40, 50, 60, 80, 100]),
        "BP_sys": bp_sys,
        "BP_dia": bp_dia,
        "PulsePressure": pulse_pressure,
        "MAP": map_val,
        "Lactate": round(random.uniform(0.5, 4.5), 2),
        "WBC": round(random.uniform(4.0, 15.0), 1),
        "Platelets": random.randint(100, 400),
        "Creatinine": round(random.uniform(0.5, 2.5), 2),
        "Bilirubin": round(random.uniform(0.2, 3.0), 2),
        "Glucose": round(random.uniform(3.0, 12.0), 1),
        "CRP": round(random.uniform(1, 200), 1),
        "ALT": round(random.uniform(10, 100), 1),
        "AST": round(random.uniform(10, 100), 1),
        "GCS": random.randint(3, 15)
    }

# Risk scoring (simplified)
def calculate_risk(v):
    score = 0
    score += 1 if v["HR"] > 120 or v["HR"] < 60 else 0
    score += 1 if v["Temp"] > 39 or v["Temp"] < 36 else 0
    score += 1 if v["RR"] > 25 or v["RR"] < 12 else 0
    score += 1 if v["SpO2"] < 90 else 0
    score += 1 if v["Lactate"] > 2.5 else 0
    score += 1 if v["BP_sys"] < 100 else 0
    score += 1 if v["WBC"] < 4 or v["WBC"] > 12 else 0
    score += 1 if v["Creatinine"] > 1.5 else 0
    score += 1 if v["Bilirubin"] > 2.0 else 0
    score += 1 if v["Platelets"] < 150 else 0
    score += 1 if v["MAP"] < 65 else 0
    score += 1 if v["GCS"] < 13 else 0
    return int((score / 12) * 100)

def update_data():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    v = simulate_vitals()
    st.session_state.trend_data["timestamps"].append(now)

    for k, val in v.items():
        st.session_state.trend_data[k].append(val)

    st.session_state.trend_data["SOFA"].append(random.randint(0, 24))
    st.session_state.trend_data["qSOFA"].append(random.randint(0, 3))
    st.session_state.trend_data["NEWS2"].append(random.randint(0, 20))

    risk = calculate_risk(v)
    st.session_state.trend_data["Risk"].append(risk)

    # Trim data
    max_len = 300
    for key in metrics_keys:
        if len(st.session_state.trend_data[key]) > max_len:
            st.session_state.trend_data[key] = st.session_state.trend_data[key][-max_len:]

update_data()
data = st.session_state.trend_data

# HEADER + ALERT
st.title("🧠 Enhanced ICU Monitoring Dashboard")
current_risk = data["Risk"][-1]
risk_color = "green" if current_risk < 30 else "orange" if current_risk < 70 else "red"
if current_risk >= 80:
    st.error("🚨 Critical Risk: Immediate clinical review required!", icon="⚠️")
st.markdown(f"### 🔥 Current Risk: <span style='color:{risk_color}; font-size: 24px;'>{current_risk}%</span>", unsafe_allow_html=True)

# METRICS VIEW
panels = st.columns(4)

def show_metrics(label, value, col):
    col.metric(label, value)

metrics = [
    ("HR", f"{data['HR'][-1]} bpm"),
    ("Temp", f"{data['Temp'][-1]} °C"),
    ("RR", f"{data['RR'][-1]} bpm"),
    ("SpO₂", f"{data['SpO2'][-1]} %"),
    ("FiO₂", f"{data['FiO2'][-1]} %"),
    ("Systolic BP", f"{data['BP_sys'][-1]} mmHg"),
    ("Diastolic BP", f"{data['BP_dia'][-1]} mmHg"),
    ("Pulse Pressure", f"{data['PulsePressure'][-1]} mmHg"),
    ("MAP", f"{data['MAP'][-1]} mmHg"),
    ("Lactate", f"{data['Lactate'][-1]} mmol/L"),
    ("WBC", f"{data['WBC'][-1]} x10⁹/L"),
    ("Platelets", f"{data['Platelets'][-1]} x10⁹/L"),
    ("Creatinine", f"{data['Creatinine'][-1]} mg/dL"),
    ("Bilirubin", f"{data['Bilirubin'][-1]} mg/dL"),
    ("Glucose", f"{data['Glucose'][-1]} mmol/L"),
    ("CRP", f"{data['CRP'][-1]} mg/L"),
    ("ALT", f"{data['ALT'][-1]} U/L"),
    ("AST", f"{data['AST'][-1]} U/L"),
    ("GCS", f"{data['GCS'][-1]}"),
    ("SOFA", f"{data['SOFA'][-1]}"),
    ("qSOFA", f"{data['qSOFA'][-1]}"),
    ("NEWS2", f"{data['NEWS2'][-1]}")
]

for i, (label, val) in enumerate(metrics):
    show_metrics(label, val, panels[i % 4])

# GRAPHS
fig, ax = plt.subplots(figsize=(12, 5))
plot_keys = ["HR", "Temp", "RR", "SpO2", "MAP", "Lactate", "Creatinine"]
colors = ["red", "orange", "green", "blue", "purple", "brown", "black"]

for i, key in enumerate(plot_keys):
    ax.plot(data["timestamps"], data[key], label=key, color=colors[i], linewidth=1)

ax.set_xticks(data["timestamps"][::max(1, len(data["timestamps"])//10)])
ax.set_xticklabels(data["timestamps"][::max(1, len(data["timestamps"])//10)], rotation=45, fontsize=8)
ax.legend(loc="upper left", fontsize=7)
ax.set_title("Vital Trends", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.4)
ax.set_facecolor("#f5f5f5")
st.pyplot(fig, use_container_width=True)

# RISK TREND
fig2, ax2 = plt.subplots(figsize=(12, 2.5))
ax2.plot(data["timestamps"], data["Risk"], color="darkred", linewidth=2)
ax2.axhline(y=80, color="red", linestyle="--")
ax2.set_ylim([0, 100])
ax2.set_xticks(data["timestamps"][::max(1, len(data["timestamps"])//10)])
ax2.set_xticklabels(data["timestamps"][::max(1, len(data["timestamps"])//10)], rotation=45, fontsize=8)
ax2.set_title("Risk Score Trend (%)")
ax2.grid(True, linestyle=":", alpha=0.6)
st.pyplot(fig2, use_container_width=True)

# EXPORT OPTION
if st.button("📥 Export Data CSV"):
    df = pd.DataFrame(data)
    st.download_button("Download CSV", df.to_csv(index=False), file_name="icu_dashboard_data.csv")

# Auto-refresh
time.sleep(REFRESH_INTERVAL)
st.experimental_rerun()
