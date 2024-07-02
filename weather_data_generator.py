import requests
import pandas as pd
from datetime import datetime, timedelta
import time  # for handling rate limits

# Function to fetch historical weather data
def fetch_historical_weather_data(api_key, location, start_date, end_date):
    url_template = "http://api.weatherapi.com/v1/history.json?key={}&q={}&dt={}"
    
    date = start_date
    weather_data = []
    
    while date <= end_date:
        url = url_template.format(api_key, location, date.strftime("%Y-%m-%d"))
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if 'forecast' in data and 'forecastday' in data['forecast'] and len(data['forecast']['forecastday']) > 0:
                day_data = data['forecast']['forecastday'][0]['day']
                weather_data.append({
                    'date': date.strftime("%Y-%m-%d"),
                    'temperature': day_data['avgtemp_c'],
                    'rainfall': day_data['totalprecip_mm']
                })
            else:
                print(f"No data available for {date.strftime('%Y-%m-%d')} in {location}")
        else:
            print(f"Failed to fetch data for {date.strftime('%Y-%m-%d')} in {location}. Status code: {response.status_code}")
            print(response.content)  # Print response content for debugging
        
        date += timedelta(days=1)
        time.sleep(0.5)  # Add a small delay between requests to avoid rate limiting
    
    return pd.DataFrame(weather_data)

# Your WeatherAPI key
api_key = "6118487079e745cc8db91725240207"
location = "Cairo"  # Update location to Cairo
start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2023-12-31", "%Y-%m-%d")

# Fetch the weather data
weather_data = fetch_historical_weather_data(api_key, location, start_date, end_date)

# Save the data to a CSV file
weather_data.to_csv("cairo_weather_data.csv", index=False)

print("Historical weather data for Cairo fetched and saved successfully!")

