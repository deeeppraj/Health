import streamlit as st
from utils.breast_utils import preprocess_image, predict_breast_cancer, generate_gradcam, validate_image, format_medical_report
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import datetime
import base64
import io
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Breast Cancer Diagnostic Dashboard", 
    layout="wide",
    initial_sidebar_state='collapsed',
    page_icon="🏥"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f8fff8 50%, #f0f9f0 100%);
        font-family: 'Inter', sans-serif;
    }
    html, body, .stApp {
        background-color: #ffffff;
        color: #1a202c;
        font-size: 15px;
        line-height: 1.5;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #0f5132 !important;
        font-weight: 600 !important;
        line-height: 1.2 !important;
        margin: 0.5rem 0 !important;
    }
    p, div, span, label, li {
        color: #2d3748 !important;
        font-weight: 400 !important;
        margin: 0.3rem 0 !important;
    }
    .main-header {
        background: linear-gradient(135deg, #ffffff 0%, #f8fff8 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 100, 0, 0.1);
        border: 1px solid rgba(25, 135, 84, 0.1);
        position: relative;
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #198754, #20c997);
        border-radius: 15px 15px 0 0;
    }
    .header-title {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #0f5132 !important;
        margin-bottom: 0.3rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .subtitle {
        font-size: 1.1rem !important;
        color: #6c757d !important;
        font-weight: 400 !important;
        margin-top: 0.3rem !important;
    }
    .status-indicators {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    .status-indicator {
        background: linear-gradient(135deg, #198754, #20c997);
        color: white !important;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        box-shadow: 0 3px 10px rgba(25, 135, 84, 0.3);
        transition: transform 0.2s ease;
    }
    .status-indicator:hover {
        transform: translateY(-2px);
    }
    .section-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0, 100, 0, 0.1);
        border: 1px solid rgba(25, 135, 84, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        position: relative;
    }
    .section-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #198754, #20c997);
        border-radius: 15px 15px 0 0;
    }
    .section-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 100, 0, 0.15);
    }
    .section-header {
        color: #0f5132 !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #e8f5e8 !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .upload-section {
        background: linear-gradient(135deg, #f8fff8, #e8f5e8);
        padding: 2rem 1.5rem;
        border-radius: 15px;
        border: 2px dashed #198754;
        text-align: center;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .upload-section:hover {
        border-color: #0f5132;
        background: linear-gradient(135deg, #e8f5e8, #d1e7dd);
    }
    .upload-title {
        color: #0f5132 !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.8rem !important;
    }
    .stFileUploader > div {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 0.8rem !important;
        transition: all 0.3s ease !important;
    }
    .stFileUploader > div:hover {
        border-color: #198754 !important;
        box-shadow: 0 3px 10px rgba(25, 135, 84, 0.15) !important;
    }
    .stTextInput > div > div > input {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        color: #2d3748 !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #198754 !important;
        box-shadow: 0 0 0 3px rgba(25, 135, 84, 0.1) !important;
        outline: none !important;
    }
    .stTextInput > label {
        color: #0f5132 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    .image-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }
    .image-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 100, 0, 0.08);
        text-align: center;
        border: 1px solid rgba(25, 135, 84, 0.1);
        transition: all 0.3s ease;
    }
    .image-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(25, 135, 84, 0.15);
    }
    .image-title {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        color: #0f5132 !important;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #198754, #20c997);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(25, 135, 84, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    .stat-card:hover::before {
        left: 100%;
    }
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(25, 135, 84, 0.4);
    }
    .stat-value {
        font-size: 2rem !important;
        font-weight: bold !important;
        margin-bottom: 0.3rem !important;
        color: white !important;
    }
    .stat-label {
        font-size: 0.9rem !important;
        opacity: 0.9 !important;
        color: white !important;
        font-weight: 500 !important;
    }
    .alert-danger {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        border: 2px solid #dc3545;
        color: #721c24 !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(220, 53, 69, 0.2);
    }
    .alert-success {
        background: linear-gradient(135deg, #d1e7dd, #badbcc);
        border: 2px solid #198754;
        color: #0f5132 !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(25, 135, 84, 0.2);
    }
    .report-section {
        background: linear-gradient(135deg, #f8fff8, #e8f5e8);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 2px solid #198754;
        box-shadow: 0 4px 15px rgba(25, 135, 84, 0.15);
    }
    .report-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }
    .report-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #198754;
    }
    .stButton > button {
        background: linear-gradient(135deg, #198754, #20c997) !important;
        color: white !important;
        border: none !important;
        padding: 10px 25px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        border-radius: 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 3px 10px rgba(25, 135, 84, 0.3) !important;
        width: 100% !important;
        max-width: 250px !important;
        margin: 0 auto !important;
        display: block !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(25, 135, 84, 0.4) !important;
    }
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    .plotly-chart {
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 100, 0, 0.08);
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(25, 135, 84, 0.1);
    }
    .analysis-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    .medical-disclaimer {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border: 2px solid #ffc107;
        color: #664d03 !important;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 3px 10px rgba(255, 193, 7, 0.2);
    }
    .footer-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: #6c757d !important;
        margin-top: 2rem;
        box-shadow: 0 3px 10px rgba(0, 100, 0, 0.08);
        border-top: 3px solid #198754;
    }
    .stSpinner > div {
        border-top-color: #198754 !important;
    }
    .compact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 0.8rem;
        margin: 0.8rem 0;
    }
    .compact-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 100, 0, 0.1);
        text-align: center;
        border: 1px solid rgba(25, 135, 84, 0.1);
    }
    .info-box {
        background: #f8fff8;
        border: 1px solid #198754;
        color: #0f5132;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
        }
        .header-title {
            font-size: 1.8rem !important;
        }
        .section-box {
            padding: 1rem;
        }
        .image-grid {
            grid-template-columns: 1fr;
            gap: 0.8rem;
        }
        .stats-grid {
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        }
        .analysis-grid {
            grid-template-columns: 1fr;
        }
        .report-grid {
            grid-template-columns: 1fr;
        }
        .status-indicators {
            flex-direction: column;
            align-items: center;
        }
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stDecoration"] {display: none;}
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb {
        background: #198754;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #0f5132;
    }
