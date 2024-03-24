import React, { useState } from 'react';
import './Dashboard.css'; // Import CSS file
import { useHistory } from 'react-router-dom';
import '@fortawesome/fontawesome-free/css/all.min.css';

const Dashboard = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const history = useHistory(); // Initialize useHistory hook

  const handleNavigation = (path) => {
    history.push(path);
  };

  const handleLogout = () => {
    // Implement your logout logic here
    console.log('Logging out...');
    // Redirect to login page
    history.push('/login');
  };

  const goToSettings = () => {
    // Redirect to settings page
    history.push('/user-profile');
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div className={`dashboard-container ${isDarkMode ? 'dark-mode' : ''}`}>
      {/* Header */}
      <div className="header">
        <button className="account-icon" onClick={goToSettings}>
          <i className="fas fa-user"></i>
        </button>
        <button className="mode-toggle" onClick={toggleDarkMode}>
          {isDarkMode ? 'Light Mode' : 'Dark Mode'}
        </button>
        <button className="control-btn" onClick={() => handleNavigation('/control')}>
          Controls
        </button>
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>

      {/* Central Components */}
      <div className="central-components">
        {/* User Info */}
        <div className="info-box">
          <h2>User</h2>
          <p>John Doe</p>
        </div>
        {/* Enter Info */}
        <div className="info-box">
          <h2>Enter</h2>
          <p>08:00 AM</p>
        </div>
        {/* Exit Info */}
        <div className="info-box">
          <h2>Exit</h2>
          <p>05:00 PM</p>
        </div>
        {/* Today's Info */}
        <div className="info-box">
          <h2>Today</h2>
          <p>2024-03-20</p>
        </div>
      </div>

      {/* Table Component */}
      <h2 className="table-name">Daily Record</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {/* Example row */}
          <tr>
            <td>1</td>
            <td>John Doe</td>
            <td>2024-03-20</td>
          </tr>
          {/* Add more rows as needed */}
        </tbody>
      </table>
    </div>
  );
};

export default Dashboard;
