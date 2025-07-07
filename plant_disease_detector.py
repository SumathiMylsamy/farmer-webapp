import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import csv
import sqlite3
from datetime import datetime

# Load model once
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("plant_disease_model.h5")

# Load labels
def load_labels():
    with open("labels.txt", "r") as f:
        return [line.strip() for line in f.readlines()]

# Log prediction to CSV and SQLite
def log_prediction(image_name, predicted_label):
    # Log to CSV
    with open("prediction_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), image_name, predicted_label])

    # Log to SQLite
    conn = sqlite3.connect("predictions.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            timestamp TEXT,
            image_name TEXT,
            prediction TEXT
        )
    ''')
    cursor.execute("INSERT INTO predictions VALUES (?, ?, ?)", (datetime.now(), image_name, predicted_label))
    conn.commit()
    conn.close()

# Optional disease info & prevention dictionary
disease_info = {
    "Tomato___Early_blight": {
        "info": "Early blight is caused by the fungus *Alternaria solani*. It causes leaf spots and defoliation.",
        "prevention": "Use disease-free seeds, rotate crops, and apply fungicides early."
    },
    "Tomato___Late_blight": {
        "info": "Late blight is caused by *Phytophthora infestans* and spreads rapidly in humid weather.",
        "prevention": "Destroy infected plants, avoid overhead irrigation, and use resistant varieties."
    },
    "Tomato___Leaf_Mold": {
        "info": "Leaf mold appears as yellow spots on the upper leaf surface and olive-green mold underneath.",
        "prevention": "Improve air circulation and avoid high humidity."
    },
    "Tomato___healthy": {
        "info": "Your tomato plant looks healthy with no visible symptoms. 🎉",
        "prevention": "Continue with good watering, sunlight, and monitoring."
    }
    # Add more diseases if needed
}

# Main detector function
def show_disease_detector():
    st.subheader("🧠 Plant Disease Detection")

    uploaded_file = st.file_uploader("📤 Upload a Leaf Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='📸 Uploaded Image', use_container_width=True)

        model = load_model()
        labels = load_labels()

        size = (224, 224)
        img = image.resize(size)
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        prediction = model.predict(img_array)
        predicted_index = np.argmax(prediction)
        predicted_label = labels[predicted_index]
        confidence = prediction[0][predicted_index]

        st.success(f"✅ Prediction: **{predicted_label}**")
        st.info(f"🔍 Confidence: {confidence * 100:.2f}%")

        # Show info & tips
        if predicted_label in disease_info:
            st.subheader("🦠 Disease Info")
            st.write(disease_info[predicted_label]["info"])

            st.subheader("🛡️ Prevention Tips")
            st.write(disease_info[predicted_label]["prevention"])

        # Log prediction
        log_prediction(uploaded_file.name, predicted_label)
