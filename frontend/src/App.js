import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import CropPredictionForm from './components/CropPredictionForm';
import WpiForecast from './components/WpiForecast';
import PredictionsPage from './pages/PredictionsPage';
import Weather from './components/Weather';
import Navbar from './components/NavBar';

const App = () => {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/crop-prediction" element={<CropPredictionForm />} />
                <Route path="/wpi-forecast" element={<WpiForecast />} />
                <Route path="/weather" element={<Weather />} />
            </Routes>
        </Router>
    );
};

export default App;
