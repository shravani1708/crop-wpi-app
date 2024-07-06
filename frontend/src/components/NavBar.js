import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/NavBar.css'; // Import the CSS file

const Navbar = () => {
    return (
        <nav className="navbar">
            <ul className="nav-list">
                <li className="nav-item"><Link to="/">Home</Link></li>
                <li className="nav-item"><Link to="/crop-prediction">Crop Yield Prediction</Link></li>
                <li className="nav-item"><Link to="/wpi-forecast">WPI Forecast</Link></li>
                <li className="nav-item"><Link to="/weather">Weather</Link></li> {/* Add Weather to the Navbar */}
            </ul>
        </nav>
    );
};

export default Navbar;
