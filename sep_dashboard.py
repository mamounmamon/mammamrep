Sepsis Live Dashboard with Patient Selector and Real-time Charts

import streamlit as st import pandas as pd import numpy as np import time import random import plotly.graph_objs as go

st.set_page_config(page_title="Sepsis Live Dashboard", layout="wide") st.title("Sepsis Live Monitoring Dashboard")

Simulated list of ICU patients

patients = ["Patient A", "Patient B", "Patient C"] selected_patient = st.selectbox("Select Patient", patients)

Initialize session state

if "data" not in st.session_state: st.session_state.data = {p: pd.DataFrame(columns=["Time", "HR", "SpO2", "BP", "RR", "Temp", "Lactate"]) for p in patients}

def generate_new_data(): return { "Time": pd.Timestamp.now(), "HR": random.randint(90, 130), "SpO2": random.uniform(88, 100), "BP": random.randint(85, 120), "RR": random.randint(20, 35), "Temp": random.uniform(37.5, 39.5), "Lactate": round(random.uniform(2.0, 4.5), 2) }

def update_data(patient): new_row = generate_new_data() df = st.session_state.data[patient] df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True) # Limit to last 60 entries df = df.tail(60) st.session_state.data[patient] = df return df

Run update loop

placeholder = st.empty()

with placeholder.container(): while True: df = update_data(selected_patient)

col1, col2 = st.columns(2)
    with col1:
        st.metric("Heart Rate (HR)", f"{df.iloc[-1]['HR']} bpm")
        st.metric("Respiratory Rate (RR)", f"{df.iloc[-1]['RR']} bpm")
        st.metric("Temperature", f"{df.iloc[-1]['Temp']:.1f} °C")
    with col2:
        st.metric("SpO2", f"{df.iloc[-1]['SpO2']:.1f}%")
        st.metric("Blood Pressure (BP)", f"{df.iloc[-1]['BP']} mmHg")
        st.metric("Lactate", f"{df.iloc[-1]['Lactate']} mmol/L")

    # Trend charts
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Time"], y=df["HR"], mode='lines+markers', name='HR'))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["SpO2"], mode='lines+markers', name='SpO2'))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["BP"], mode='lines+markers', name='BP'))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["RR"], mode='lines+markers', name='RR'))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Temp"], mode='lines+markers', name='Temp'))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Lactate"], mode='lines+markers', name='Lactate'))

    fig.update_layout(title='Vital Signs Trend (Last Minute)', xaxis_title='Time', yaxis_title='Value',
                      height=500, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)

    time.sleep(1)
    st.experimental_rerun()

    
