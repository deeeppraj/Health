# 🏥 AI-Powered Healthcare Kiosk

An intelligent, modular, and NDHM-compliant healthcare kiosk designed to bridge the urban-rural health gap in India. This system integrates deep learning diagnostics, electronic health records (EHR), teleconsultation, and multilingual voice assistance—all built on a secure Intel-based stack.

---
## 📄 Technical Report

📘 **[Comprehensive Technical Report on the AI-Powered Healthcare Kiosk](./ITR%20report%20INTEL%20Final.pdf)**

Authored by *Deepraj Bhattacharjee*, this report details the problem statement, system architecture, CNN model performance, deployment strategy, and go-to-market blueprint.  
Includes:

## 🚀 Key Features

- **Breast Cancer Detection**: CNN-based histopathology image classification with Grad-CAM explainability
- **Vitals & Symptom Capture**: Integrated digital health questionnaire with ABHA identification
- **EHR Viewer**: Visualizes patient visit history, lab results, medications, and vitals
- **Teleconsultation**: Real-time booking and video calls with verified doctors (eSanjeevani-ready)
- **Medication & Vaccination Tracker**: ABHA-linked dashboards with dose/frequency history
- **Multilingual Voice Assistant**: Hindi-English speech interface for better accessibility

---

## 🧠 AI Model Highlights

- **Model**: Convolutional Neural Network (CNN)
- **Dataset**: Breast Histopathology Images (50x50/64x64 image patches)
- **Accuracy**: 86.66% (train), 86.57% (validation)
- **Inference Engine**: TensorFlow & OpenVINO
- **Explainability**: Grad-CAM heatmaps for transparent decision support

---

## 🏗️ Project Structure

```bash
📁 app.py                # Main launcher (Streamlit)
📁 pages/                # Modular healthcare features (EHR, Assessment, AI Diagnostics, etc.)
📁 utils/                # Helper functions for preprocessing, model loading, encryption
📁 models/               # Pretrained and optimized model files (.h5, .xml)
📁 data/                 # Synthetic, raw, and processed healthcare datasets
📁 notebooks/            # Model training, EDA, performance evaluation
````

---

## 🖥️ Tech Stack

* **Frontend**: Streamlit + Custom CSS
* **AI/ML**: TensorFlow, OpenVINO, Keras, Grad-CAM
* **Voice AI**: Google Speech API + Helsinki-NLP + gTTS
* **Standards**: ABHA/NDHM Compliant, HIPAA Secure
* **Deployment**: Edge-ready, Cloud-compatible

---

## 📦 Installation (Local Setup)

```bash
git clone https://github.com/your-username/ai-health-kiosk.git
cd ai-health-kiosk
pip install -r requirements.txt
streamlit run app.py
```

> ⚠️ Note: Requires access to ABHA sandbox and pretrained CNN models (provided in `/models`)

---

## 📍 Use Cases

* Rural PHCs and HWCs
* Mobile health vans
* Urban outpatient clinics
* NGO-led screening camps
* Corporate health wellness centers

---

## 🤝 Collaborate

We're open to collaborations on:

* Public health pilots
* Model expansion (e.g. cervical, skin cancer)
* Regulatory validation
* System integrations

📧 Contact: [work.deepraj@gmail.com](mailto:work.deepraj@gmail.com)

---

## 📜 License

MIT License — feel free to use and adapt with attribution.

```

