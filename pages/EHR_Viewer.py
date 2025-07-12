import streamlit as st
from utils.ehr_mock_data import get_mock_ehr

st.set_page_config(page_title="EHR Viewer", layout="wide", page_icon="📁", initial_sidebar_state="collapsed")

st.markdown("""
<style>
        body, .markdown-text-container, .stMarkdown, .stTextInput, .stTextInput input,
    .ehr-header, .ehr-box, .ehr-section-title, .ehr-subtitle, .stTextInput label,
    .stMarkdown p, .stMarkdown div {
        color: #222 !important;
    }
            /* Force Streamlit into light mode */
html, body, .stApp {
    background-color: #f8fff8 !important;
    color-scheme: light !important;
    color: #222 !important;
}

/* Force text color to dark */
h1, h2, h3, h4, h5, h6, p, div, span, label, input, textarea, .stMarkdown, .markdown-text-container {
    color: #222 !important;
}

/* Fix Streamlit input box in dark mode */
input, textarea {
    background-color: white !important;
    color: #222 !important;
    border: 1px solid #ccc !important;
}


    .ehr-header {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,100,0,0.1);
        border-top: 5px solid #28a745;
        text-align: center;
        margin: 2rem 0 1rem;
    }
    .ehr-title {
        color: #006400 !important;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.2rem;
    }
    .ehr-subtitle {
        color: #666;
        font-size: 1.1rem;
    }
    .ehr-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,100,0,0.08);
        border-left: 4px solid #28a745;
    }
    .ehr-section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #006400;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
    }
    .ehr-section-title:before {
        content: "📌";
        margin-right: 10px;
    }
    .stTextInput input {
        background-color: white !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    .stTextInput input:focus {
        border-color: #28a745 !important;
        box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="ehr-header">
    <div class="ehr-title">📁 ABHA-Linked Health Records</div>
    <div class="ehr-subtitle">View secure patient history linked to ABHA ID</div>
</div>
""", unsafe_allow_html=True)

# Use previously submitted ABHA ID
default_abha = st.session_state.get("submitted_abha_id", "")
abha_id = st.text_input("Enter ABHA ID", value=default_abha, placeholder="XX-XXXX-XXXX-XXXX", max_chars=17)

if abha_id:
    ehr = get_mock_ehr(abha_id)

    with st.container():
        st.markdown('<div class="ehr-box">', unsafe_allow_html=True)
        st.markdown('<div class="ehr-section-title">🏥 Clinical Visits</div>', unsafe_allow_html=True)
        for visit in ehr["clinical_visits"]:
            st.markdown(f"- {visit['date']}: **{visit['doctor']}** ({visit['department']}) — _{visit['diagnosis']}_")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="ehr-box">', unsafe_allow_html=True)
        st.markdown('<div class="ehr-section-title">💊 Medications</div>', unsafe_allow_html=True)
        for med in ehr["medications"]:
            line = f"- **{med['name']}** ({med['dose']}) — {med['frequency']} since {med['start_date']}"
            if "end_date" in med:
                line += f", till {med['end_date']}"
            st.markdown(line)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="ehr-box">', unsafe_allow_html=True)
        st.markdown('<div class="ehr-section-title">🧪 Lab Reports</div>', unsafe_allow_html=True)
        for lab in ehr["lab_tests"]:
            st.markdown(f"- {lab['date']}: **{lab['test']}** — *{lab['result']}*")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="ehr-box">', unsafe_allow_html=True)
        st.markdown('<div class="ehr-section-title">📈 Vitals History</div>', unsafe_allow_html=True)
        for v in ehr["vitals_history"]:
            st.markdown(f"- {v['date']}: BP: **{v['bp']}**, Pulse: **{v['pulse']} bpm**, Temp: **{v['temp']}°C**, SpO₂: **{v['spo2']}%**")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("🔍 Please enter a valid ABHA ID to view linked health records.")
