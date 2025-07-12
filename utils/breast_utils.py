# utils/breast_utils.py

import tensorflow as tf
from PIL import Image
import numpy as np
import io
import pandas as pd
import os
from openvino.runtime import Core
import datetime # Required for format_medical_report
import matplotlib.pyplot as plt # Required for generate_gradcam's colormap

# Define a consistent target size for images
# IMPORTANT: This MUST match the input size your *trained model* expects.
# Based on your previous conversion error, your model expects 64x64 images.
TARGET_SIZE = (64, 64)
INPUT_SHAPE = (64, 64, 3) # (Height, Width, Channels) for a 3-channel (RGB) image

def load_and_build_model(openvino_xml_path, h5_path): # Changed parameter name for clarity
    """
    Loads an OpenVINO XML model and a Keras H5 model.
    The H5 model is specifically needed for Grad-CAM.
    """
    compiled_model = None
    tf_model = None
    
    try:
        # Load OpenVINO model
        core = Core()
        # OpenVINO automatically finds the .bin file if the .xml file is specified
        if not os.path.exists(openvino_xml_path):
            raise FileNotFoundError(f"OpenVINO XML model file not found: {openvino_xml_path}")
        
        ov_model = core.read_model(model=openvino_xml_path)
        
        # Check if the device is available, prioritize CPU or AUTO
        if "CPU" in core.available_devices:
            compiled_model = core.compile_model(model=ov_model, device_name="CPU")
        else:
            print("CPU device not available. Trying AUTO device for OpenVINO inference.")
            compiled_model = core.compile_model(model=ov_model, device_name="AUTO")
        
        print(f"DEBUG: OpenVINO model loaded successfully from {openvino_xml_path}")

    except Exception as e:
        print(f"ERROR: Failed to load OpenVINO model: {e}")
        # Allow it to continue to try loading the TF model, but ensure compiled_model is None
        compiled_model = None 

    # Load TensorFlow/Keras model (for Grad-CAM)
    try:
        if not os.path.exists(h5_path):
            raise FileNotFoundError(f"Keras H5 model file not found: {h5_path}")
            
        tf_model = tf.keras.models.load_model(h5_path)
        print(f"DEBUG: Keras H5 model loaded successfully from {h5_path}")
    except Exception as e:
        print(f"ERROR: Failed to load Keras H5 model for Grad-CAM: {e}")
        tf_model = None # Ensure it's None if loading fails

    if compiled_model is None:
        raise Exception("Failed to load OpenVINO model. Cannot proceed with inference.")
    if tf_model is None:
        print("WARNING: Failed to load Keras H5 model. Grad-CAM functionality will not be available.")

    return compiled_model, tf_model


def preprocess_image(image_file):
    """
    Preprocesses an uploaded image for model prediction.
    Converts to RGB, resizes, and normalizes pixel values.
    """
    try:
        # Debug 1: Check if image_file is valid
        print(f"DEBUG: Preprocessing started for {image_file.name if hasattr(image_file, 'name') else 'unknown file'}")

        img = Image.open(image_file).convert('RGB')
        
        # Debug 2: Original image dimensions
        print(f"DEBUG: Original image dimensions: {img.size}, format: {img.format}")

        img = img.resize(TARGET_SIZE)
        
        # Debug 3: Resized image dimensions
        print(f"DEBUG: Resized image dimensions: {img.size}")

        img_array = np.array(img).astype(np.float32)
        
        # Debug 4: Image array shape and dtype before normalization
        print(f"DEBUG: img_array shape before norm: {img_array.shape}, dtype: {img_array.dtype}, min: {img_array.min()}, max: {img_array.max()}")

        # Normalize to [0, 1] range
        img_array = img_array / 255.0
        
        # Debug 5: Image array shape and dtype after normalization
        print(f"DEBUG: img_array shape after norm: {img_array.shape}, dtype: {img_array.dtype}, min: {img_array.min()}, max: {img_array.max()}")


        # Expand dimensions to create a batch of 1
        img_tensor = np.expand_dims(img_array, axis=0)
        
        # Debug 6: Final tensor shape
        print(f"DEBUG: Final img_tensor shape for model: {img_tensor.shape}")

        # Final check if the shape matches what the model expects
        # (1,) + INPUT_SHAPE ensures it matches (1, 64, 64, 3)
        expected_shape_for_model = (1,) + INPUT_SHAPE
        if img_tensor.shape != expected_shape_for_model:
            print(f"ERROR: Mismatch in final tensor shape. Expected {expected_shape_for_model}, got {img_tensor.shape}")
            # Consider raising an exception here if this is a critical mismatch
            return None # Or handle differently

        return img_tensor
    except Exception as e:
        print(f"ERROR during image preprocessing: {e}")
        return None

