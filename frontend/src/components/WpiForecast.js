import React, { useState } from 'react';
import axios from 'axios';

const WpiForecast = () => {
    const [commodity, setCommodity] = useState('');
    const [forecast, setForecast] = useState([]);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/wpi-forecast', { commodity });
            console.log('Forecast response:', response.data);
            
            if (response.data.error) {
                setError(response.data.error);
                setForecast([]); // Clear forecast data on error
            } else {
                setForecast(response.data.forecast);
                setError(null); // Clear any previous errors
            }
        } catch (error) {
            console.error('Forecast error:', error);
            setError('Error fetching forecast. Please try again.');
        }
    };

    return (
        <div>
            <h2>WPI Forecast</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Commodity:
                    <input type="text" value={commodity} onChange={(e) => setCommodity(e.target.value)} />
                </label>
                <button type="submit">Get Forecast</button>
            </form>
            {error && <p>{error}</p>}
            {forecast.length > 0 && (
                <div>
                    <h3>Forecasted WPI for the next year:</h3>
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
