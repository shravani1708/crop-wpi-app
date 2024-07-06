import React, { useState } from 'react';
import axios from 'axios';
import '../styles/WpiForecast.css'; // Import the CSS file

const WpiForecast = () => {
    const [commodity, setCommodity] = useState('');
    const [forecast, setForecast] = useState([]);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formattedCommodity = commodity.charAt(0).toUpperCase() + commodity.slice(1);
        try {
            const response = await axios.post('http://localhost:5000/wpi-forecast', { commodity: formattedCommodity });
            console.log('Forecast response:', response.data);
            
            if (response.data.error) {
                setError(response.data.error);
                setForecast([]); // Clear forecast data on error
            } else {
                const adjustedForecast = handleNegativeValues(response.data.forecast);
                setForecast(adjustedForecast);
                setError(null); // Clear any previous errors
            }
        } catch (error) {
            console.error('Forecast error:', error);
            setError('Error fetching forecast. Please try again.');
        }
    };

    const handleNegativeValues = (forecastData) => {
        // Calculate average WPI for the commodity
        const averageWPI = forecastData.reduce((acc, item) => acc + item['Forecasted WPI'], 0) / forecastData.length;

        // Adjust negative values
        const adjustedForecast = forecastData.map(item => ({
            ...item,
            'Forecasted WPI': item['Forecasted WPI'] < 0 ? averageWPI : item['Forecasted WPI']
        }));

        return adjustedForecast;
    };

    const handleCommodityChange = (e) => {
        const value = e.target.value;
        setCommodity(value.charAt(0).toUpperCase() + value.slice(1));
    };

    return (
        <div className="form-container">
            <h2>WPI Forecast</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Commodity:
                    <input type="text" value={commodity} onChange={handleCommodityChange} />
                </label>
                <button type="submit">Get Forecast</button>
            </form>
            {error && <p className="error">{error}</p>}
            {forecast.length > 0 && (
                <div className="forecast-container">
                    <h3>Forecasted WPI for {commodity} for the next 12 months:</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Forecasted WPI</th>
                            </tr>
                        </thead>
                        <tbody>
                            {forecast.map((item, index) => (
                                <tr key={index}>
                                    <td>{item.Date}</td>
                                    <td>{item['Forecasted WPI']}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default WpiForecast;
