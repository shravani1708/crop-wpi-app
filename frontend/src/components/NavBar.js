import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/crop-prediction">Crop Yield Prediction</Link></li>
                <li><Link to="/wpi-forecast">WPI Forecast</Link></li>
            </ul>
        </nav>
    );
};

export default Navbar;
