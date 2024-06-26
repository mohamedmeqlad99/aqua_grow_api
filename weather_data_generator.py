import requests
import pandas as pd
from datetime import datetime, timedelta

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
            day_data = data['forecast']['forecastday'][0]['day']
            weather_data.append({
                'date': date,
                'temperature': day_data['avgtemp_c'],
                'rainfall': day_data['totalprecip_mm']
            })
        else:
            print(f"Failed to fetch data for {date.strftime('%Y-%m-%d')}")
        
        date += timedelta(days=1)
    
    return pd.DataFrame(weather_data)

# Your WeatherAPI key
api_key = "your_api_key_here"  # Replace with your actual API key
location = "Egypt"
start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2023-12-31", "%Y-%m-%d")

# Fetch the weather data
weather_data = fetch_historical_weather_data(api_key, location, start_date, end_date)

# Save the data to a CSV file
weather_data.to_csv("egypt_weather_data.csv", index=False)

print("Historical weather data fetched and saved successfully!")
