import React, { useState } from 'react';
import './Dashboard.css'; // Import CSS file
import { useHistory } from 'react-router-dom';
import '@fortawesome/fontawesome-free/css/all.min.css';

const Dashboard = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [userData, setUserData] = useState({
    username: 'John Doe',
    currentPassword: '',
    newPassword: '',
    retypeNewPassword: '',
    email: '',
    phoneNumber: ''
  });
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
    history.push('/settings');
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserData({ ...userData, [name]: value });
  };
  

  const handleSubmit = (e) => {
    e.preventDefault();
    // Implement logic to submit user profile data
    console.log('Submitting user profile data:', userData);
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
        <button className="control-btn" onClick={() => handleNavigation('/dashboard')}>
          Home
        </button>
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>

      {/* User Info */}
      <div className="user-info">
        <div className="info-box">
          <h2>User</h2>
          <p>{userData.username}</p>
        </div>
      </div>

      {/* User Profile Form */}
      <form className="user-profile-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Username:</label>
          <input type="text" name="username" value={userData.username} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Current Password:</label>
          <input type="password" name="currentPassword" value={userData.currentPassword} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>New Password:</label>
          <input type="password" name="newPassword" value={userData.newPassword} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Retype New Password:</label>
          <input type="password" name="retypeNewPassword" value={userData.retypeNewPassword} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Email:</label>
          <input type="email" name="email" value={userData.email} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Phone Number:</label>
          <input type="text" name="phoneNumber" value={userData.phoneNumber} onChange={handleChange} />
        </div>
        <button type="submit">Save</button>
      </form>
    </div>
  );
};

export default Dashboard;
