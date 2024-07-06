import React from 'react';
import Navbar from '../components/NavBar';
import '../styles/HomePage.css'; // Import the CSS file

const HomePage = () => {
    return (
        <div className="home-container">
            <div className="content">
                <h1>Welcome to Crop and WPI Prediction App</h1>
                <p>Choose an option from the navigation bar above.</p>
            </div>
        </div>
    );
};

export default HomePage;
