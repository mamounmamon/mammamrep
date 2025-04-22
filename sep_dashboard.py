import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
import time
import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.set_page_config(layout="wide", page_title="Advanced ICU Sepsis & Condition Dashboard")

REFRESH_INTERVAL = 1
MAX_HISTORY = 300

if "trend_data" not in st.session_state:
    METRICS = [
        "HR", "Temp", "RR", "SpO2", "Lactate", "BP_sys",
        "WBC", "Platelets", "Creatinine", "Bilirubin", "MAP", "GCS",
        "Glucose", "Urine_Output", "INR", "FiO2", "pH", "PaCO2"
    ]
    st.session_state.trend_data = {metric: [] for metric in ["timestamps"] + METRICS + ["Sepsis_Risk", "ARDS_Risk", "Shock_Risk"]}

METRICS = [
    "HR", "Temp", "RR", "SpO2", "Lactate", "BP_sys",
    "WBC", "Platelets", "Creatinine", "Bilirubin", "MAP", "GCS",
    "Glucose", "Urine_Output", "INR", "FiO2", "pH", "PaCO2"
]

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

def update_data():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    vitals = simulate_vitals()
    st.session_state.trend_data["timestamps"].append(now)
    for k, v in vitals.items():
        st.session_state.trend_data[k].append(v)

    sepsis_score = sum([
        vitals["HR"] > 120 or vitals["HR"] < 60,
        vitals["Temp"] > 39 or vitals["Temp"] < 36,
        vitals["RR"] > 25 or vitals["RR"] < 12,
        vitals["SpO2"] < 90,
        vitals["Lactate"] > 2.5,
        vitals["BP_sys"] < 100,
        vitals["WBC"] < 4 or vitals["WBC"] > 12,
        vitals["Creatinine"] > 1.5,
        vitals["Bilirubin"] > 2.0,
        vitals["Platelets"] < 150,
        vitals["MAP"] < 65,
        vitals["GCS"] < 13
    ])

    ards_score = sum([
        vitals["FiO2"] > 50,
        vitals["pH"] < 7.3,
        vitals["PaCO2"] > 50,
        vitals["SpO2"] < 90
    ])

    shock_score = sum([
        vitals["MAP"] < 65,
        vitals["Lactate"] > 2,
        vitals["Urine_Output"] < 0.5,
        vitals["BP_sys"] < 100
    ])

    st.session_state.trend_data["Sepsis_Risk"].append(int((sepsis_score / 12) * 100))
    st.session_state.trend_data["ARDS_Risk"].append(int((ards_score / 4) * 100))
    st.session_state.trend_data["Shock_Risk"].append(int((shock_score / 4) * 100))

    for key in st.session_state.trend_data:
        if len(st.session_state.trend_data[key]) > MAX_HISTORY:
            st.session_state.trend_data[key] = st.session_state.trend_data[key][-MAX_HISTORY:]

update_data()

st.title("🧠 ICU Condition Intelligence Dashboard")
st.caption("Live monitoring of critical ICU metrics & predictive risks")

with st.container():
    col1, col2, col3 = st.columns(3)
    sepsis = st.session_state.trend_data["Sepsis_Risk"][-1]
    ards = st.session_state.trend_data["ARDS_Risk"][-1]
    shock = st.session_state.trend_data["Shock_Risk"][-1]

    col1.metric("Sepsis Risk", f"{sepsis}%", delta_color="normal")
    col2.metric("ARDS Risk", f"{ards}%", delta_color="inverse")
    col3.metric("Shock Risk", f"{shock}%", delta_color="off")

with st.expander("💛 Live Vitals", expanded=True):
    cols = st.columns(4)
    latest_values = {k: v[-1] for k, v in st.session_state.trend_data.items() if k != "timestamps"}
    for i, (k, v) in enumerate(latest_values.items()):
        label = k.replace("_", " ")
        cols[i % 4].metric(label=label, value=str(v))

with st.expander("📊 Cluster Insights", expanded=False):
    if len(st.session_state.trend_data["HR"]) >= 10:
        df = pd.DataFrame(st.session_state.trend_data)
        scaler = StandardScaler()
        X = scaler.fit_transform(df[METRICS])
        kmeans = KMeans(n_clusters=3, random_state=42)
        df["Cluster"] = kmeans.fit_predict(X)
        st.bar_chart(df["Cluster"].value_counts().sort_index())
        st.dataframe(df[["timestamps", "Cluster"] + METRICS].tail(10))
    else:
        st.info("Waiting for enough data to perform clustering...")

def draw_trend_chart(metric_list, title):
    data = st.session_state.trend_data
    fig, ax = plt.subplots(figsize=(12, 4))
    for metric in metric_list:
        ax.plot(data["timestamps"], data[metric], label=metric)
    ax.legend()
    ax.set_title(title)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    st.pyplot(fig)

with st.expander("📈 Trend Analysis Charts", expanded=False):
    draw_trend_chart(["HR", "RR", "Temp", "SpO2"], "🢫 Respiratory & Cardiovascular")
    draw_trend_chart(["WBC", "Lactate", "Platelets"], "🧪 Sepsis Indicators")
    draw_trend_chart(["Creatinine", "Bilirubin", "MAP", "GCS"], "🧠 Renal/Liver Function & Consciousness")
    draw_trend_chart(["Sepsis_Risk", "ARDS_Risk", "Shock_Risk"], "⚠️ Risk Scores Over Time")

with st.expander("⬇️ Export Data"):
    df = pd.DataFrame(st.session_state.trend_data)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download ICU Data as CSV", data=csv, file_name="icu_data.csv", mime="text/csv")

if st.button("Stop Refresh"):
    st.stop()
else:
    time.sleep(REFRESH_INTERVAL)
    st.experimental_rerun()