def predict_breast_cancer(img_tensor, compiled_model):
    """
    Makes a prediction using the loaded OpenVINO model.
    Returns the predicted class ("Benign" or "Malignant") and confidence.
    """
    try:
        # Debug 7: Check input tensor for prediction
        print(f"DEBUG: Entering predict_breast_cancer. Input tensor shape: {img_tensor.shape}, dtype: {img_tensor.dtype}")
        print(f"DEBUG: Input tensor min/max: {img_tensor.min()}/{img_tensor.max()}")

        # Get input and output nodes for OpenVINO inference
        input_layer = compiled_model.input(0)
        output_layer = compiled_model.output(0)

        # Debug 8: Check input layer properties from the compiled model
        # input_layer.shape and output_layer.shape might be ov.runtime.PartialShape objects
        print(f"DEBUG: OpenVINO Input Layer Name: {input_layer.any_name}, Shape: {input_layer.shape}, Dtype: {input_layer.get_element_type()}")
        print(f"DEBUG: OpenVINO Output Layer Name: {output_layer.any_name}, Shape: {output_layer.shape}, Dtype: {output_layer.get_element_type()}")

        # Run inference
        # Debug 9: Try-except for the actual inference call
        try:
            results = compiled_model([img_tensor])[output_layer]
            print(f"DEBUG: Inference results raw: {results}, shape: {results.shape}")
        except Exception as inference_e:
            print(f"ERROR: OpenVINO inference failed during model call: {inference_e}")
            return "Inference Error", 0.0


        # Assuming a binary classification where output is a single probability
        # Or a 2-element array for [benign_prob, malignant_prob]
        if results.shape[-1] == 1: # Single output neuron (sigmoid activation)
            malignant_prob = results[0][0]
            print(f"DEBUG: Model output is single value (sigmoid). Malignant Prob: {malignant_prob}")
        elif results.shape[-1] == 2: # Two output neurons (softmax activation)
            malignant_prob = results[0][1] # Assuming index 1 is malignant (adjust if 0 is malignant)
            print(f"DEBUG: Model output is two values (softmax). Benign Prob: {results[0][0]}, Malignant Prob: {results[0][1]}")
        else:
            raise ValueError(f"Model output shape {results.shape} is not as expected for binary classification (expected last dim to be 1 or 2).")

        if malignant_prob > 0.5:
            prediction = "Malignant"
            confidence = float(malignant_prob)
        else:
            prediction = "Benign"
            confidence = float(1 - malignant_prob) # Confidence in benign prediction
        
        print(f"DEBUG: Final Prediction: {prediction}, Confidence: {confidence:.4f}")
        return prediction, confidence
    except Exception as e:
        print(f"ERROR during prediction function execution: {e}")
        return "Error", 0.0

