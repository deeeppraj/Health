import streamlit as st

st.set_page_config(
    page_title="AI Health Kiosk Launcher",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f8fff8 50%, #f0f9f0 100%);
        font-family: 'Inter', sans-serif;
        color: #1a202c;
    }

    .main-header {
        background: linear-gradient(135deg, #ffffff 0%, #f8fff8 100%);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(0, 100, 0, 0.1);
        border: 1px solid rgba(25, 135, 84, 0.1);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #198754, #20c997, #198754);
        animation: shimmer 3s infinite;
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f5132;
        margin-bottom: 0.25rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #0f5132, #198754);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .header-subtitle {
        font-size: 1rem;
        color: #6c757d;
        font-weight: 400;
        margin-bottom: 0.75rem;
    }

    .status-badges {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 0.75rem;
    }

    .status-badge {
        background: linear-gradient(135deg, #198754, #20c997);
        color: white;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 11px;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(25, 135, 84, 0.3);
        transition: all 0.3s ease;
        border: none;
    }

    .status-badge:hover {
        transform: translateY(-1px);
        box-shadow: 0 3px 10px rgba(25, 135, 84, 0.4);
    }

    /* Adjusted features-grid for explicit column control */
    .features-grid {
        display: block; /* Removed grid display here, using Streamlit columns */
        margin: 1rem 0;
    }

    .feature-box {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 100, 0, 0.08);
        border: 1px solid rgba(25, 135, 84, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .feature-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, #198754, #20c997);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }

    .feature-box:hover::before {
        transform: scaleX(1);
    }

    .feature-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(25, 135, 84, 0.12);
        border-color: rgba(25, 135, 84, 0.3);
    }

    .feature-content {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .feature-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .feature-icon {
        font-size: 1.8rem;
        background: linear-gradient(135deg, #198754, #20c997);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        flex-shrink: 0;
    }

    .feature-title {
        font-size: 1.1rem;
        color: #0f5132;
        margin: 0;
        font-weight: 600;
        line-height: 1.2;
        flex-grow: 1;
    }

    .feature-desc {
        font-size: 0.85rem;
        color: #6c757d;
        line-height: 1.4;
        flex-grow: 1;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        margin-bottom: 0.75rem;
    }

    .feature-meta {
        display: flex;
        gap: 0.4rem;
        flex-wrap: wrap;
        align-items: center;
        justify-content: flex-start;
        margin-bottom: 0.75rem;
        overflow-x: auto;
        overflow-y: hidden;
        white-space: nowrap;
        scrollbar-width: none;
        -ms-overflow-style: none;
    }

    .feature-meta::-webkit-scrollbar {
        display: none;
    }

    .meta-tag {
        background: #f8fff8;
        color: #0f5132;
        padding: 2px 6px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 500;
        border: 1px solid #d1e7dd;
        white-space: nowrap;
        line-height: 1;
    }

    .feature-button {
        margin-top: auto;
    }

    .stButton > button {
        background: linear-gradient(135deg, #198754, #20c997) !important;
        color: white !important;
        border: none !important;
        padding: 8px 18px !important;
        font-size: 0.85rem !important;
        border-radius: 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(25, 135, 84, 0.3) !important;
        width: 100% !important;
        position: relative !important;
        overflow: hidden !important;
        height: 36px !important;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(25, 135, 84, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    .stats-container {
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1.25rem 0;
        box-shadow: 0 4px 15px rgba(0, 100, 0, 0.08);
        border: 1px solid rgba(25, 135, 84, 0.1);
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 1.25rem;
        text-align: center;
    }

    .stat-item {
        padding: 0.5rem;
    }

    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #198754;
        display: block;
        margin-bottom: 0.25rem;
    }

    .stat-label {
        font-size: 0.75rem;
        color: #6c757d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .footer-container {
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 1.5rem;
        box-shadow: 0 3px 12px rgba(0, 100, 0, 0.08);
        border-top: 2px solid #198754;
    }

    .footer-links {
        display: flex;
        justify-content: center;
        gap: 1.25rem;
        margin-bottom: 0.75rem;
        flex-wrap: wrap;
    }

    .footer-link {
        color: #198754;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.85rem;
        transition: color 0.3s ease;
    }

    .footer-link:hover {
        color: #0f5132;
        text-decoration: underline;
    }

    @media (max-width: 768px) {
        .header-title {
            font-size: 1.8rem;
        }

        /* Adjusted features-grid for explicit column control */
        .features-grid {
             /* Resetting this to ensure streamlit columns take precedence */
        }

        .feature-box {
            padding: 1rem;
            min-height: 130px;
        }

        .feature-header {
            gap: 0.5rem;
        }

        .feature-icon {
            font-size: 1.6rem;
        }

        .feature-title {
            font-size: 1rem;
        }

        .feature-desc {
            font-size: 0.8rem;
        }

        .stats-grid {
            grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
            gap: 1rem;
        }

        .status-badges {
            flex-direction: row;
            justify-content: center;
            gap: 0.4rem;
        }

        .meta-tag {
            font-size: 0.65rem;
            padding: 1px 5px;
        }

        .feature-meta {
            gap: 0.3rem;
            flex-wrap: wrap;
            white-space: normal;
            overflow-x: hidden;
        }
    }

    @media (max-width: 480px) {
        .feature-meta {
            overflow-x: auto;
            overflow-y: hidden;
            white-space: nowrap;
            scrollbar-width: none;
            -ms-overflow-style: none;
        }

        .feature-meta::-webkit-scrollbar {
            display: none;
        }

        .meta-tag {
            display: inline-block;
        }
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stDecoration"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.markdown('''
<div class="main-header">
    <h1 class="header-title">🏥 AI Health Kiosk</h1>
    <p class="header-subtitle">Mediview Hospital | Unified Patient Care Interface</p>
    <div class="status-badges">
        <span class="status-badge">🔬 AI-Powered</span>
        <span class="status-badge">🏥 ABDM Compliant</span>
        <span class="status-badge">🔒 HIPAA Secure</span>
        <span class="status-badge">📱 Multi-Platform</span>
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('''
<div class="stats-container">
    <div class="stats-grid">
        <div class="stat-item">
            <span class="stat-number">7</span>
            <div class="stat-label">Healthcare Modules</div>
        </div>
        <div class="stat-item">
            <span class="stat-number">24/7</span>
            <div class="stat-label">Availability</div>
        </div>
        <div class="stat-item">
            <span class="stat-number">100%</span>
            <div class="stat-label">Secure</div>
        </div>
        <div class="stat-item">
            <span class="stat-number">AI</span>
            <div class="stat-label">Powered</div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

def feature_card(title, desc, button_label, path, icon="🔧", tags=None, parent_col=None):
    """
    Renders a feature card with title, description, icon, tags, and a button.
    It now accepts a 'parent_col' to render within a specific column.
    """
    with parent_col: # Use the provided column directly
        st.markdown(f'''
        <div class="feature-box">
            <div class="feature-content">
                <div class="feature-header">
                    <span class="feature-icon">{icon}</span>
                    <h3 class="feature-title">{title}</h3>
                </div>
                <div class="feature-desc">{desc}</div>
                <div class="feature-meta">
                    {''.join(f'<span class="meta-tag">{tag}</span>' for tag in tags) if tags else ''}
                </div>
            </div>
            <div class="feature-button">
            ''', unsafe_allow_html=True) # Close the feature-button div after the button

        # Place the Streamlit button here. Its return value is True if clicked.
        if st.button(button_label, key=f"btn_{title}"):
            st.switch_page(path)

        st.markdown('''
            </div>
        </div>
        ''', unsafe_allow_html=True) # Close the feature-box and feature-button divs

pages = [
    {
        "title": "Health Assessment",
        "desc": "Comprehensive vital signs recording, symptom documentation, and secure ABHA-linked data submission with real-time validation.",
        "button_label": "🚀 Launch Assessment",
        "path": r"pages\Health_Assessment.py",
        "icon": "🩺",
        "tags": ["ABHA Linked", "Real-time", "Secure"]
    },
    {
        "title": "Electronic Health Records",
        "desc": "Access complete patient history including clinical visits, laboratory results, vital trends, and medication records.",
        "button_label": "📋 View Records",
        "path": r"pages\EHR_Viewer.py",
        "icon": "📁",
        "tags": ["Patient History", "Lab Results", "Medications"]
    },
    {
        "title": "Breast Cancer Diagnostics",
        "desc": "Advanced AI-powered image analysis with confidence scoring, Grad-CAM visualization, and comprehensive diagnostic reporting.",
        "button_label": "🔬 Start Diagnosis",
        "path": r"pages\Breast_Cancer.py",
        "icon": "🎗️",
        "tags": ["AI Analysis", "Grad-CAM", "Medical Imaging"]
    },
    {
        "title": "Teleconsultation Platform",
        "desc": "Schedule and conduct secure video consultations with verified healthcare professionals and specialists.",
        "button_label": "📞 Book Consultation",
        "path": r"pages\Teleconsultation.py",
        "icon": "📞",
        "tags": ["Video Calls", "Verified Doctors", "Scheduling"]
    },
    {
        "title": "Medication Tracker",
        "desc": "Monitor medication schedules, track adherence, set automated reminders, and manage prescription refills with dosage tracking.",
        "button_label": "💊 Track Medications",
        "path": r"pages\Medication_Tracker.py",
        "icon": "💊",
        "tags": ["Reminders", "Adherence", "Prescriptions"]
    },
    {
        "title": "Vaccination Management",
        "desc": "Track immunization status, monitor vaccination schedules, and receive automated reminders for pending vaccines.",
        "button_label": "💉 Track Vaccines",
        "path": r"pages\Vaccination_Tracking.py",
        "icon": "💉",
        "tags": ["Immunization", "Reminders", "Schedule"]
    },
    {
        "title": "Health Risk Calculator",
        "desc": "Assess personalized risk factors for diabetes, hypertension, cardiovascular disease, and other chronic conditions.",
        "button_label": "📊 Calculate Risk",
        "path": r"pages\Health_Risk_Calculator.py",
        "icon": "📊",
        "tags": ["Risk Assessment", "Diabetes", "Hypertension"]
    }
]

# Display cards in a 2x2 grid structure
st.markdown('<div class="features-grid">', unsafe_allow_html=True) # Keep this div for general styling/margin
for i in range(0, len(pages), 2): # Iterate by 2 to create rows of 2
    col1, col2 = st.columns(2, gap="medium") # Create two columns for each row
    
    # Render the first card in the first column
    feature_card(**pages[i], parent_col=col1)
    
    # Render the second card in the second column, if it exists
    if i + 1 < len(pages):
        feature_card(**pages[i+1], parent_col=col2)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('''
<div class="footer-container">
    <div class="footer-links">
        <a href="#" class="footer-link">🏥 About Hospital</a>
        <a href="#" class="footer-link">📞 Emergency Services</a>
        <a href="#" class="footer-link">🔒 Privacy Policy</a>
        <a href="#" class="footer-link">📋 Terms of Service</a>
        <a href="#" class="footer-link">💬 Support Center</a>
    </div>
    <p style="color: #6c757d; margin: 0.75rem 0;"><strong>© 2024 Mediview Hospital</strong> | AI-Powered Healthcare Platform</p>
    <p style="color: #6c757d; font-size: 0.85rem;">🌐 Available 24/7 • 📱 Mobile Responsive • 🔬 Research Grade AI • 🛡️ HIPAA Compliant</p>
</div>
''', unsafe_allow_html=True)