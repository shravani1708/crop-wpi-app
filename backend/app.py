from flask import Flask, render_template, request, jsonify
import pickle
import requests
import pandas as pd
from flask_cors import CORS
from pmdarima import auto_arima
import numpy as np
import warnings
from datetime import datetime
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the crop prediction model
with open('models/RandomForest.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Ignore warnings for SARIMA model
warnings.filterwarnings("ignore")

# Load WPI dataset
df = pd.read_csv(r"C:\Users\Shrav\Documents\Research\WPI data\combined_WPI_data_final.csv")
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    city = data['city']
    npk_values = [float(data[key]) for key in ['N', 'P', 'K']]
    ph = float(data['ph'])
    rainfall = float(data['rainfall'])

    # Fetch weather data from API
    weather_api_key = '6daa8091ea0a64e28c136f2a3a55a3b9'
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'
    response = requests.get(weather_url)
    weather_data = response.json()
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']

    # Prepare input data for crop prediction
    data_df = pd.DataFrame({
        'N': [npk_values[0]],
        'P': [npk_values[1]],
        'K': [npk_values[2]],
        'temperature': [temperature],
        'humidity': [humidity],
        'ph': [ph],
        'rainfall': [rainfall]
    })

    # Use RandomForest model for prediction
    prediction = model.predict(data_df)[0]
    return jsonify({'prediction': prediction})

@app.route('/wpi-forecast', methods=['POST'])
def wpi_forecast():
    data = request.get_json()
    commodity_name = data['commodity']

    df_commodity = df[df['COMM_NAME'] == commodity_name]

    if df_commodity.empty:
        return jsonify({'error': 'Commodity not found in dataset'})

    # Fit SARIMA model using auto_arima for automated model selection
    model = SARIMAX(df_commodity['WPI'], order=(0, 1, 2), seasonal_order=(0, 1, 0, 12))
    model_fit = model.fit(disp=False)

    # Forecast for one year starting from the current system date
    today = datetime.now().date()
    forecast_steps = 12
    forecast_dates = pd.date_range(start=today, periods=forecast_steps + 1, freq='M')[1:]

    # Generate forecasts and confidence intervals
    forecast_next_year = model_fit.get_forecast(steps=forecast_steps)
    forecast_mean = forecast_next_year.predicted_mean
    conf_int = forecast_next_year.conf_int()

    forecast_df = pd.DataFrame({
        'Date': forecast_dates,
        'Forecasted WPI': forecast_mean,
        'Lower CI': conf_int.iloc[:, 0],
        'Upper CI': conf_int.iloc[:, 1]
    })

    return jsonify({'forecast': forecast_df.to_dict(orient='records')})

@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    city = data.get('city')
    
    api_key = '6daa8091ea0a64e28c136f2a3a55a3b9'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'

    # Construct URL without date parameter to get current weather
    url = f'{base_url}?q={city}&appid={api_key}&units=metric'
    
    # Fetch weather data from the API
    response = requests.get(url)
    data = response.json()

    if 'main' in data and 'temp_max' in data['main'] and 'temp_min' in data['main']:
        max_temp = data['main']['temp_max'] - 273.15
        min_temp = data['main']['temp_min'] - 273.15

        # Get other weather information
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        # Check if sunrise and sunset timestamps exist in the response
        if 'sys' in data and 'sunrise' in data['sys'] and 'sunset' in data['sys']:
            sunrise_timestamp = data['sys']['sunrise']
            sunset_timestamp = data['sys']['sunset']
            
            # Convert sunrise and sunset times to readable format
            sunrise_time = datetime.fromtimestamp(sunrise_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            sunset_time = datetime.fromtimestamp(sunset_timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            sunrise_time = "Unknown"
            sunset_time = "Unknown"

        # Create formatted weather report
        report = {
            'city': city,
            'date': 'today',
            'maxTemp': max_temp,
            'minTemp': min_temp,
            'humidity': humidity,
            'windSpeed': wind_speed,
            'sunriseTime': sunrise_time,
            'sunsetTime': sunset_time
        }

        return jsonify(report)
    else:
        return jsonify({'error': 'Weather data not available for the given city.'})

if __name__ == '__main__':
    app.run(debug=True)