def generate_gradcam(model, img_tensor, layer_name=None):
    """
    Generates a Grad-CAM heatmap for the given image and Keras model.
    `model` must be a Keras model, not an OpenVINO compiled model.
    `layer_name` should be the name of the last convolutional layer in your model.
    """
    print(f"DEBUG: Entering generate_gradcam. Keras model input tensor shape: {img_tensor.shape}")

    # Inspect the Keras model's layers
    print("DEBUG: Keras Model Layers (for Grad-CAM target identification):")
    try:
        for i, layer in enumerate(model.layers):
            # --- MODIFIED HERE: Use .output_shape or .input_shape with getattr ---
            # Some layers (like Rescaling) might not directly have 'output_shape'
            output_shape_str = ""
            if hasattr(layer, 'output_shape'):
                output_shape_str = f"Output Shape={layer.output_shape}"
            elif hasattr(layer, 'input_shape'):
                output_shape_str = f"Input Shape={layer.input_shape}" # Fallback for layers like Rescaling
            else:
                output_shape_str = "Shape=N/A"

            print(f"  Layer {i}: Name='{layer.name}', Type={type(layer).__name__}, {output_shape_str}")
        print("DEBUG: Successfully iterated through model layers.")
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to iterate through Keras model layers (during shape print): {e}")
        return None # Exit if we can't even list layers

    # --- Setting the specific layer name based on your model architecture ---
    # The last Conv2D layer is likely 'conv2d_2' in your sequential model.
    # If you changed the names in your model definition, update this.
    target_conv_layer_name = 'conv2d_2'
    print(f"DEBUG: Hardcoding target Grad-CAM layer_name to: '{target_conv_layer_name}' based on model structure.")
    layer_name = target_conv_layer_name # Override layer_name if it was None or different


    if layer_name is None: # This block is now mostly for fallback or if hardcoding is removed
        # Attempt to find the last conv layer dynamically
        candidate_layers = [layer for layer in reversed(model.layers) 
                            if isinstance(layer, tf.keras.layers.Conv2D)]
        if candidate_layers:
            layer_name = candidate_layers[0].name
            print(f"DEBUG: Dynamically found last Conv2D layer for Grad-CAM: '{layer_name}' (fallback).")
        else:
            print("ERROR: No Conv2D layers found in the model for Grad-CAM. Cannot proceed.")
            raise ValueError("Could not find a convolutional layer for Grad-CAM. Please ensure your model has Conv2D layers.")
    else: # If layer_name was manually provided (or hardcoded, which it is now)
        # Verify the selected layer is indeed a Conv2D layer and exists
        try:
            target_layer_check = model.get_layer(layer_name)
            if not isinstance(target_layer_check, tf.keras.layers.Conv2D):
                print(f"WARNING: Specified layer_name '{layer_name}' is not a Conv2D layer. Grad-CAM might fail or produce unexpected results.")
        except ValueError:
             print(f"ERROR: Specified layer_name '{layer_name}' does not exist in the Keras model. Grad-CAM will fail.")
             return None


    # Ensure the layer exists
    try:
        target_layer = model.get_layer(layer_name)
    except ValueError:
        print(f"ERROR: Specified or dynamically found layer '{layer_name}' does not exist in the Keras model.")
        return None # Return None if layer isn't found
    
    # Build the Grad-CAM model
    try:
        grad_model = tf.keras.models.Model(
            [model.inputs], [target_layer.output, model.output]
        )
        print("DEBUG: Grad-CAM sub-model created successfully.")
    except Exception as e:
        print(f"ERROR: Failed to create Grad-CAM sub-model. Check 'layer_name' or model structure: {e}")
        return None

    with tf.GradientTape() as tape:
        # Watch the target convolutional layer's output
        tape.watch(target_layer.output)
        last_conv_layer_output, predictions = grad_model(img_tensor)
        
        # Debug: Predictions shape from Grad-CAM sub-model
        print(f"DEBUG: Grad-CAM sub-model predictions shape: {predictions.shape}, values: {predictions}")
        
        # Determine the predicted class index
        if predictions.shape[-1] == 1: # Sigmoid output for binary classification
            pred_index = 0 # Only one output neuron, always take its gradient
            class_channel = predictions[:, pred_index]
        elif predictions.shape[-1] == 2: # Softmax output for binary classification
            pred_index = tf.argmax(predictions[0]) # Get the index of the highest probability
            class_channel = predictions[:, pred_index]
        else:
            print(f"WARNING: Grad-CAM: Unexpected prediction shape {predictions.shape}. Defaulting to index 0.")
            pred_index = 0
            class_channel = predictions[:, pred_index]

        print(f"DEBUG: Grad-CAM: Selected predicted class index for gradients: {pred_index}")

    grads = tape.gradient(class_channel, last_conv_layer_output)
    
    # Check if gradients are None (critical failure)
    if grads is None:
        print(f"ERROR: Gradients are None for Grad-CAM. This is a critical issue.")
        print("Possible causes: layer_name is wrong, model is not differentiable, or input is problematic (e.g., all zeros).")
        return None

    # Check for NaN or Inf in gradients (less common but possible with bad training)
    if tf.reduce_any(tf.math.is_nan(grads)) or tf.reduce_any(tf.math.is_inf(grads)):
        print("ERROR: NaN or Inf values detected in gradients. Grad-CAM will likely fail or be corrupted.")
        return None

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Debug: Pooled gradients
    print(f"DEBUG: Pooled gradients shape: {pooled_grads.shape}, values: {pooled_grads.numpy()}")

    last_conv_layer_output = last_conv_layer_output[0] # Remove batch dimension

    # Compute heatmap
    # Add a check for zero pooled_grads which would lead to an empty heatmap
    # Use a small epsilon to compare against zero to account for floating point inaccuracies
    if tf.reduce_max(tf.abs(pooled_grads)) < 1e-6: 
        print("WARNING: Pooled gradients are effectively zero. Grad-CAM heatmap will be empty/black. This can happen if the model is not learning well or the selected layer isn't discriminative for this input.")
        heatmap = tf.zeros_like(tf.squeeze(last_conv_layer_output))
    else:
        # Expand pooled_grads to match last_conv_layer_output's last dimension for dot product
        # Element-wise multiplication between each channel of the feature map
        # and the importance weight calculated for that channel.
        heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap) # Remove the last dimension if it's 1
    
    # Normalize heatmap to [0, 1]
    # Add a small epsilon to the denominator to prevent division by zero if max is 0
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-10) 
    heatmap = heatmap.numpy()

    # Debug: Heatmap min/max after normalization
    print(f"DEBUG: Heatmap min: {heatmap.min()}, max: {heatmap.max()}")

    # Overlay heatmap on original image
    # Denormalize original image to 0-255 for proper blending
    img = (img_tensor[0] * 255).astype(np.uint8) 
    
    # Ensure matplotlib.pyplot is imported
    cmap = plt.get_cmap('jet')
    # Apply the colormap to the heatmap, then convert to 0-255 RGB
    heatmap_colored = cmap(heatmap)[:, :, :3] # Get RGB from colormap, discard alpha
    heatmap_colored = (heatmap_colored * 255).astype(np.uint8)

    # Resize heatmap to original image size (which is TARGET_SIZE for processed images)
    # Ensure the array type is uint8 before creating PIL Image
    heatmap_pil = Image.fromarray(heatmap_colored).resize((img.shape[1], img.shape[0]))
    
    # Overlay heatmap with transparency
    alpha = 0.4
    overlay_img = Image.fromarray(img)
    overlay_heatmap = Image.blend(overlay_img.convert("RGBA"), heatmap_pil.convert("RGBA"), alpha=alpha)
    
    print("DEBUG: Grad-CAM heatmap generated successfully.")
    return overlay_heatmap

