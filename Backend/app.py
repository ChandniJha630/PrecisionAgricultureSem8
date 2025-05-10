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
import boto3
from botocore.exceptions import ClientError
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# ------------------ Configuration ------------------ #
# Google Gemini AI setup
genai.configure(api_key="YOUR_GEMINI_API_KEY")
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# Create upload folder if not exists
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ------------------ Utility Functions ------------------ #
def get_current_ist_time():
    """Returns the current IST time in YYYY-MM-DD HH:MM:SS format."""
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

# AWS Configuration
region_name = "us-east-2"
table_name = "farm-data"

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=region_name)
table = dynamodb.Table(table_name)

@app.route('/local-weather', methods=['GET'])
def fetch_latest_data():
    try:
        # Scan the table to get all records
        response = table.scan()

        items = response.get("Items", [])
        if items:
            # Sort items by CreatedAt and return the latest one
            latest_entry = max(items, key=lambda x: x.get("id", ""))
            return jsonify(latest_entry), 200
        else:
            return jsonify({"message": "No data found"}), 404

    except ClientError as e:
        return jsonify({"error": e.response['Error']['Message']}), 500

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