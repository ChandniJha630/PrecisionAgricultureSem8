from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from PIL import Image
import base64
import os
import pytz
from io import BytesIO
import google.generativeai as genai
import requests

app = Flask(__name__)
CORS(app)

# ------------------ Configuration ------------------ #
# Google Gemini setup
genai.configure(api_key="YOUR_GEMINI_API_KEY")
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# MongoDB setup
client = MongoClient("mongodb+srv://chandnijha630:abc@cluster0.mbrxcya.mongodb.net/?retryWrites=true&w=majority")
db = client["IOT"]
collection = db["data"]

# Create upload folder if not exists
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ------------------ Utility Functions ------------------ #
def get_current_ist_time():
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")


# ------------------ Routes ------------------ #
@app.route('/')
def home():
    return "Precision Agriculture Flask Backend Running!"


@app.route('/upload-image', methods=['POST'])
def upload_image():
    try:
        data = request.get_json()
        image_data = data['image'].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"captured_{timestamp}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)

        return jsonify({"message": f"Image saved as {filename}"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/predict-disease', methods=['POST'])
def predict_disease():
    try:
        data = request.get_json()
        image_data = data['image'].split(",")[1]
        image_bytes = base64.b64decode(image_data)

        image_part = {
            "mime_type": "image/png",
            "data": image_bytes
        }

        prompt = (
            "You are a plant pathology expert. Analyze this leaf image and predict the disease. "
            "Respond only with the disease name (or 'Healthy' if no disease)."
        )

        response = gemini_model.generate_content([prompt, image_part])
        predicted_label = response.text.strip()

        return jsonify({"predicted_disease": predicted_label})
    except Exception as e:
        return jsonify({"error": f"Prediction error: {str(e)}"})


@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        disease = data.get('disease', '')

        prompt = (
            f"Suggest practical treatments for the crop disease: {disease}. "
            "Keep it short and give 3–4 actionable points."
        )

        response = gemini_model.generate_content(prompt)
        suggestion = response.text.strip()

        return jsonify({"suggestion": suggestion})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/local-weather', methods=['GET'])
def get_latest_local_station_data():
    try:
        # MongoDB connection
        client = MongoClient(
            'mongodb+srv://chandnijha630:abc@cluster0.mbrxcya.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
        )
        db = client['IOT']
        collection = db['data']
        
        # Fetch the latest data based on timestamp
        data = collection.find_one(sort=[("CreatedAt", -1)])  
        
        if data:
            # Return the latest data
            return jsonify({
                "temperature": data.get("Temperature", 0),
                "humidity": data.get("Humidity", 0),
                "rain": data.get("Rain", 0),
                "timestamp": data.get("CreatedAt", get_current_ist_time()).strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            return jsonify({"error": "No sensor data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/predicted-weather', methods=['GET'])
def get_predicted_weather():
    # Dummy values for predicted data
    predicted = {
        "temperature": 29.7,
        "humidity": 72,
        "rain": 5,
        "timestamp": get_current_ist_time()
    }
    return jsonify(predicted)


# ------------------ Run Server ------------------ #
if __name__ == "__main__":
    app.run(debug=True)
