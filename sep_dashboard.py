import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# Simulated patient data for 12 hours
hours = pd.date_range(end=datetime.datetime.now(), periods=12, freq='H')
data = pd.DataFrame({
    'Time': hours,
    'Heart Rate': np.random.randint(70, 120, size=12),
    'Systolic BP': np.random.randint(90, 130, size=12),
    'SpO2': np.random.randint(90, 100, size=12),
    'Temperature': np.round(np.random.uniform(36.5, 39.0, size=12), 1),
    'Lactate': np.round(np.linspace(1.0, 3.5, num=12), 1)
})

# Sepsis Risk Score (basic logic)
risk_score = int((data['Lactate'].iloc[-1] - 1.0) * 30 + (120 - data['Systolic BP'].iloc[-1]) + (100 - data['SpO2'].iloc[-1]))
risk_score = min(max(risk_score, 0), 100)

# Streamlit UI
st.title("Sepsis Risk Monitoring Dashboard")
st.subheader("Patient Vitals Over Last 12 Hours")
st.line_chart(data.set_index('Time')[['Heart Rate', 'Systolic BP', 'SpO2', 'Temperature', 'Lactate']])

st.subheader("AI Estimated Sepsis Risk")
st.progress(risk_score)
st.metric(label="Sepsis Risk Score", value=f"{risk_score}/100")

if risk_score >= 60:
    st.error("Alert: Rising risk of sepsis detected. Consider checking lactate and blood pressure.")
elif risk_score >= 30:
    st.warning("Warning: Mild increase in risk. Monitor closely.")
else:
    st.success("Patient stable.")
