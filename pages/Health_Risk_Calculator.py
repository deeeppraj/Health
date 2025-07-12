import streamlit as st
import numpy as np

st.set_page_config(page_title="Health Risk + Coaching", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    body, .main { background-color: #f4fdf8; }
    h1, h2, h3 { color: #176943; }
    .stButton>button { background-color: #176943; color: white; }
    .block-container { padding: 2rem 3rem; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Health Risk Calculator + 🧠 Lifestyle Coaching")
st.subheader("Estimate personal health risks and receive lifestyle recommendations")

col1, col2, col3 = st.columns(3)
age = col1.slider("Age", 10, 90, 30)
bmi = col2.slider("BMI", 10.0, 45.0, 22.0)
bp = col3.slider("Systolic BP", 80, 200, 120)

col4, col5 = st.columns(2)
smoker = col4.selectbox("Do you smoke?", ["No", "Yes"])
diabetic = col5.selectbox("Diabetes history?", ["No", "Yes"])

risk_factors = 0
if age > 45: risk_factors += 1
if bmi > 30: risk_factors += 1
if bp > 140: risk_factors += 1
if smoker == "Yes": risk_factors += 1
if diabetic == "Yes": risk_factors += 1

if st.button("Calculate Risk"):
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🩺 Risk Result")
        if risk_factors <= 1:
            st.success("✅ Low risk for chronic conditions.")
            risk_level = "Low"
        elif risk_factors == 2:
            st.warning("⚠️ Moderate risk. Consider regular screening.")
            risk_level = "Moderate"
        else:
            st.error("🚨 High risk. Medical consultation advised.")
            risk_level = "High"

    with col_b:
        st.subheader("🍎 Lifestyle Coaching")
        if risk_level == "Low":
            st.write("- Maintain your current routine.")
            st.write("- Balanced diet and 150 min of moderate activity per week.")
            st.write("- Annual checkups are recommended.")
        elif risk_level == "Moderate":
            st.write("- Adopt DASH or Mediterranean-style diet.")
            st.write("- Reduce sugar and saturated fats.")
            st.write("- Increase daily activity (brisk walk 30+ min).")
            st.write("- Quit smoking and limit alcohol.")
        else:
            st.write("- Strict dietary monitoring; consult a nutritionist.")
            st.write("- Engage in 45+ min of low-impact cardio most days.")
            st.write("- Completely avoid smoking, alcohol, and high-sodium foods.")
            st.write("- Monitor BP, blood glucose, and lipid profile monthly.")
