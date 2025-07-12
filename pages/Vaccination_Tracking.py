import streamlit as st
from utils.vaccine_utils import load_vaccine_data, get_patient_vaccine_status

st.set_page_config(page_title="Vaccination Tracker", layout="centered",initial_sidebar_state='collapsed')
st.markdown("""
    <style>
        .main { background-color: #f6fff6; }
        .stTextInput > div > div > input {
            border: 2px solid #198754; border-radius: 8px;
        }
        .stDataFrame { border: 1px solid #198754; border-radius: 6px; }
        .stButton>button {
            background-color: #198754; color: white;
            border-radius: 8px; padding: 0.5em 1em;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 ABHA-Based Vaccination Tracker")

abha_id = st.text_input("Enter ABHA ID")

if abha_id:
    try:
        df = load_vaccine_data()
        patient_data = get_patient_vaccine_status(abha_id, df)

        if not patient_data.empty:
            st.success(f"Vaccination Records for {patient_data.iloc[0]['Name']}")
            st.dataframe(
                patient_data[["Vaccine", "Dose", "Due Date", "Status"]].set_index("Vaccine"),
                use_container_width=True
            )
        else:
            st.warning("No vaccination record found for this ABHA ID.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
