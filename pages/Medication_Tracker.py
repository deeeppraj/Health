import streamlit as st
import pandas as pd

st.set_page_config(page_title="Medication Management", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    body { background-color: #f8fdf8; }
    .main { background-color: #f8fdf8; }
    .css-1d391kg { background-color: #f8fdf8; }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 Medication Tracker")
st.subheader("Monitor active and completed medication schedules")

abha_id = st.text_input("Enter ABHA ID")

if abha_id:
    df = pd.read_csv("data/medication_data.csv", parse_dates=["Start Date", "End Date"])
    patient_data = df[df["ABHA_ID"] == abha_id]

    if patient_data.empty:
        st.warning("No records found for this ABHA ID.")
    else:
        today = pd.to_datetime("today").normalize()
        patient_data["Status"] = patient_data["End Date"].apply(lambda x: "Ongoing" if x >= today else "Completed")

        st.success(f"Found {len(patient_data)} medication record(s) for {abha_id}")
        st.dataframe(patient_data[["Medication", "Dosage", "Frequency", "Start Date", "End Date", "Status"]], use_container_width=True)
