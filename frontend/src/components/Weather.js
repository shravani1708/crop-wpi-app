import React, { useState } from 'react';
import axios from 'axios';
import '../styles/Weather.css'; // Import the CSS file

const Weather = () => {
    const [city, setCity] = useState('');
    const [weatherData, setWeatherData] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/weather', { city });
            setWeatherData(response.data);
            setError(null);
        } catch (error) {
            setError('Error fetching weather data. Please try again.');
            setWeatherData(null);
            console.error('Error fetching weather data:', error);
        }
    };

    const handleCityChange = (e) => setCity(e.target.value);

    return (
        <div className="weather-container">
            <h2>Weather Forecast</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    City:
                    <input type="text" value={city} onChange={handleCityChange} />
                </label>
                <button type="submit">Get Weather</button>
            </form>
            {error && <p className="error">{error}</p>}
            {weatherData && (
                <div className="weather-report">
                    <h3>Weather in {weatherData.city} today:</h3>
                    <p>Max Temperature: {weatherData.maxTemp}°C</p>
                    <p>Min Temperature: {weatherData.minTemp}°C</p>
                    <p>Humidity: {weatherData.humidity}%</p>
                    <p>Wind Speed: {weatherData.windSpeed} m/s</p>
                    <p>Sunrise Time: {weatherData.sunriseTime}</p>
                    <p>Sunset Time: {weatherData.sunsetTime}</p>
                </div>
            )}
        </div>
    );
};

export default Weather;
