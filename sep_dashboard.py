import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
import matplotlib.pyplot as plt

# Simulate vitals data for a condition
def generate_vital_trends(mean=0.5, std_dev=0.1):
    time_range = pd.date_range(end=datetime.datetime.now(), periods=24, freq='H')
    values = np.clip(np.random.normal(mean, std_dev, len(time_range)), 0, 1)
    return pd.Series(values, index=time_range)

# More advanced condition box with trend explanation and alerts
def condition_box(name, trend):
    avg_value = trend.mean()
    risk_score = avg_value * 100
    alert_level = "Normal"
    alert_color = "green"

    if risk_score > 80:
        alert_level = "Critical"
        alert_color = "red"
    elif risk_score > 60:
        alert_level = "High"
        alert_color = "orange"
    elif risk_score > 40:
        alert_level = "Moderate"
        alert_color = "yellow"

    with st.container():
        st.subheader(name)
        st.metric(label="Risk Score", value=f"{risk_score:.1f}", delta=f"{(risk_score - 50):+.1f}")
        st.markdown(f"**Alert Level:** :{alert_color}[{alert_level}]")
        st.line_chart(trend)
        st.caption("Trend based on recent 24-hour vitals simulation")

# ICU Dashboard Title
st.title("ICU Multi-Condition Intelligent Dashboard")
st.markdown("This dashboard shows live trends and AI-estimated risks for critical conditions in the ICU.")

# Example conditions to simulate
conditions_data = {
    "Sepsis": generate_vital_trends(mean=0.65),
    "Acute Kidney Injury": generate_vital_trends(mean=0.55),
    "ARDS": generate_vital_trends(mean=0.60),
    "Myocardial Infarction": generate_vital_trends(mean=0.45),
    "DKA (Diabetic Ketoacidosis)": generate_vital_trends(mean=0.50),
    "Pulmonary Embolism": generate_vital_trends(mean=0.52),
    "Stroke": generate_vital_trends(mean=0.48),
    "Hypovolemic Shock": generate_vital_trends(mean=0.70),
    "Severe Pneumonia": generate_vital_trends(mean=0.58),
    "Multi-Organ Failure": generate_vital_trends(mean=0.75),
    "Hyperkalemia": generate_vital_trends(mean=0.62),
    "Severe Hypertension": generate_vital_trends(mean=0.67)
}

# Display conditions in rows with 3 columns
conditions_list = list(conditions_data.items())
for i in range(0, len(conditions_list), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(conditions_list):
            condition_name, trend = conditions_list[i + j]
            with cols[j]:
                condition_box(condition_name, trend)


