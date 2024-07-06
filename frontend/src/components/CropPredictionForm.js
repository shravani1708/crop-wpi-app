import React, { useState } from 'react';
import axios from 'axios';
import '../styles/CropPredictionForm.css'; // Import the CSS file

const CropPredictionForm = () => {
    const [city, setCity] = useState('');
    const [N, setN] = useState('');
    const [P, setP] = useState('');
    const [K, setK] = useState('');
    const [ph, setPh] = useState('');
    const [rainfall, setRainfall] = useState('');
    const [prediction, setPrediction] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/predict', {
                city,
                N,
                P,
                K,
                ph,
                rainfall
            });
            setPrediction(response.data.prediction);
        } catch (error) {
            console.error('Prediction error:', error);
        }
    };

    return (
        <div className="form-container">
            <h2>Crop Yield Prediction</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    City:
                    <input type="text" value={city} onChange={(e) => setCity(e.target.value)} />
                </label>
                <label>
                    N:
                    <input type="number" value={N} onChange={(e) => setN(e.target.value)} />
                </label>
                <label>
                    P:
                    <input type="number" value={P} onChange={(e) => setP(e.target.value)} />
                </label>
                <label>
                    K:
                    <input type="number" value={K} onChange={(e) => setK(e.target.value)} />
                </label>
                <label>
                    pH:
                    <input type="number" value={ph} onChange={(e) => setPh(e.target.value)} />
                </label>
                <label>
                    Rainfall:
                    <input type="number" value={rainfall} onChange={(e) => setRainfall(e.target.value)} />
                </label>
                <button type="submit">Predict</button>
            </form>
            {prediction && <p className="prediction">Prediction: {prediction}</p>}
        </div>
    );
};

export default CropPredictionForm;
