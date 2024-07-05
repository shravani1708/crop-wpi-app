from flask import Flask, render_template, request, jsonify
import pickle
import requests
import pandas as pd
from flask_cors import CORS
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np
import warnings
import itertools

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the crop prediction model
with open('models/RandomForest.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Ignore warnings for ARIMA model
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

    weather_api_key = '6daa8091ea0a64e28c136f2a3a55a3b9'
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'
    response = requests.get(weather_url)
    weather_data = response.json()
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']

    data_df = pd.DataFrame({
        'N': [npk_values[0]],
        'P': [npk_values[1]],
        'K': [npk_values[2]],
        'temperature': [temperature],
        'humidity': [humidity],
        'ph': [ph],
        'rainfall': [rainfall]
    })

    prediction = model.predict(data_df)[0]
    return jsonify({'prediction': prediction})

@app.route('/wpi-forecast', methods=['POST'])
def wpi_forecast():
    data = request.get_json()
    commodity_name = data['commodity']

    df_commodity = df[df['COMM_NAME'] == commodity_name]

    if df_commodity.empty:
        return jsonify({'error': 'Commodity not found in dataset'})

    train_size = int(len(df_commodity) * 0.8)
    train, test = df_commodity.iloc[:train_size], df_commodity.iloc[train_size:]

    p = d = q = range(0, 3)
    pdq = list(itertools.product(p, d, q))

    best_rmse = float('inf')
    best_params = None
    for param in pdq:
        try:
            model = ARIMA(train['WPI'], order=param)
            model_fit = model.fit()
            forecast_test = model_fit.forecast(steps=len(test))
            rmse = np.sqrt(mean_squared_error(test['WPI'], forecast_test))
            if rmse < best_rmse:
                best_rmse = rmse
                best_params = param
        except:
            continue

    model = ARIMA(df_commodity['WPI'], order=best_params)
    model_fit = model.fit()
    forecast_steps = 12
    forecast_next_year = model_fit.forecast(steps=forecast_steps)

    last_date = df_commodity.index[-1]
    forecast_dates = pd.date_range(last_date, periods=forecast_steps + 1, freq='M')[1:]

    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecasted WPI': forecast_next_year})

    return jsonify({'forecast': forecast_df.to_dict(orient='records')})

if __name__ == '__main__':
    app.run(debug=True)
