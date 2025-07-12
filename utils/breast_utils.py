import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import io
import streamlit as st
import datetime
import pandas as pd
from typing import Tuple, Optional, Dict, List
import os
from PIL import Image
import io

def validate_image(file) -> bool:
    try:
        image = Image.open(file)
        image.verify()
        file.seek(0)
        return True
    except Exception:
        return False


def load_and_build_model(h5_path: str, input_shape=(1, 64, 64, 3)) -> tf.keras.Model:
    try:
        model = load_model(h5_path)
        try:
            _ = model.inputs
        except (AttributeError, ValueError):
            dummy_input = tf.random.normal(input_shape)
            _ = model(dummy_input)
        return model
    except Exception as e:
        st.error(f"❌ Failed to load and build model: {str(e)}")
        return None

def preprocess_image(uploaded_file) -> Optional[np.ndarray]:
    try:
        if hasattr(uploaded_file, 'read'):
            image_bytes = uploaded_file.read()
            uploaded_file.seek(0)
            img = Image.open(io.BytesIO(image_bytes))
        else:
            img = Image.open(uploaded_file)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img = img.resize((64, 64), Image.Resampling.LANCZOS)
        img_array = np.array(img).astype(np.float32) / 255.0
        return np.expand_dims(img_array, axis=0)
    except Exception as e:
        st.error(f"Error preprocessing image: {str(e)}")
        return None

def predict_breast_cancer(img_tensor: np.ndarray, model) -> Tuple[str, float]:
    try:
        if img_tensor is None or model is None:
            return "Error", 0.0
        predictions = model.predict(img_tensor, verbose=0)
        pred_prob = float(predictions[0][0])
        temperature = 1.5
        calibrated_prob = 1 / (1 + np.exp(-np.log(pred_prob / (1 - pred_prob)) / temperature))
        pred_class = "Malignant" if calibrated_prob > 0.5 else "Benign"
        confidence = max(0.5, min(0.99, calibrated_prob if pred_class == "Malignant" else 1 - calibrated_prob))
        return pred_class, confidence
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        return "Error", 0.0

def find_conv_layers(model) -> List[str]:
    conv_layers = []
    for layer in model.layers:
        layer_type = type(layer).__name__
        if any(conv_type in layer_type for conv_type in ['Conv2D', 'Convolution2D', 'SeparableConv2D', 'DepthwiseConv2D']):
            conv_layers.append(layer.name)
    return conv_layers

def generate_gradcam(model, img_tensor, layer_name=None):
    try:
        if img_tensor is None or model is None:
            return None
        try:
            _ = model.inputs
        except ValueError:
            dummy_input = tf.convert_to_tensor(img_tensor, dtype=tf.float32)
            _ = model(dummy_input)
            st.info("✅ Model built successfully inside Grad-CAM.")

        conv_layers = find_conv_layers(model)
        if not conv_layers:
            st.warning("No convolutional layers found")
            return create_simple_heatmap(img_tensor)

        if layer_name is None:
            layer_name = conv_layers[-1]

        grad_model = tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[model.get_layer(layer_name).output, model.output]
        )

        if not isinstance(img_tensor, tf.Tensor):
            img_tensor = tf.convert_to_tensor(img_tensor, dtype=tf.float32)

        with tf.GradientTape() as tape:
            tape.watch(img_tensor)
            conv_outputs, predictions = grad_model(img_tensor)
            class_output = predictions[:, 0]

        grads = tape.gradient(class_output, conv_outputs)
        if grads is None:
            return create_simple_heatmap(img_tensor)

        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
        heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
        heatmap = tf.maximum(heatmap, 0)
        if tf.reduce_max(heatmap) > 0:
            heatmap /= tf.reduce_max(heatmap)
        heatmap = heatmap.numpy()
        heatmap = cv2.resize(heatmap, (64, 64)) 
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        original_img = np.uint8(255 * img_tensor[0])
        original_img = cv2.resize(original_img, (64, 64))
        return cv2.addWeighted(original_img, 0.6, heatmap, 0.4, 0)
    except Exception as e:
        st.warning(f"Could not generate Grad-CAM: {str(e)}")
        return create_simple_heatmap(img_tensor)

def create_simple_heatmap(img_tensor: np.ndarray) -> np.ndarray:
    try:
        img = img_tensor.numpy()[0] if isinstance(img_tensor, tf.Tensor) else img_tensor[0]
        gray = cv2.cvtColor(np.uint8(255 * img), cv2.COLOR_RGB2GRAY) if len(img.shape) == 3 else np.uint8(255 * img)
        blurred = cv2.GaussianBlur(gray, (15, 15), 0)
        return cv2.applyColorMap(blurred, cv2.COLORMAP_JET)
    except Exception as e:
        st.error(f"Error creating simple heatmap: {str(e)}")
        return np.zeros((64, 64, 3), dtype=np.uint8)