def validate_image(image_file):
    """
    Basic validation for uploaded image files.
    Checks if the file can be opened as an image and is not empty.
    """
    if image_file is None:
        print("DEBUG: validate_image: image_file is None.")
        return False
    try:
        img = Image.open(image_file)
        img.verify()  # Verify that it is an image
        # Reset file pointer after verify if you want to read it again
        image_file.seek(0)
        print(f"DEBUG: validate_image: {image_file.name if hasattr(image_file, 'name') else 'unknown file'} is a valid image.")
        return True
    except Exception as e:
        print(f"ERROR: validate_image failed for {image_file.name if hasattr(image_file, 'name') else 'unknown file'}: {e}")
        return False

def get_image_metadata(image_file):
    """
    Extracts basic metadata from an image file.
    """
    metadata = {}
    try:
        img = Image.open(image_file)
        metadata["dimensions"] = f"{img.width} × {img.height}"
        metadata["format"] = img.format
        # Get file size from the BytesIO object if it's already in memory
        if hasattr(image_file, 'seek') and hasattr(image_file, 'tell'):
            current_pos = image_file.tell()
            image_file.seek(0, os.SEEK_END)
            metadata["size"] = f"{image_file.tell() / 1024:.1f} KB"
            image_file.seek(current_pos) # Reset cursor
        elif hasattr(image_file, 'size'): # For st.file_uploader.UploadedFile
             metadata["size"] = f"{image_file.size / 1024:.1f} KB"
        else:
            metadata["size"] = "N/A"
        
        print(f"DEBUG: Image metadata extracted: {metadata}")
        return metadata
    except Exception as e:
        print(f"ERROR getting image metadata: {e}")
        metadata["error"] = str(e)
        return metadata


