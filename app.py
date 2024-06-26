from flask import Flask, request, jsonify
import requests
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained machine learning model
with open('crop_water_usage_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Mapping for crop names
crop_mapping = {'rice': 0, 'wheat': 1, 'beets': 2, 'corn': 3, 'potatoes': 4}

# Function to fetch weather data from an external API
def fetch_weather_data(location):
    api_key = "your_api_key_here"  # Replace with your actual API key
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temp_c']
        rainfall = data['current']['precip_mm']
        return temperature, rainfall
@app.route('/api/recommendation', methods=['POST'])
def recommendation():
    data = request.get_json()
    location = data.get('location')
    crop = data.get('crop')

    if not location or not crop:
        return jsonify({'error': 'Location and crop are required'}), 400

    temperature, rainfall = fetch_weather_data(location)
    
    if temperature is None or rainfall is None:
        return jsonify({'error': 'Could not fetch weather data'}), 500

    if crop not in crop_mapping:
        return jsonify({'error': 'Invalid crop type'}), 400

    crop_code = crop_mapping[crop]
    else:
        return None, None

@app.route('/api/recommendation', methods=['POST'])
def recommendation():
    data = request.get_json()
    location = data.get('location')
    crop = data.get('crop')