def format_medical_report(abha_id: str, prediction: str, confidence: float, timestamp: str,
                          image_metadata: Optional[Dict] = None) -> Dict:
    risk_assessment = get_risk_assessment(prediction, confidence)
    report = {
        "Patient_ID": abha_id,
        "Analysis_Date": timestamp,
        "Analysis_Time": datetime.datetime.now().strftime("%H:%M:%S"),
        "Prediction": prediction,
        "Confidence_Score": f"{confidence * 100:.1f}%",
        "Confidence_Level": get_prediction_confidence_level(confidence),
        "Risk_Category": "High Risk" if prediction == "Malignant" else "Low Risk",
        "Risk_Level": risk_assessment["risk_level"],
        "Urgency": risk_assessment["urgency"],
        "Recommendation": risk_assessment["recommended_action"],
        "AI_Model": "CNN-v1.0",
        "Analysis_Type": "Breast Cancer Screening",
        "Model_Architecture": "Convolutional Neural Network",
        "Input_Resolution": "64x64 pixels",
        "Processing_Method": "Deep Learning Classification"
    }
    if image_metadata:
        report.update({
            "Image_Format": image_metadata.get("format", "Unknown"),
            "Image_Size": image_metadata.get("size", "Unknown"),
            "Original_Dimensions": image_metadata.get("dimensions", "Unknown")
        })
    return report

def get_prediction_confidence_level(confidence: float) -> str:
    if confidence >= 0.95:
        return "Very High"
    elif confidence >= 0.85:
        return "High"
    elif confidence >= 0.75:
        return "Medium-High"
    elif confidence >= 0.65:
        return "Medium"
    elif confidence >= 0.55:
        return "Low-Medium"
    else:
        return "Low"

def get_risk_assessment(prediction: str, confidence: float) -> Dict[str, str]:
    if prediction == "Malignant":
        if confidence >= 0.9:
            return {"risk_level": "CRITICAL", "urgency": "IMMEDIATE", "recommended_action": "Seek emergency medical consultation within 24 hours"}
        elif confidence >= 0.8:
            return {"risk_level": "HIGH", "urgency": "URGENT", "recommended_action": "Schedule oncologist consultation within 48 hours"}
        elif confidence >= 0.7:
            return {"risk_level": "MODERATE-HIGH", "urgency": "PRIORITY", "recommended_action": "Consult healthcare provider within 1 week"}
        else:
            return {"risk_level": "MODERATE", "urgency": "ROUTINE", "recommended_action": "Discuss with primary care physician"}
    else:
        if confidence >= 0.9:
            return {"risk_level": "VERY LOW", "urgency": "ROUTINE", "recommended_action": "Continue regular screening schedule"}
        elif confidence >= 0.8:
            return {"risk_level": "LOW", "urgency": "ROUTINE", "recommended_action": "Maintain regular check-ups"}
        else:
            return {"risk_level": "LOW-MODERATE", "urgency": "FOLLOW-UP", "recommended_action": "Consider additional imaging or follow-up"}

def save_analysis_history(abha_id: str, prediction: str, confidence: float,
                          timestamp: str, file_path: str = "data/breast_cancer_history.csv") -> bool:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        new_record = {
            "ABHA_ID": abha_id,
            "Date": timestamp,
            "Prediction": prediction,
            "Confidence": confidence,
            "Risk_Level": get_risk_assessment(prediction, confidence)["risk_level"]
        }
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
        else:
            df = pd.DataFrame([new_record])
        df.to_csv(file_path, index=False)
        return True
    except Exception as e:
        st.warning(f"Could not save analysis history: {str(e)}")
        return False

def get_image_metadata(uploaded_file) -> Dict:
    try:
        img = Image.open(uploaded_file)
        metadata = {
            "format": img.format,
            "mode": img.mode,
            "size": f"{uploaded_file.size / 1024:.1f} KB",
            "dimensions": f"{img.width} × {img.height}",
            "has_transparency": img.mode in ('RGBA', 'LA') or 'transparency' in img.info
        }
        if hasattr(img, '_getexif') and img._getexif():
            metadata["has_exif"] = True
        else:
            metadata["has_exif"] = False
        uploaded_file.seek(0)
        return metadata
    except Exception as e:
        return {"error": str(e)}
