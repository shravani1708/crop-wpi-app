import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CropPredictionForm from './components/CropPredictionForm';
import WpiForecast from './components/WpiForecast';
import PredictionsPage from './pages/PredictionsPage';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/crop-prediction" element={<CropPredictionForm />} />
                <Route path="/wpi-forecast" element={<WpiForecast />} />
                <Route path="/predictions" element={<PredictionsPage />} />
            </Routes>
        </Router>
    );
};

export default App;
