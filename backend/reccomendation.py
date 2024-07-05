from flask import Flask, request, jsonify
import pickle
import requests
import pandas as pd

app = Flask(__name__)

# Load the RandomForest model
with open('models/RandomForest.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def index():
    return "Flask server is running."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Extract data from JSON request
        city = data['city']
        npk_values = [float(data[key]) for key in ['N', 'P', 'K']]
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])

        # Fetch weather data
        weather_api_key = '6daa8091ea0a64e28c136f2a3a55a3b9' 
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric'
        response = requests.get(weather_url)
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']

        # Prepare data for prediction
        data_df = pd.DataFrame({
            'N': [npk_values[0]],
            'P': [npk_values[1]],
            'K': [npk_values[2]],
            'temperature': [temperature],
            'humidity': [humidity],
            'ph': [ph],
            'rainfall': [rainfall]
        })

        # Make prediction using RandomForest model
        prediction = model.predict(data_df)[0]

        return jsonify({'prediction': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
