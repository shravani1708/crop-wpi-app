import React from 'react';
import Navbar from '../components/NavBar';
import CropPredictionForm from '../components/CropPredictionForm';
import WpiForecast from '../components/WpiForecast';

const PredictionsPage = () => {
    return (
        <div>
            <Navbar />
            <h1>Predictions</h1>
            <div style={{ display: 'flex', justifyContent: 'space-around' }}>
                <div>
                    <CropPredictionForm />
                </div>
                <div>
                    <WpiForecast />
                </div>
            </div>
        </div>
    );
};

export default PredictionsPage;
