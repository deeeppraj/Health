import streamlit as st
from utils.data_extract import save_patient_data, get_mock_profile
import datetime

st.set_page_config(
    page_title="Hospital Health Kiosk",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🏥"
)

st.markdown("""
<meta name="color-scheme" content="light">
<style>
    .main > div { padding-top: 2rem; }
    .stApp { background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%); }
    .main .block-container { color: #333333; }
    p, div, span, h1, h2, h3, h4, h5, h6, label, input, textarea, select {
        color: #333333 !important;
    }
    .header-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,100,0,0.1);
        border-top: 5px solid #28a745;
        text-align: center;
        margin-bottom: 2rem;
    }
    .header-title {
        color: #006400 !important;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .subtitle {
        color: #666 !important;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    .status-badges {
        display: flex;
        justify-content: center;
        gap: 15px;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    .badge {
        background: #28a745;
        color: white !important;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .section-box {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,100,0,0.08);
        border-left: 4px solid #28a745;
    }
    .section-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        color: #006400 !important;
        font-size: 1.3rem;
        font-weight: 600;
    }
    .step-number {
        background: #28a745;
        color: white !important;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 10px;
        font-size: 0.9rem;
    }
    .patient-info {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border: 1px solid #28a745;
    }
    .patient-info h4 {
        color: #006400 !important;
        margin-bottom: 10px;
    }
    .patient-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 10px;
        margin-top: 10px;
    }
    .patient-detail {
        background: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
    }
    .patient-detail .label {
        font-size: 0.9rem;
        color: #666 !important;
        margin-bottom: 5px;
    }
    .patient-detail .value {
        font-weight: bold;
        color: #006400 !important;
    }
    .vitals-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
    }
    .vital-box {
        background: #f8fff8;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0f2e0;
    }
    .footer {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: #666 !important;
        margin-top: 2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .emergency-info {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404 !important;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        text-align: center;
    }
    .success-info {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724 !important;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e0e0e0;
        border-radius: 4px;
        margin-bottom: 20px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #28a745, #20c997);
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: #28a745 !important;
        box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.2) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #28a745, #20c997) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        font-size: 1.1rem !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3) !important;
    }
    .stButton > button:disabled {
        background: #cccccc !important;
        color: #666666 !important;
        cursor: not-allowed !important;
    }
    #MainMenu, footer, header, .stDeployButton, [data-testid="stDecoration"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <h1 class="header-title">🏥 AI Health Kiosk</h1>
    <p class="subtitle">Mediview Hospital - Digital Health Assessment</p>
    <div class="status-badges">
        <span class="badge">🛡️ ABDM-Compliant</span>
        <span class="badge">🔒 Secure</span>
        <span class="badge">🌿 Paperless</span>
        <span class="badge">🤖 AI-Powered</span>
    </div>
</div>
""", unsafe_allow_html=True)

if 'form_progress' not in st.session_state:
    st.session_state.form_progress = 0

progress_html = f"""
<div class="progress-bar">
    <div class="progress-fill" style="width: {st.session_state.form_progress}%"></div>
</div>
"""
st.markdown(progress_html, unsafe_allow_html=True)

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="step-number">1</div>
    <span>👤 Patient Identification</span>
