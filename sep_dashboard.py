import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import time

st.set_page_config(layout="wide", page_title="ICU Live Dashboard")

# Inject styles
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
st.markdown('<p class="big-title">🧠 ICU AI Risk Dashboard (Live)</p>', unsafe_allow_html=True)
st.caption("Vitals updated every 5 seconds · Simulated data")

# Auto-refresh every 5 seconds
countdown = 5
if "last_refresh" not in st.session_state:
    st.session_state["last_refresh"] = time.time()

elapsed = time.time() - st.session_state["last_refresh"]
if elapsed > countdown:
    st.session_state["last_refresh"] = time.time()
    st.experimental_rerun()

# ICU Conditions
icu_conditions = [
    "Sepsis", "ARDS", "Cardiac Arrest", "Kidney Injury", "Liver Failure",
    "Pulmonary Embolism", "Stroke", "Hypoglycemia", "Hyperkalemia",
    "Hemorrhage", "Pneumonia", "Shock"
]

def simulate_vitals():
    return {
        "HR": random.randint(60, 140),
        "BP": f"{random.randint(90, 120)}/{random.randint(60, 85)}",
        "Temp": round(random.uniform(36.0, 40.0), 1),
        "SpO2": random.randint(88, 100),
        "RR": random.randint
