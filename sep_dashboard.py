import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import datetime

st.set_page_config(layout="wide", page_title="ICU Live Dashboard")

# Auto-refresh every 1 second
REFRESH_INTERVAL = 1
if "last_refresh_time" not in st.session_state:
    st.session_state.last_refresh_time = time.time()

elapsed_time = time.time() - st.session_state.last_refresh_time
if elapsed_time > REFRESH_INTERVAL:
    st.session_state.last_refresh_time = time.time()
    st.rerun()
else:
    remaining = REFRESH_INTERVAL - int(elapsed_time)
    st.markdown(f"<p style='color: gray; font-size: 12px;'>⏳ Auto-refreshing in {remaining}s...</p>", unsafe_allow_html=True)

# Styling
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 11px !important;
    }
    .big-title {
        font-size: 28px !important;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .card {
        border-radius: 16px;
        padding: 1rem;
        background-color: #ffffff;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .alert-low { color: green; }
    .alert-moderate { color: orange; }
    .alert-high { color: red; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="big-title">🧠 ICU AI Smart Monitoring Dashboard</div>', unsafe_allow_html=True)
st.caption("Smart alerts · Live 24h trends · Multivariable insight · 12 monitored ICU risks")

icu_conditions = [
    "Sepsis", "ARDS", "Cardiac Arrest", "Kidney Injury", "Liver Failure",
    "Pulmonary Embolism", "Stroke", "Hypoglycemia", "Hyperkalemia",
    "Hemorrhage", "Pneumonia", "Shock"
]

MAX_HISTORY_HOURS = 24
DATA_INTERVAL_MINUTES = 1
MAX_DATA_POINTS = MAX_HISTORY_HOURS * 60 // DATA_INTERVAL_MINUTES

if "trend_data" not in st.session_state:
    st.session_state.trend_data = {}
    for cond in icu_conditions:
        st.session_state.trend_data[cond] = {}
        for vital in ["HR", "Temp", "RR", "SpO2", "Lactate", "BP_sys", "BP_dia", "BP"]:
            st.session_state.trend_data[cond][vital] = []
        st.session_state.trend_data[cond]["timestamps"] = []

def simulate_vitals():
    bp_sys = random.randint(90, 140)
    bp_dia = random.randint(60, 90)
    return {
        "HR": random.randint(60, 140),
        "BP_sys": bp_sys,
        "BP_dia": bp_dia,
        "BP": f"{bp_sys}/{bp_dia}",
        "Temp": round(random.uniform(36.0, 40.0), 1),
        "SpO2": random.randint(85, 100),
        "RR": random.randint(10, 30),
        "Lactate": round(random.uniform(0.5, 4.5), 2)
    }

def alert_level(v):
    score = 0
    score += v["HR"] > 110
    score += v["Temp"] > 38.5
    score += v["SpO2"] < 92
    score += v["Lactate"] > 2.5
    score += v["BP_sys"] < 95

    if score >= 4:
        return "🔴 High", "alert-high"
    elif score >= 2:
        return "🟠 Moderate", "alert-moderate"
    else:
        return "🟢 Low", "alert-low"

def plot_combined_trends(condition):
    data = st.session_state.trend_data[condition]
    timestamps = data["timestamps"][-MAX_DATA_POINTS:]
    colors = {
        "HR": "red", "Temp": "orange", "RR": "green", "SpO2": "blue",
        "Lactate": "purple", "BP_sys": "gray"
    }
    fig, ax = plt.subplots(figsize=(6, 2.5))

    for key in ["HR", "Temp", "RR", "SpO2", "Lactate", "BP_sys"]:
        values = data[key][-MAX_DATA_POINTS:]
        ax.plot(timestamps, values, label=key, color=colors[key], linewidth=1.5)

    if len(timestamps) > 4:
        ax.set_xticks(timestamps[::max(1, len(timestamps)//4)])
        ax.set_xticklabels(timestamps[::max(1, len(timestamps)//4)], rotation=45, fontsize=6)
    else:
        ax.set_xticks([])

    ax.set_yticks([])
    ax.set_facecolor("#f7f7f7")
    ax.legend(fontsize=6, loc="upper left")
    st.pyplot(fig, use_container_width=True)

cols = st.columns(3)

for idx, condition in enumerate(icu_conditions):
    vitals = simulate_vitals()
    alert, alert_class = alert_level(vitals)

    data = st.session_state.trend_data[condition]
    now = datetime.datetime.now().strftime("%H:%M:%S")
    data["timestamps"].append(now)
    for k in vitals:
        if k in data:
            data[k].append(vitals[k])
            if len(data[k]) > MAX_DATA_POINTS:
                data[k].pop(0)
    if len(data["timestamps"]) > MAX_DATA_POINTS:
        data["timestamps"].pop(0)

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

            plot_combined_trends(condition)
            st.markdown("</div>", unsafe_allow_html=True)

st.caption("Auto-refreshing every 1 second · Monitoring 24h vitals · Simulated data for 12 ICU risk profiles")
