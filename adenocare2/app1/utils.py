import tensorflow as tf
import os

def load_model():
    # Construct the path to the .keras file
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'lung_cancer_vgg16', 'lung_cancer_vgg16.keras')
    
    # Debug: Print the path to verify
    print(f"Loading model from: {model_path}")

    # Check if the file exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")

    try:
        # Load the model
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        raise ValueError(f"Error loading model: {e}")