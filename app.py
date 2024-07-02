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
def fetch_weather_data():
    api_key = "6118487079e745cc8db91725240207"  # Replace with your actual API key
    location = "Cairo"  # Fixed location
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=7"
    response = requests.get(url)
    
    print(f"Request URL: {url}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")

    if response.status_code == 200:
        data = response.json()
        forecast_days = data['forecast']['forecastday']
        weekly_data = []
        for day in forecast_days:
            date = day['date']
            temperature = day
