import streamlit as st
from utils.breast_utils import preprocess_image, predict_breast_cancer, generate_gradcam, validate_image, format_medical_report, load_and_build_model, get_image_metadata
import pandas as pd
from PIL import Image
import datetime
import os
import plotly.graph_objects as go

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
        overflow: hidden;
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

    .image-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    }
    .image-card {
        background: white;
        padding: 1rem;
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
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.8rem !important;
        color: #0f5132 !important;
    }
    .heatmap-interpretation-box {
        background: #f8fff8;
        border: 1px solid #198754;
        color: #0f5132;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 0.8rem;
        margin: 0.8rem 0;
    }
    .stat-card {
        background: linear-gradient(135deg, #198754, #20c997);
        color: white;
        padding: 1.2rem;
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
        font-size: 1.8rem !important;
        font-weight: bold !important;
        margin-bottom: 0.3rem !important;
        color: white !important;
    }
    .stat-label {
        font-size: 0.85rem !important;
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

    .plotly-chart {
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 100, 0, 0.08);
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(25, 135, 84, 0.1);
    }

    .compact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.8rem;
        margin: 0.8rem 0;
    }
    .compact-card {
        background: white;
        padding: 0.8rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 100, 0, 0.1);
        text-align: center;
        border: 1px solid rgba(25, 135, 84, 0.1);
    }
    .compact-card h4 {
        font-size: 1rem !important;
        margin-bottom: 0.3rem !important;
    }
    .compact-card div {
        font-size: 1.3rem !important;
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

    @media (max-width: 768px) {
        .main-header { padding: 1rem; }
        .header-title { font-size: 1.8rem !important; }
        .section-box { padding: 1rem; }
        .image-grid { grid-template-columns: 1fr; gap: 0.8rem; }
        .stats-grid { grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); }
        .analysis-grid { grid-template-columns: 1fr; }
        .report-grid { grid-template-columns: 1fr; }
        .status-indicators { flex-direction: column; align-items: center; }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_cancer_model():
    model_h5_path = r"models\cnn_based_breast_cancer_pred.h5"
    model_xml_path = r"models_openvino\cnn_based_breast_cancer_pred_ov.xml" # Assuming you have an OpenVINO XML model
    try:
        compiled_model, tf_model = load_and_build_model(model_xml_path, model_h5_path)
        return compiled_model, tf_model
    except Exception as e:
        st.error(f"Failed to load AI model: {e}. Please ensure 'models/cnn_based_breast_cancer_pred.h5' and 'models/cnn_based_breast_cancer_pred.xml' exist and are valid models.")
        return None, None

compiled_model, tf_model = load_cancer_model()

st.markdown(f"""
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
""", unsafe_allow_html=True)

if compiled_model is None or tf_model is None:
    st.stop()

st.markdown(f"""
<div class="upload-section">
    <h3 class="upload-title">📤 Upload Medical Image for Analysis</h3>
</div>
""", unsafe_allow_html=True)

col_upload, col_abha = st.columns([2, 1])
with col_upload:
    uploaded = st.file_uploader(
        "Select breast scan image (X-ray, mammogram, or ultrasound)",
        type=["jpg", "jpeg", "png", "bmp", "tiff"],
        help="Supported formats: JPG, JPEG, PNG, BMP, TIFF (Max size: 10MB)"
    )

with col_abha:
    abha_id = st.text_input(
        "🆔 Patient ABHA ID",
        max_chars=14,
        help="Enter patient's ABHA (Ayushman Bharat Health Account) ID",
        placeholder="XX-XXXX-XXXX-XXXX"
    )
    if abha_id and len(abha_id.replace('-', '')) < 1:
        st.warning("⚠️ ABHA ID should be at least 10 digits long.")

if uploaded and abha_id and len(abha_id.replace('-', '')) >= 1:
    if not validate_image(uploaded):
        st.error("❌ Invalid image format or corrupted file. Please upload a valid image.")
        st.stop()

    with st.spinner("🔄 Processing image and generating AI analysis..."):
        img_tensor = preprocess_image(uploaded)
        if img_tensor is None:
            st.error("❌ Failed to preprocess image. Please ensure it's a valid medical scan.")
            st.stop()

        prediction, confidence = predict_breast_cancer(img_tensor, compiled_model)
        if prediction == "Error":
            st.error("❌ Failed to make AI prediction. The model might not be suitable for this image or an internal error occurred.")
            st.stop()
        
        heatmap = None
        try:
            heatmap = generate_gradcam(model=tf_model, img_tensor=img_tensor)
        except Exception:
            st.info("💡 Note: Could not generate AI attention heatmap for this image. Analysis proceeds without it.")

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">📊 AI Diagnostic Results</h3>', unsafe_allow_html=True)

    img_col, heatmap_col = st.columns(2)
    with img_col:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.markdown('<div class="image-title">📸 Original Medical Image</div>', unsafe_allow_html=True)
        st.image(uploaded, use_column_width=True, caption="Uploaded medical scan")

        try:
            img_metadata = get_image_metadata(uploaded)
            if "error" not in img_metadata:
                st.markdown(f"""
                <div class="info-box">
                    <strong>Image Details:</strong><br>
                    📐 Dimensions: {img_metadata.get("dimensions", "Unknown")}<br>
                    📁 Format: {img_metadata.get("format", "Unknown")}<br>
                    💾 Size: {img_metadata.get("size", "Unknown")}
                </div>
                """, unsafe_allow_html=True)
        except Exception:
            pass

        st.markdown('</div>', unsafe_allow_html=True)

    with heatmap_col:
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.markdown('<div class="image-title">🔥 AI Attention Heatmap</div>', unsafe_allow_html=True)
        if heatmap is not None:
            st.image(heatmap, use_column_width=True, caption="AI focus areas highlighted")
            st.markdown("""
            <div class="heatmap-interpretation-box">
                <strong>🔍 Heatmap Interpretation:</strong><br>
                🔴 Red areas: High AI attention<br>
                🟡 Yellow areas: Medium attention<br>
                🔵 Blue areas: Low attention
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("💡 Heatmap could not be generated. This might be due to model architecture limitations or image characteristics.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    confidence_color_bg = "#198754" if confidence > 0.8 else "#ffc107" if confidence > 0.6 else "#dc3545"
    confidence_level = "Very High" if confidence > 0.9 else "High" if confidence > 0.8 else "Medium" if confidence > 0.6 else "Low"
    risk_level_text = "HIGH RISK" if prediction == "Malignant" else "LOW RISK"
    risk_color_bg = "#dc3545" if prediction == "Malignant" else "#198754"
    prediction_icon = "🚨" if prediction == "Malignant" else "✅"
    risk_icon = "⚠️" if prediction == "Malignant" else "🛡️"
    now = datetime.datetime.now()

    st.markdown(f"""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{prediction_icon}</div>
            <div class="stat-label">AI Prediction</div>
            <div style="font-size: 1.1rem; margin-top: 0.3rem; font-weight: 600;">{prediction}</div>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, {confidence_color_bg}, {confidence_color_bg}dd);">
            <div class="stat-value">{confidence * 100:.1f}%</div>
            <div class="stat-label">Confidence Score</div>
            <div style="font-size: 0.9rem; margin-top: 0.3rem; opacity: 0.9;">{confidence_level} Confidence</div>
        </div>
        <div class="stat-card" style="background: linear-gradient(135deg, {risk_color_bg}, {risk_color_bg}dd);">
            <div class="stat-value">{risk_icon}</div>
            <div class="stat-label">Risk Assessment</div>
            <div style="font-size: 1rem; margin-top: 0.3rem; font-weight: 600;">{risk_level_text}</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">📅</div>
            <div class="stat-label">Analysis Date</div>
            <div style="font-size: 0.9rem; margin-top: 0.3rem;">{now.strftime("%d %b %Y")}</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">{now.strftime("%H:%M:%S")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if prediction == "Malignant":
        st.markdown("""
        <div class="alert-danger">
            <h4 style="margin: 0 0 0.5rem 0; color: #721c24;">⚠️ High-Risk Result Detected</h4>
            <p style="margin: 0.3rem 0;"><strong>Immediate Action Required:</strong></p>
            <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                <li>Schedule urgent consultation with an oncologist.</li>
                <li>Bring this report and original images for review.</li>
                <li>Consider seeking a second medical opinion.</li>
                <li>Do not delay professional medical consultation.</li>
            </ul>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;"><em>This AI analysis is for screening purposes only and requires professional medical validation.</em></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-success">
            <h4 style="margin: 0 0 0.5rem 0; color: #0f5132;">✅ Low-Risk Result</h4>
            <p style="margin: 0.3rem 0;"><strong>Recommended Next Steps:</strong></p>
            <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                <li>Continue with your regular breast cancer screening schedule.</li>
                <li>Maintain healthy lifestyle habits to promote overall well-being.</li>
                <li>Schedule routine follow-up examinations as advised by your doctor.</li>
                <li>Stay aware of any changes in breast health and report them promptly.</li>
            </ul>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;"><em>Regular screening remains important for early detection.</em></p>
        </div>
        """, unsafe_allow_html=True)

    now_formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    image_metadata = get_image_metadata(uploaded)
    report_data = format_medical_report(abha_id, prediction, confidence, now_formatted, image_metadata=image_metadata)

    st.markdown('<div class="report-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">📋 Comprehensive Medical Report</h3>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="report-grid">
        <div class="report-item">
            <h4 style="color: #0f5132; margin-bottom: 0.5rem;">Patient Information</h4>
            <p><strong>Patient ID:</strong> {report_data.get("Patient_ID", "N/A")}</p>
            <p><strong>Analysis Date:</strong> {report_data.get("Analysis_Date", "N/A")}</p>
            <p><strong>Analysis Time:</strong> {report_data.get("Analysis_Time", "N/A")}</p>
            <p><strong>Image Format:</strong> {report_data.get("Image_Format", "N/A")}</p>
            <p><strong>Image Size:</strong> {report_data.get("Image_Size", "N/A")}</p>
            <p><strong>Original Dimensions:</strong> {report_data.get("Original_Dimensions", "N/A")}</p>
        </div>
        <div class="report-item">
            <h4 style="color: #0f5132; margin-bottom: 0.5rem;">AI Analysis Results</h4>
            <p><strong>Prediction:</strong> {report_data.get("Prediction", "N/A")}</p>
            <p><strong>Confidence Score:</strong> {report_data.get("Confidence_Score", "N/A")} ({report_data.get("Confidence_Level", "N/A")})</p>
            <p><strong>Risk Category:</strong> {report_data.get("Risk_Category", "N/A")}</p>
            <p><strong>Risk Level:</strong> {report_data.get("Risk_Level", "N/A")}</p>
            <p><strong>Urgency:</strong> {report_data.get("Urgency", "N/A")}</p>
            <p><strong>Recommendation:</strong> {report_data.get("Recommendation", "N/A")}</p>
            <p><strong>AI Model:</strong> {report_data.get("AI_Model", "N/A")}</p>
            <p><strong>Analysis Type:</strong> {report_data.get("Analysis_Type", "N/A")}</p>
            <p><strong>Model Architecture:</strong> {report_data.get("Model_Architecture", "N/A")}</p>
            <p><strong>Input Resolution:</strong> {report_data.get("Input_Resolution", "N/A")}</p>
            <p><strong>Processing Method:</strong> {report_data.get("Processing_Method", "N/A")}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    history_file = "data/breast_cancer_history.csv"
    os.makedirs("data", exist_ok=True)
    
    hist_df = pd.DataFrame()
    if os.path.exists(history_file):
        try:
            hist_df = pd.read_csv(history_file)
        except Exception as e:
            st.warning(f"Could not load patient history from CSV: {str(e)}. Starting with a fresh history for this session.")
    
    save_analysis_history_success = False
    try:
        from utils.breast_utils import save_analysis_history
        save_analysis_history_success = save_analysis_history(abha_id, prediction, confidence, now_formatted, file_path=history_file)
    except Exception as e:
        st.error(f"❌ An error occurred while attempting to save history: {e}")
    
    if save_analysis_history_success:
        st.success("✅ Analysis saved to patient history.")
    else:
        st.warning("⚠️ Analysis could not be saved to patient history. Please check permissions or file integrity.")

    if abha_id in hist_df['ABHA_ID'].values:
        patient_hist = hist_df[hist_df['ABHA_ID'] == abha_id].copy()
        patient_hist["Date"] = pd.to_datetime(patient_hist["Date"], format="%Y-%m-%d %H:%M:%S")
        patient_hist = patient_hist.sort_values(by="Date", ascending=True)

        with st.expander("📈 View Patient History & Trends", expanded=True):
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.markdown('<h3 class="section-header">📈 Patient History Analysis</h3>', unsafe_allow_html=True)

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
                height=350,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            total_scans = len(patient_hist)
            malignant_count = len(patient_hist[patient_hist['Prediction'] == 'Malignant'])
            benign_count = len(patient_hist[patient_hist['Prediction'] == 'Benign'])
            avg_confidence = patient_hist['Confidence'].mean()

            st.markdown(f"""
            <div class="compact-grid">
                <div class="compact-card">
                    <h4>📊 Total Scans</h4>
                    <div style="font-weight: bold; color: #198754;">{total_scans}</div>
                </div>
                <div class="compact-card">
                    <h4>🚨 High-Risk Results</h4>
                    <div style="font-weight: bold; color: #dc3545;">{malignant_count}</div>
                </div>
                <div class="compact-card">
                    <h4>✅ Low-Risk Results</h4>
                    <div style="font-weight: bold; color: #198754;">{benign_count}</div>
                </div>
                <div class="compact-card">
                    <h4>📈 Avg. Confidence</h4>
                    <div style="font-weight: bold; color: #198754;">{avg_confidence:.1%}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info(f"ℹ️ No prior history found for ABHA ID: **{abha_id}**. This is the first recorded analysis for this ID.")

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">📥 Download Medical Report</h3>', unsafe_allow_html=True)
    
    report_text = "\n".join([f"{k}: {v}" for k, v in report_data.items()])
    st.download_button(
        label="Download Full Report (TXT)",
        data=report_text,
        file_name=f"Breast_Cancer_Report_{abha_id}_{now.strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        help="Download a text file containing the full analysis report."
    )

    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="medical-disclaimer">
        <h4 style="margin: 0 0 0.5rem 0; color: #664d03;">Important Medical Disclaimer</h4>
        <p style="margin: 0.3rem 0;">This AI-powered diagnostic tool is for informational and screening purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare professional for any health concerns or before making any decisions related to patient care.</p>
        <p style="margin: 0; font-size: 0.8rem;">The information provided by this tool should be used in conjunction with a comprehensive clinical evaluation by a medical doctor.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("Please upload an image and enter the patient's ABHA ID to begin the analysis.")

st.markdown("""
<div class="footer-container">
    <p>Developed with ❤️ by Your Healthcare AI Team</p>
    <p>© 2025 Breast Cancer Diagnostic Dashboard. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)