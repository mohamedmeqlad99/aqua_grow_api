from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS

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
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        
        data = response.json()
        forecast_days = data['forecast']['forecastday']
        weekly_data = []
        for day in forecast_days:
            date = day['date']
            temperature = day['day']['avgtemp_c']
            rainfall = day['day']['totalprecip_mm']
            weekly_data.append((date, temperature, rainfall))
        return weekly_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recommendation', methods=['POST'])
def recommendation():
    data = request.get_json()
    crop = data.get('crop')

    if not crop:
        return jsonify({'error': 'Crop is required'}), 400

    weekly_weather_data = fetch_weather_data()
    
    if weekly_weather_data is None:
        return jsonify({'error': 'Could not fetch weather data'}), 500

    if crop not in crop_mapping:
        return jsonify({'error': 'Invalid crop type'}), 400

    crop_code = crop_mapping[crop]
    recommendations = []

    for week_data in weekly_weather_data:
        date, temperature, rainfall = week_data
        # Prepare the input data for the model
        input_data = pd.DataFrame([[temperature, rainfall, crop_code]], columns=['temperature', 'rainfall', 'crop'])
        
        # Make a prediction
        predicted_water_usage = model.predict(input_data)[0]

        recommendations.append({
            'date': date,
            'temperature': temperature,
            'recommended_water_usage': f'{predicted_water_usage:.2f} liters of water per square meter'
        })

    return jsonify({'recommendations': recommendations})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True)