</div>
""", unsafe_allow_html=True)

abha_id = st.text_input("**ABHA ID (14-digit)**", max_chars=17, placeholder="XX-XXXX-XXXX-XXXX")
profile = {}

if abha_id:
    abha_clean = abha_id.replace('-', '').replace(' ', '')
    if len(abha_clean) >= 10:
        try:
            profile = get_mock_profile(abha_id)
            if profile and isinstance(profile, dict) and profile.get('name'):
                st.markdown(f"""
                <div class="patient-info">
                    <h4>✅ Patient Verified</h4>
                    <div class="patient-details">
                        <div class="patient-detail">
                            <div class="label">Name</div>
                            <div class="value">{profile.get('name', 'N/A')}</div>
                        </div>
                        <div class="patient-detail">
                            <div class="label">Age</div>
                            <div class="value">{profile.get('age', 'N/A')} yrs</div>
                        </div>
                        <div class="patient-detail">
                            <div class="label">Gender</div>
                            <div class="value">{profile.get('gender', 'N/A')}</div>
                        </div>
                        <div class="patient-detail">
                            <div class="label">Blood Group</div>
                            <div class="value">{profile.get('blood_group', 'N/A')}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("❌ Patient not found in database.")
                st.info("💡 You can still proceed with health assessment.")
        except Exception as e:
            st.error("❌ Error fetching profile.")
            st.info("💡 You can still proceed with health assessment.")
    else:
        st.info("📝 Please enter a complete 14-digit ABHA ID")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="step-number">2</div>
    <span>❤️ Vital Signs</span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="vital-box">', unsafe_allow_html=True)
    bp = st.text_input("🩺 **Blood Pressure (mmHg)**", placeholder="e.g. 120/80")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="vital-box">', unsafe_allow_html=True)
    temp = st.number_input("🌡️ **Temperature (°C)**", min_value=35.0, max_value=45.0, step=0.1, format="%.1f")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="vital-box">', unsafe_allow_html=True)
    pulse = st.number_input("💓 **Pulse Rate (bpm)**", min_value=30, max_value=180, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="vital-box">', unsafe_allow_html=True)
    spo2 = st.number_input("🫁 **SpO₂ (%)**", min_value=70, max_value=100, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="step-number">3</div>
    <span>📋 Symptoms & Concerns</span>
</div>
""", unsafe_allow_html=True)

symptoms = st.text_area("**Describe your symptoms in detail**", 
                       placeholder="e.g., cough, headache, fatigue, pain...", 
                       height=120)
st.markdown('</div>', unsafe_allow_html=True)

progress = 0
if abha_id and len(abha_id.replace('-', '').replace(' ', '')) >= 14:
    progress += 30
if bp or temp or pulse or spo2:
    progress += 40
if symptoms:
    progress += 30
st.session_state.form_progress = progress

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <div class="step-number">4</div>
    <span>📤 Submit Assessment</span>
</div>
""", unsafe_allow_html=True)

can_submit = abha_id and (bp or temp or pulse or spo2 or symptoms)

if not can_submit:
    st.markdown("""
    <div class="emergency-info">
        ⚠️ Please enter your ABHA ID and at least one health parameter before submitting.
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("✅ Submit Health Assessment", disabled=not can_submit, key="submit_btn"):
        if can_submit:
            timestamp = datetime.datetime.now().isoformat()
            patient_data = {
                "abha_id": abha_id,
                "profile": profile,
                "vitals": {
                    "bp": bp,
                    "temp": temp if temp > 0 else None,
                    "pulse": pulse if pulse > 0 else None,
                    "spo2": spo2 if spo2 > 0 else None
                },
                "symptoms": symptoms,
                "timestamp": timestamp
            }
            try:
                save_patient_data(abha_id, patient_data)
                st.markdown("""
                <div class="success-info">
                    ✅ Health data submitted successfully! Your assessment has been recorded.
                </div>
                """, unsafe_allow_html=True)
                #st.balloons()
                st.markdown(f"**📅 Timestamp:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                st.session_state.form_progress = 100

                st.markdown("""
                <div class="section-box">
                    <div class="section-header">
                        <div class="step-number">5</div>
                        <span>🚀 What's Next?</span>
                    </div>
                """, unsafe_allow_html=True)

                next_option = st.radio("Choose your next step:",
                                       ["📁 View ABHA-Linked EHR", "🩺 Book Teleconsultation"],
                                       index=0)

                if next_option == "📁 View ABHA-Linked EHR":
                    st.markdown("🔗 Click [here](./EHR_Viewer) to view full health records.", unsafe_allow_html=True)
                else:
                    st.markdown("📞 Click [here](./Teleconsultation) to begin teleconsultation.", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error("❌ Submission error")

            except Exception as e:
                st.error("❌ Submission error")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="emergency-info">
    🚨 <strong>Emergency?</strong> Call 108 immediately or press the emergency button at the help desk.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    <p><strong>🛡️ ABDM-Compliant System | Mediview Hospital</strong></p>
    <p>📞 Emergency: 108 | ℹ️ Help Desk: 1800-XXX-XXXX</p>
    <p>🔐 Your health data is secure and encrypted</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.form_progress != progress:
    st.rerun()
