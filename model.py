import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle

# Generate synthetic data
np.random.seed(42)

temperatures = np.random.uniform(15, 40, 1000)  # Temperatures between 15 and 40 degrees Celsius
rainfall = np.random.uniform(0, 150, 1000)      # Rainfall between 0 and 150 mm
crops = np.random.choice(['rice', 'wheat', 'beets', 'corn', 'potatoes'], 1000)  # Randomly choose crop types

# Assume some synthetic water usage patterns
def calculate_water_usage(temp, rain, crop):
    base_usage = {
        'rice': 2.0,
        'wheat': 1.0,
        'beets': 1.2,
        'corn': 1.8,
        'potatoes': 1.5
    }
    temp_factor = 0.1 * (temp - 20)  # More water needed for higher temperatures
    rain_factor = -0.05 * rain       # Less water needed with more rainfall
    return max(base_usage[crop] + temp_factor + rain_factor, 0)  # Ensure non-negative water usage

water_usage = np.array([calculate_water_usage(temp, rain, crop) for temp, rain, crop in zip(temperatures, rainfall, crops)])

# Create DataFrame
data = {
    'temperature': temperatures,
    'rainfall': rainfall,
    'crop': crops,
    'water_usage': water_usage
}
df = pd.DataFrame(data)

# Preprocess data
df['crop'] = df['crop'].astype('category').cat.codes  # Convert crop names to numerical codes

# Features and target variable
X = df[['temperature', 'rainfall', 'crop']]
y = df['water_usage']

# Train a model
model = RandomForestRegressor()
model.fit(X, y)

# Save the model to a pickle file
with open('crop_water_usage_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved successfully!")