def format_medical_report(abha_id, prediction, confidence, analysis_datetime_str, image_metadata=None):
    """
    Formats the medical report data as a dictionary.
    """
    # Ensure datetime is imported at the top of the file
    report = {
        "Patient_ID": abha_id,
        "Analysis_Date": datetime.datetime.strptime(analysis_datetime_str, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"),
        "Analysis_Time": datetime.datetime.strptime(analysis_datetime_str, "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S"),
        "Prediction": prediction,
        "Confidence_Score": f"{confidence * 100:.2f}%",
        "Confidence_Level": "Very High" if confidence > 0.9 else "High" if confidence > 0.8 else "Medium" if confidence > 0.6 else "Low",
        "Risk_Category": "HIGH RISK" if prediction == "Malignant" else "LOW RISK",
        "Risk_Level": "Severe" if prediction == "Malignant" and confidence > 0.8 else \
                             "Moderate" if prediction == "Malignant" else "Minimal",
        "Urgency": "Immediate Consultation" if prediction == "Malignant" else "Routine Follow-up",
        "Recommendation": "Urgent specialist referral and further diagnostic tests (biopsy, advanced imaging) recommended." if prediction == "Malignant" else \
                               "Continue routine screening as per clinical guidelines. Consult a physician for overall breast health assessment.",
        "AI_Model": "CNN v1.0 (OpenVINO Optimized)",
        "Analysis_Type": "Breast Cancer Screening (Image-based)",
        "Model_Architecture": "Custom CNN",
        "Input_Resolution": f"{TARGET_SIZE[0]}x{TARGET_SIZE[1]} pixels",
        "Processing_Method": "Preprocessing + OpenVINO Inference + Grad-CAM Visualization"
    }

    if image_metadata:
        report["Image_Format"] = image_metadata.get("format", "N/A")
        report["Image_Size"] = image_metadata.get("size", "N/A")
        report["Original_Dimensions"] = image_metadata.get("dimensions", "N/A")
    else:
        report["Image_Format"] = "N/A"
        report["Image_Size"] = "N/A"
        report["Original_Dimensions"] = "N/A"

    print(f"DEBUG: Medical report formatted for Patient ID: {abha_id}")
    return report

def save_analysis_history(abha_id, prediction, confidence, analysis_datetime_str, file_path="data/breast_cancer_history.csv"):
    """
    Saves the current analysis to a CSV file for patient history tracking.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    new_record = {
        'ABHA_ID': abha_id,
        'Prediction': prediction,
        'Confidence': confidence,
        'Date': analysis_datetime_str
    }
    
    new_df = pd.DataFrame([new_record])
    
    if os.path.exists(file_path):
        try:
            existing_df = pd.read_csv(file_path)
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            print(f"DEBUG: Appending new record for ABHA_ID {abha_id} to existing history.")
        except pd.errors.EmptyDataError:
            # Handle case where CSV exists but is empty
            updated_df = new_df
            print(f"DEBUG: Starting new history in existing empty CSV for ABHA_ID {abha_id}.")
        except Exception as e:
            print(f"ERROR reading existing history file: {e}")
            return False # Indicate failure
    else:
        updated_df = new_df
        print(f"DEBUG: Creating new history file for ABHA_ID {abha_id}.")
    
    try:
        updated_df.to_csv(file_path, index=False)
        print(f"DEBUG: Analysis history saved successfully for ABHA_ID {abha_id}.")
        return True
    except Exception as e:
        print(f"ERROR saving updated history to CSV: {e}")
        return False # Indicate failure