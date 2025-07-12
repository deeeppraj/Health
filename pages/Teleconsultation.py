import streamlit as st
from utils.data_extract import get_patient_data
import datetime
import time

# Simple Configuration
st.set_page_config(
    page_title="Teleconsultation - Mediview",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🏥"
)

# Fixed CSS with proper text visibility
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    .stApp {
        background: #f8f9fa;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header */
    .header {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 2rem;
        border-left: 4px solid #28a745;
    }
    
    .header h1 {
        color: #28a745 !important;
        font-size: 2rem !important;
        margin: 0 !important;
    }
    
    .header p {
        color: #666 !important;
        margin: 0.5rem 0 0 0 !important;
        font-size: 1rem !important;
    }
    
    /* Section Container */
    .section-container {
        margin: 2rem 0;
    }
    
    .section-header {
        color: #28a745 !important;
        font-size: 1.4rem !important;
        margin-bottom: 1rem !important;
        border-bottom: 2px solid #28a745;
        padding-bottom: 0.5rem;
    }
    
    /* Input Section */
    .input-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .input-section h3 {
        color: #333 !important;
        margin-bottom: 1rem !important;
    }
    
    .stTextInput input {
        border: 2px solid #e0e0e0 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 16px !important;
        color: #333 !important;
    }
    
    .stTextInput input:focus {
        border-color: #28a745 !important;
        box-shadow: 0 0 0 3px rgba(40,167,69,0.1) !important;
    }
    
    /* Two Column Layout */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        height: 100%;
        border-left: 4px solid #28a745;
    }
    
    .info-card.error {
        border-left: 4px solid #dc3545;
    }
    
    .info-card.error h4 {
        color: #dc3545 !important;
    }
    
    .card-title {
        color: #28a745 !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .info-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .info-row:last-child {
        border-bottom: none;
    }
    
    .info-label {
        color: #666 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    .info-value {
        color: #333 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    .tag {
        background: #e7f3ff;
        color: #0366d6;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
    }
    
    .tag.normal { background: #e8f5e8; color: #28a745; }
    .tag.warning { background: #fff3cd; color: #856404; }
    .tag.danger { background: #f8d7da; color: #721c24; }
    
    /* Buttons */
    .stButton button {
        background: #28a745 !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton button:hover {
        background: #218838 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Doctor Section */
    .doctor-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    
    .doctor-info {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .doctor-avatar {
        width: 50px;
        height: 50px;
        background: #28a745;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.2rem;
    }
    
    .doctor-details h4 {
        color: #333 !important;
        margin: 0 !important;
        font-size: 1.1rem !important;
    }
    
    .doctor-details p {
        color: #666 !important;
        margin: 2px 0 !important;
        font-size: 13px !important;
    }
    
    /* Summary Section */
    .summary-card {
        background: #f8f9fa;
        border: 2px solid #28a745;
        padding: 2rem;
        border-radius: 12px;
        margin: 2rem 0;
    }
    
    .summary-card h3 {
        color: #28a745 !important;
        margin-bottom: 1rem !important;
    }
    
    .summary-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .summary-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #28a745;
    }
    
    .summary-item h4 {
        color: #333 !important;
        margin: 0 0 0.5rem 0 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    .summary-item p {
        color: #666 !important;
        margin: 0 !important;
        font-size: 0.8rem !important;
    }
    
    .summary-notes {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #ffc107;
    }
    
    .summary-notes h4 {
        color: #856404 !important;
        margin: 0 0 0.5rem 0 !important;
        font-size: 0.9rem !important;
    }
    
    .summary-notes p {
        color: #666 !important;
        margin: 0 !important;
        font-size: 0.8rem !important;
        line-height: 1.5;
    }
    
    /* Success Message */
    .success-container {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 2rem 0;
    }
    
    .success-container h3 {
        color: #155724 !important;
        margin-bottom: 1rem !important;
    }
    
    .meeting-link {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        word-break: break-all;
        border: 2px solid #28a745;
    }
    
    .meeting-link strong {
        color: #333 !important;
    }
    
    .meeting-link a {
        color: #28a745 !important;
        text-decoration: none;
    }
    
    /* Emergency cards text fix */
    .info-card h4 {
        color: #333 !important;
        margin: 0 0 0.5rem 0 !important;
        font-size: 1rem !important;
    }
    
    .info-card p {
        color: #666 !important;
        margin: 0.25rem 0 !important;
        font-size: 0.9rem !important;
    }
    
    .info-card strong {
        color: #333 !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'booking_confirmed' not in st.session_state:
    st.session_state.booking_confirmed = False
if 'selected_doctor' not in st.session_state:
    st.session_state.selected_doctor = None
if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

# Header
st.markdown("""
<div class="header">
    <h1>🏥 Teleconsultation</h1>
    <p>Quick Healthcare Consultation</p>
</div>
""", unsafe_allow_html=True)

# ABHA ID Input
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown("### 🔑 Enter ABHA ID")
abha_id = st.text_input("", placeholder="Enter your 14-digit ABHA ID", max_chars=17)
st.markdown('</div>', unsafe_allow_html=True)

# Main Content
if abha_id and len(abha_id.replace('-', '').replace(' ', '')) >= 14:
    with st.spinner('Loading patient data...'):
        time.sleep(1)
        data = get_patient_data(abha_id)
    
    if data:
        # Two Column Layout
        col1, col2 = st.columns(2)
        
        # Left Column - Patient Info
        with col1:
            st.markdown("""
            <div class="info-card">
                <h3 class="card-title">👤 Patient Information</h3>
                <div class="info-row">
                    <span class="info-label">Name</span>
                    <span class="info-value">{}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Age</span>
                    <span class="info-value">{} years</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Gender</span>
                    <span class="info-value">{}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Blood Group</span>
                    <span class="info-value">{}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">ABHA ID</span>
                    <span class="info-value">{}</span>
                </div>
            </div>
            """.format(
                data['profile'].get('name', 'Not Available'),
                data['profile'].get('age', 'N/A'),
                data['profile'].get('gender', 'Not specified'),
                data['profile'].get('blood_group', 'Not available'),
                abha_id
            ), unsafe_allow_html=True)
        
        # Right Column - Vitals
        with col2:
            vitals = data.get('vitals', {})
            
            # Function to get vital status
            def get_vital_status(vital_type, value):
                if vital_type == 'bp':
                    if value and '/' in str(value):
                        systolic = int(str(value).split('/')[0])
                        if systolic > 140: return 'danger'
                        elif systolic > 120: return 'warning'
                        else: return 'normal'
                elif vital_type == 'temp':
                    if value and float(value) > 100: return 'danger'
                    elif value and float(value) > 99: return 'warning'
                    else: return 'normal'
                elif vital_type == 'pulse':
                    if value and (int(value) > 100 or int(value) < 60): return 'warning'
                    else: return 'normal'
                elif vital_type == 'spo2':
                    if value and int(value) < 95: return 'danger'
                    elif value and int(value) < 98: return 'warning'
                    else: return 'normal'
                return 'normal'
            
            bp_status = get_vital_status('bp', vitals.get('bp'))
            temp_status = get_vital_status('temp', vitals.get('temp'))
            pulse_status = get_vital_status('pulse', vitals.get('pulse'))
            spo2_status = get_vital_status('spo2', vitals.get('spo2'))
            
            st.markdown("""
            <div class="info-card">
                <h3 class="card-title">📊 Vital Signs</h3>
                <div class="info-row">
                    <span class="info-label">Blood Pressure</span>
                    <div>
                        <span class="info-value">{}</span>
                        <span class="tag {}">{}</span>
                    </div>
                </div>
                <div class="info-row">
                    <span class="info-label">Temperature</span>
                    <div>
                        <span class="info-value">{}°C</span>
                        <span class="tag {}">{}</span>
                    </div>
                </div>
                <div class="info-row">
                    <span class="info-label">Heart Rate</span>
                    <div>
                        <span class="info-value">{} bpm</span>
                        <span class="tag {}">{}</span>
                    </div>
                </div>
                <div class="info-row">
                    <span class="info-label">SpO₂</span>
                    <div>
                        <span class="info-value">{}%</span>
                        <span class="tag {}">{}</span>
                    </div>
                </div>
            </div>
            """.format(
                vitals.get('bp', 'N/A'), bp_status, bp_status.upper(),
                vitals.get('temp', 'N/A'), temp_status, temp_status.upper(),
                vitals.get('pulse', 'N/A'), pulse_status, pulse_status.upper(),
                vitals.get('spo2', 'N/A'), spo2_status, spo2_status.upper()
            ), unsafe_allow_html=True)
        
        # Symptoms Section
        if data.get('symptoms'):
            st.markdown("""
            <div class="info-card" style="margin-top: 2rem;">
                <h3 class="card-title">📋 Symptoms</h3>
                <p style="color: #666; line-height: 1.6; margin: 0;">{}</p>
            </div>
            """.format(data.get('symptoms', 'No symptoms reported')), unsafe_allow_html=True)
        
        # Doctor Selection
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-header">👨‍⚕️ Available Doctors</h3>', unsafe_allow_html=True)
        
        doctors = [
            {
                "name": "Dr. Radhika Mehta",
                "specialty": "General Physician",
                "experience": "15+ years",
                "rating": "4.8/5",
                "avatar": "👩‍⚕️",
                "fee": 500,
                "status": "Available Now"
            },
            {
                "name": "Dr. Amit Sharma", 
                "specialty": "Internal Medicine",
                "experience": "12+ years",
                "rating": "4.7/5",
                "avatar": "👨‍⚕️",
                "fee": 600,
                "status": "Available in 30 mins"
            }
        ]
        
        for i, doctor in enumerate(doctors):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="doctor-card">
                    <div class="doctor-info">
                        <div class="doctor-avatar">{doctor['avatar']}</div>
                        <div class="doctor-details">
                            <h4>{doctor['name']}</h4>
                            <p>{doctor['specialty']} • {doctor['experience']}</p>
                            <p>⭐ {doctor['rating']} • <span class="tag normal">{doctor['status']}</span></p>
                            <p><strong>Fee: ₹{doctor['fee']}</strong></p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"Select Doctor", key=f"select_{i}"):
                    st.session_state.selected_doctor = doctor
                    st.session_state.show_summary = True
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show Summary Before Booking
        if st.session_state.show_summary and st.session_state.selected_doctor and not st.session_state.booking_confirmed:
            doctor = st.session_state.selected_doctor
            
            # Calculate urgency based on vitals
            urgent_vitals = []
            if bp_status == 'danger': urgent_vitals.append("High Blood Pressure")
            if temp_status == 'danger': urgent_vitals.append("Fever")
            if spo2_status == 'danger': urgent_vitals.append("Low Oxygen")
            
            urgency_level = "High" if urgent_vitals else "Normal"
            urgency_color = "#dc3545" if urgent_vitals else "#28a745"
            
            # Build the urgent vitals message properly
            urgent_vitals_html = ""
            if urgent_vitals:
                urgent_vitals_html = f"<p>• <strong>Urgent vitals detected:</strong> {', '.join(urgent_vitals)}</p>"
            
            st.markdown(f"""
<div class="summary-card">
    <h3>📋 Consultation Summary</h3>
    <div class="summary-grid">
        <div class="summary-item">
            <h4>Patient</h4>
            <p>{data['profile'].get('name', 'N/A')}, {data['profile'].get('age', 'N/A')} years</p>
        </div>
        <div class="summary-item">
            <h4>Selected Doctor</h4>
            <p>{doctor['name']}</p>
        </div>
        <div class="summary-item">
            <h4>Consultation Fee</h4>
            <p>₹{doctor['fee']}</p>
        </div>
        <div class="summary-item">
            <h4>Urgency Level</h4>
            <p style="color: {urgency_color}; font-weight: bold;">{urgency_level}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

            
            # Booking Confirmation Buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("◀️ Back to Doctors", key="back_to_doctors"):
                    st.session_state.show_summary = False
                    st.session_state.selected_doctor = None
                    st.rerun()
            
            with col2:
                if st.button("✅ Confirm Booking", key="confirm_booking"):
                    st.session_state.booking_confirmed = True
                    st.rerun()
            
            with col3:
                if st.button("❌ Cancel", key="cancel_booking"):
                    st.session_state.show_summary = False
                    st.session_state.selected_doctor = None
                    st.rerun()
        
        # Booking Confirmation
        if st.session_state.booking_confirmed and st.session_state.selected_doctor:
            doctor = st.session_state.selected_doctor
            consultation_id = f"TC{datetime.datetime.now().strftime('%Y%m%d%H%M')}{abha_id[-4:]}"
            meeting_link = f"https://mediview.consultation.secure/{consultation_id}"
            
            st.markdown(f"""
            <div class="success-container">
                <h3>✅ Consultation Booked Successfully!</h3>
                <div class="meeting-link">
                    <strong>Meeting Link:</strong><br>
                    <a href="{meeting_link}" target="_blank">{meeting_link}</a>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                    <div><strong>Doctor:</strong> {doctor['name']}</div>
                    <div><strong>Fee:</strong> ₹{doctor['fee']}</div>
                    <div><strong>Consultation ID:</strong> {consultation_id}</div>
                    <div><strong>Status:</strong> <span class="tag normal">Confirmed</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            #st.balloons()
            
            # Reset button
            if st.button("🔄 Book Another Consultation"):
                st.session_state.booking_confirmed = False
                st.session_state.selected_doctor = None
                st.session_state.show_summary = False
                st.rerun()
    
    else:
        st.error("❌ No health record found for this ABHA ID. Please verify and try again.")

# Emergency & Support Section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<h3 class="section-header">🚨 Emergency & Support</h3>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card error">
        <h4>🚨 Medical Emergency</h4>
        <p><strong>Call: 108</strong></p>
        <p>24/7 Emergency Services</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4>💬 Technical Support</h4>
        <p><strong>Call: 1800-XXX-XXXX</strong></p>
        <p>Available 24/7</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h4>📧 Customer Care</h4>
        <p><strong>support@mediview.com</strong></p>
        <p>Response within 2 hours</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)