</style>
""", unsafe_allow_html=True)

from utils.breast_utils import load_and_build_model

@st.cache_resource
def load_cancer_model():
    model_path = r"models\cnn_based_breast_cancer_pred.h5"
    try:
        return load_and_build_model(model_path)
    except:
        return None

model = load_cancer_model()

st.markdown('''
<div class="main-header">
    <h1 class="header-title">🏥 Breast Cancer Diagnostic Dashboard</h1>
    <p class="subtitle">Advanced AI-powered medical imaging analysis for early detection</p>
    <div class="status-indicators">
        <span class="status-indicator">🔬 AI-Powered Analysis</span>
        <span class="status-indicator">🏥 Medical Grade</span>
        <span class="status-indicator">🔒 HIPAA Compliant</span>
        <span class="status-indicator">⚡ Real-time Results</span>
    </div>
</div>
''', unsafe_allow_html=True)

if model is None:
    st.error("⚠️ Model could not be loaded. Please check the model path.")
    st.stop()

st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown('<h3 class="upload-title">📤 Upload Medical Image for Analysis</h3>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    uploaded = st.file_uploader(
        "Select breast scan image (X-ray, mammogram, or ultrasound)", 
        type=["jpg", "jpeg", "png", "bmp", "tiff"],
        help="Supported formats: JPG, JPEG, PNG, BMP, TIFF (Max size: 10MB)"
    )
    
    if uploaded:
        try:
            if validate_image(uploaded):
                st.success("✅ Image uploaded successfully and validated")
            else:
                st.error("❌ Invalid image format")
                st.stop()
        except:
            st.error("❌ Error validating image")
            st.stop()

with col2:
    abha_id = st.text_input(
        "🆔 Patient ABHA ID", 
        max_chars=14,
        help="Enter patient's ABHA (Ayushman Bharat Health Account) ID",
        placeholder="XX-XXXX-XXXX-XXXX"
    )
    
    if abha_id and len(abha_id) < 2:
        st.warning("⚠️ ABHA ID should be at least 10 characters long")

st.markdown('</div>', unsafe_allow_html=True)

if uploaded and abha_id:
    try:
        with st.spinner("🔄 Processing image and generating AI analysis..."):
            img_tensor = preprocess_image(uploaded)
            if img_tensor is None:
                st.error("❌ Failed to preprocess image")
                st.stop()
            
            prediction, confidence = predict_breast_cancer(img_tensor, model)
            
            if prediction == "Error":
                st.error("❌ Failed to make prediction")
                st.stop()
        
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-header">📊 AI Diagnostic Results</h3>', unsafe_allow_html=True)
        
        st.markdown('<div class="image-grid">', unsafe_allow_html=True)
        
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.markdown('<div class="image-title">📸 Original Medical Image</div>', unsafe_allow_html=True)
        st.image(uploaded, width=300, caption="Uploaded medical scan")
        
        try:
            img_info = Image.open(uploaded)
            st.markdown(f"""
            <div class="info-box">
                <strong>Image Details:</strong><br>
                📐 Dimensions: {img_info.width} × {img_info.height}<br>
                📁 Format: {img_info.format}<br>
                💾 Size: {uploaded.size / 1024:.1f} KB
            </div>
            """, unsafe_allow_html=True)
        except:
            pass
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.markdown('<div class="image-title">🔥 AI Attention Heatmap</div>', unsafe_allow_html=True)
        try:
            with st.spinner("Generating AI attention heatmap..."):
                heatmap = generate_gradcam(model=model, img_tensor=img_tensor)
            
            if heatmap is not None:
                st.image(heatmap, width=300, caption="AI focus areas highlighted")
                st.markdown("""
                <div class="info-box">
                    <strong>🔍 Heatmap Interpretation:</strong><br>
                    🔴 Red areas: High AI attention<br>
                    🟡 Yellow areas: Medium attention<br>
                    🔵 Blue areas: Low attention
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Could not generate attention heatmap")
        except:
            st.warning("Could not generate heatmap")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
        
        prediction_icon = "🚨" if prediction == "Malignant" else "✅"
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-value">{prediction_icon}</div>
            <div class="stat-label">AI Prediction</div>
            <div style="font-size: 1.1rem; margin-top: 0.3rem; font-weight: 600;">{prediction}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        confidence_color = "#198754" if confidence > 0.8 else "#ffc107" if confidence > 0.6 else "#dc3545"
        confidence_level = "Very High" if confidence > 0.9 else "High" if confidence > 0.8 else "Medium" if confidence > 0.6 else "Low"
        st.markdown(f'''
        <div class="stat-card" style="background: linear-gradient(135deg, {confidence_color}, {confidence_color}dd);">
            <div class="stat-value">{confidence * 100:.1f}%</div>
            <div class="stat-label">Confidence Score</div>
            <div style="font-size: 0.9rem; margin-top: 0.3rem; opacity: 0.9;">{confidence_level} Confidence</div>
        </div>
        ''', unsafe_allow_html=True)
        
        risk_level = "HIGH RISK" if prediction == "Malignant" else "LOW RISK"
        risk_color = "#dc3545" if prediction == "Malignant" else "#198754"
        risk_icon = "⚠️" if prediction == "Malignant" else "🛡️"
        st.markdown(f'''
        <div class="stat-card" style="background: linear-gradient(135deg, {risk_color}, {risk_color}dd);">
            <div class="stat-value">{risk_icon}</div>
            <div class="stat-label">Risk Assessment</div>
            <div style="font-size: 1rem; margin-top: 0.3rem; font-weight: 600;">{risk_level}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        now = datetime.datetime.now()
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-value">📅</div>
            <div class="stat-label">Analysis Date</div>
            <div style="font-size: 0.9rem; margin-top: 0.3rem;">{now.strftime("%d %b %Y")}</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">{now.strftime("%H:%M:%S")}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if prediction == "Malignant":
            st.markdown('''
            <div class="alert-danger">
                <h4 style="margin: 0 0 0.5rem 0; color: #721c24;">⚠️ High-Risk Result Detected</h4>
                <p style="margin: 0.3rem 0;"><strong>Immediate Action Required:</strong></p>
                <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                    <li>Schedule urgent consultation with an oncologist</li>
                    <li>Bring this report and original images</li>
                    <li>Consider getting a second opinion</li>
                    <li>Do not delay medical consultation</li>
                </ul>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;"><em>This AI analysis is for screening purposes only and requires professional medical validation.</em></p>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="alert-success">
                <h4 style="margin: 0 0 0.5rem 0; color: #0f5132;">✅ Low-Risk Result</h4>
                <p style="margin: 0.3rem 0;"><strong>Recommended Next Steps:</strong></p>
                <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                    <li>Continue regular screening schedule</li>
                    <li>Maintain healthy lifestyle habits</li>
                    <li>Schedule routine follow-up as advised</li>
                    <li>Stay aware of any changes</li>
                </ul>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;"><em>Regular screening remains important for early detection.</em></p>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        now_formatted = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            report_data = format_medical_report(abha_id, prediction, confidence, now_formatted)
        except:
            report_data = {
                'ABHA_ID': abha_id,
                'Prediction': prediction,
                'Confidence': confidence,
                'Confidence_Level': confidence_level,
                'Risk_Category': risk_level,
                'AI_Model': 'CNN v1.0',
                'Date': now_formatted
            }
        
        st.markdown(f'''
        <div class="report-section">
            <h3 style="color: #0f5132; margin-bottom: 1rem;">📋 Comprehensive Medical Report</h3>
            <div class="report-grid">
                <div class="report-item">
                    <h4 style="color: #0f5132; margin-bottom: 0.5rem;">Patient Information</h4>
                    <p><strong>Patient ID:</strong> {abha_id}</p>
                    <p><strong>Analysis Date:</strong> {now_formatted}</p>
                    <p><strong>Image Type:</strong> {uploaded.type}</p>
                    <p><strong>File Size:</strong> {uploaded.size / 1024:.1f} KB</p>
                </div>
                <div class="report-item">
                    <h4 style="color: #0f5132; margin-bottom: 0.5rem;">AI Analysis Results</h4>
                    <p><strong>Prediction:</strong> {prediction}</p>
                    <p><strong>Confidence:</strong> {confidence * 100:.1f}% ({confidence_level})</p>
                    <p><strong>Risk Category:</strong> {risk_level}</p>
                    <p><strong>Model Version:</strong> CNN v1.0</p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        history_file = "data/breast_cancer_history.csv"
        if os.path.exists(history_file):
            try:
                hist_df = pd.read_csv(history_file)
                if abha_id in hist_df['ABHA_ID'].values:
                    st.markdown('<div class="section-box">', unsafe_allow_html=True)
                    st.markdown('<h3 class="section-header">📈 Patient History Analysis</h3>', unsafe_allow_html=True)
                    
                    patient_hist = hist_df[hist_df['ABHA_ID'] == abha_id].copy()
                    patient_hist["Date"] = pd.to_datetime(patient_hist["Date"])
                    
                    st.markdown('<div class="analysis-grid">', unsafe_allow_html=True)
                    
                    st.markdown('<div class="plotly-chart">', unsafe_allow_html=True)
                    
                    fig = go.Figure()
                    
                    for prediction_type in patient_hist["Prediction"].unique():
                        subset = patient_hist[patient_hist["Prediction"] == prediction_type]
                        color = '#dc3545' if prediction_type == 'Malignant' else '#198754'
                        
                        fig.add_trace(go.Scatter(
                            x=subset["Date"],
                            y=subset["Confidence"],
                            mode='lines+markers',
                            name=f'{prediction_type} Results',
                            line=dict(color=color, width=3),
                            marker=dict(size=8, color=color),
                            hovertemplate='<b>%{fullData.name}</b><br>' +
                                        'Date: %{x}<br>' +
                                        'Confidence: %{y:.1%}<br>' +
                                        '<extra></extra>'
                        ))
                    
                    fig.update_layout(
                        title='Patient Confidence Score Trends Over Time',
                        xaxis_title='Analysis Date',
                        yaxis_title='Confidence Score',
                        yaxis=dict(tickformat='.0%', range=[0, 1]),
                        template='plotly_white',
                        height=400,
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Patient Statistics Summary
                    st.markdown('<div class="compact-grid">', unsafe_allow_html=True)
                    
                    total_scans = len(patient_hist)
                    malignant_count = len(patient_hist[patient_hist['Prediction'] == 'Malignant'])
                    benign_count = len(patient_hist[patient_hist['Prediction'] == 'Benign'])
                    avg_confidence = patient_hist['Confidence'].mean()
                    
                    st.markdown(f'''
                    <div class="compact-card">
                        <h4 style="color: #0f5132; margin-bottom: 0.5rem;">📊 Total Scans</h4>
                        <div style="font-size: 1.5rem; font-weight: bold; color: #198754;">{total_scans}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    st.markdown(f'''
                    <div class="compact-card">
                        <h4 style="color: #0f5132; margin-bottom: 0.5rem;">🚨 High-Risk Results</h4>
                        <div style="font-size: 1.5rem; font-weight: bold; color: #dc3545;">{malignant_count}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    st.markdown(f'''
                    <div class="compact-card">
                        <h4 style="color: #0f5132; margin-bottom: 0.5rem;">✅ Low-Risk Results</h4>
                        <div style="font-size: 1.5rem; font-weight: bold; color: #198754;">{benign_count}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    st.markdown(f'''
                    <div class="compact-card">
                        <h4 style="color: #0f5132; margin-bottom: 0.5rem;">📈 Avg. Confidence</h4>
                        <div style="font-size: 1.5rem; font-weight: bold; color: #198754;">{avg_confidence:.1%}</div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Could not load patient history: {str(e)}")
        
        # Save current analysis to history
        try:
            new_record = pd.DataFrame([report_data])
            
            if os.path.exists(history_file):
                existing_df = pd.read_csv(history_file)
                updated_df = pd.concat([existing_df, new_record], ignore_index=True)
            else:
                os.makedirs("data", exist_ok=True)
                updated_df = new_record
            
            updated_df.to_csv(history_file, index=False)
            st.success("✅ Analysis saved to patient history")
        except Exception as e:
            st.warning(f"Could not save to history: {str(e)}")
        
        # Download Report Section
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-header">📥 Download Medical Report</h3>', unsafe_allow_html=True)
        
        # Generate PDF-ready report content
        report_content = f"""
BREAST CANCER DIAGNOSTIC REPORT
================================

Patient Information:
- Patient ID: {abha_id}
- Analysis Date: {now_formatted}
- Image Type: {uploaded.type}
- File Size: {uploaded.size / 1024:.1f} KB

AI Analysis Results:
- Prediction: {prediction}
- Confidence Score: {confidence * 100:.1f}% ({confidence_level})
- Risk Category: {risk_level}
- AI Model: CNN v1.0

Clinical Recommendations:
{
"- Schedule urgent consultation with an oncologist" if prediction == "Malignant" 
else "- Continue regular screening schedule"
}
{
"- Bring this report and original images to consultation" if prediction == "Malignant"
else "- Maintain healthy lifestyle habits"
}
{
"- Consider getting a second opinion" if prediction == "Malignant"
else "- Schedule routine follow-up as advised"
}
{
"- Do not delay medical consultation" if prediction == "Malignant"
else "- Stay aware of any changes"
}

DISCLAIMER:
This AI analysis is for screening purposes only and requires professional medical validation.
This report should not be used as the sole basis for medical decisions.

Generated by: Breast Cancer Diagnostic Dashboard
Report ID: {abha_id}_{now.strftime('%Y%m%d_%H%M%S')}
        """
        
        # Create download button
        st.download_button(
            label="📄 Download Complete Report",
            data=report_content,
            file_name=f"breast_cancer_report_{abha_id}_{now.strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ An error occurred during analysis: {str(e)}")
        st.error("Please try uploading a different image or contact support.")

# Medical Disclaimer
st.markdown('''
<div class="medical-disclaimer">
    <h4 style="margin: 0 0 0.5rem 0; color: #664d03;">⚠️ Important Medical Disclaimer</h4>
    <p style="margin: 0.3rem 0; color: #664d03;"><strong>This AI diagnostic tool is intended for screening and educational purposes only.</strong></p>
    <p style="margin: 0.3rem 0; color: #664d03;">Results should not be used as the sole basis for medical decisions. Always consult with qualified healthcare professionals for proper diagnosis and treatment. This tool does not replace professional medical advice, diagnosis, or treatment.</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #664d03;"><em>For emergency medical situations, contact your local emergency services immediately.</em></p>
</div>
''', unsafe_allow_html=True)

# Footer
st.markdown('''
<div class="footer-container">
    <p style="margin: 0.3rem 0; color: #6c757d;">🏥 Breast Cancer Diagnostic Dashboard v1.0</p>
    <p style="margin: 0.3rem 0; color: #6c757d;">Powered by Advanced AI & Machine Learning | Built with Streamlit</p>
    <p style="margin: 0.3rem 0; color: #6c757d;">© 2024 Medical AI Solutions. All rights reserved.</p>
</div>
''', unsafe_allow_html=True)
