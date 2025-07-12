# convert_model.py

import tensorflow as tf
import openvino as ov
import os
import sys

# --- Configuration ---
# Path to your original Keras .h5 model
H5_MODEL_PATH = "models/cnn_based_breast_cancer_pred.h5" 

# Directory where the OpenVINO IR files (.xml and .bin) will be saved
# This directory will be created if it doesn't exist.
OUTPUT_DIR = "models_openvino"

# Base name for the OpenVINO IR files (e.g., "cnn_based_breast_cancer_pred_ov.xml")
MODEL_NAME = "cnn_based_breast_cancer_pred_ov"

# --- Model's Expected Input Shape ---
# IMPORTANT: This MUST match the input shape your Keras model expects.
# Based on your error log: Keras model input shape: (None, 64, 64, 3)
INPUT_SHAPE = [1, 64, 64, 3] # Corrected input shape for your 64x64x3 model

# --- Script Logic ---
def main():
    print(f"Starting model conversion from '{H5_MODEL_PATH}' to OpenVINO IR...")

    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Ensured output directory '{OUTPUT_DIR}' exists.")

    # Check if the H5 model file exists
    if not os.path.exists(H5_MODEL_PATH):
        print(f"Error: Keras H5 model file not found at '{H5_MODEL_PATH}'.")
        print("Please ensure your .h5 model is in the specified path.")
        sys.exit(1) # Exit with an error code

    # Load the Keras model
    try:
        keras_model = tf.keras.models.load_model(H5_MODEL_PATH)
        print("Keras model loaded successfully.")
        print(f"Keras model input shape: {keras_model.input_shape}")
        
        # This warning will now ideally not appear if INPUT_SHAPE is correctly set
        if list(keras_model.input_shape) != [None] + INPUT_SHAPE[1:]: # Compare ignoring batch size
            print(f"Warning: Detected Keras model input shape {keras_model.input_shape} "
                  f"does not fully match specified INPUT_SHAPE for conversion {INPUT_SHAPE}.")
            print("Please double-check INPUT_SHAPE in this script.")

    except Exception as e:
        print(f"Error loading Keras model from '{H5_MODEL_PATH}': {e}")
        print("Please ensure it's a valid Keras .h5 model and your TensorFlow version is compatible.")
        sys.exit(1)

    # Convert to OpenVINO IR
    try:
        ov_model = ov.convert_model(keras_model, 
                                     input=ov.runtime.PartialShape(INPUT_SHAPE))
        
        output_xml_path = os.path.join(OUTPUT_DIR, f"{MODEL_NAME}.xml")
        ov.save_model(ov_model, output_xml_path)
        
        print(f"\n--- Conversion Successful! ---")
        print(f"OpenVINO IR model saved to:")
        print(f"  '{output_xml_path}'")
        print(f"  '{os.path.splitext(output_xml_path)[0]}.bin'") 
        print(f"You can now use these .xml and .bin files with OpenVINO.")
        print(f"Remember to add these files to your Git repository before deploying to Streamlit Cloud.")

    except Exception as e:
        print(f"\nError converting model to OpenVINO IR: {e}")
        print("Possible causes:")
        print("  - Incorrect INPUT_SHAPE specified in this script (though we just fixed it, re-verify if error persists).")
        print("  - Issues with your Keras model's layers or operations not fully supported by OpenVINO (less common).")
        print("  - Missing OpenVINO development tools (ensure `pip install openvino-dev[tensorflow2]`).")
        sys.exit(1)

if __name__ == "__main__":
    main()