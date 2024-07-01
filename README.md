# AquaGrow API

AquaGrow is a Flask-based API that provides water usage recommendations for agricultural lands based on real-time weather data. The recommendations are generated using a machine learning model trained on historical weather data and crop-specific water usage patterns.

## Features

- Fetch real-time weather data for any location.
- Generate water usage recommendations for five crops: Rice, Wheat, Beets, Corn, and Potatoes.
- API endpoint for health checks.

## Getting Started

### Prerequisites

- Python 3.7+
- Flask
- Requests
- Pandas
- Scikit-learn
- WeatherAPI key (you can sign up for an API key at [WeatherAPI](https://www.weatherapi.com/))

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/aquagrow.git
    cd aquagrow
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
