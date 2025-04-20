import streamlit as st import pandas as pd import numpy as np import time from datetime import datetime, timedelta

st.set_page_config(page_title="Live ICU Monitor", layout="wide") st.title("Live ICU Sepsis Risk Monitor")

Initialize session state for simulation

if 'data' not in st.session_state: base_time = datetime.now() - timedelta(hours=1) times = [base_time + timedelta(minutes=i*5) for i in range(12)] st.session_state.data = pd.DataFrame({ 'Time': times, 'Heart Rate': np.random.randint(80, 110, size=12), 'Systolic BP': np.random.randint(100, 120, size=12), 'SpO2': np.random.randint(92, 98, size=12), 'Temperature': np.round(np.random.uniform(36.8, 38.5, size=12), 1), 'Lactate': np.round(np.linspace(1.0, 2.8, num=12), 2) })

Simulate new data every run

new_row = { 'Time': datetime.now(), 'Heart Rate': np.random.randint(80, 120), 'Systolic BP': np.random.randint(90, 130), 'SpO2': np.random.randint(90, 100), 'Temperature': round(np.random.uniform(36.5, 39.0), 1), 'Lactate': round(np.random.uniform(1.0, 4.0), 2) }

Append and keep only recent 12 entries

st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True) st.session_state.data = st.session_state.data.iloc[-12:]

Risk calculation

last = st.session_state.data.iloc[-1] risk_score = int((last['Lactate'] - 1.0) * 30 + (120 - last['Systolic BP']) + (100 - last['SpO2'])) risk_score = min(max(risk_score, 0), 100)

Layout

col1, col2 = st.columns([3, 1])

with col1: st.subheader("Vitals - Last Hour") st.line_chart(st.session_state.data.set_index('Time')[['Heart Rate', 'Systolic BP', 'SpO2', 'Temperature', 'Lactate']])

with col2: st.subheader("Sepsis Risk") st.metric(label="Risk Score", value=f"{risk_score}/100") st.progress(risk_score) if risk_score >= 60: st.error("High Risk: Possible Sepsis. Alert staff.") elif risk_score >= 30: st.warning("Moderate Risk: Monitor closely.") else: st.success("Low Risk")

st.caption("Data simulated every run. Refresh page to simulate new vitals.")