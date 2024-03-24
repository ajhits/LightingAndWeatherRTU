import React, { useEffect, useState } from 'react';
import './Dashboard.css'; // Import CSS file
import { useNavigate } from 'react-router-dom';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { getUserDetails } from '../firebase/Firestore';
import { changing_password } from '../firebase/Authentication';

const Dashboard = (props) => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [userData, setUserData] = useState({
    currentPassword: '',
    newPassword: '',
    retypeNewPassword: '',
  });

  const [details, setDetails] = useState({
    name: 'John Doe',
    email: 'test@gmail.com',
    phoneNumber: '+63 934569310'
  });

  const history = useNavigate(); // Initialize useHistory hook

  const handleNavigation = (path) => {
    history(path);
  };

  const handleLogout = () => {
    // Implement your logout logic here
    console.log('Logging out...');
    // Redirect to login page
    history('/login');
  };

  const goToSettings = () => {
    // Redirect to settings page
    history('/settings');
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

    changing_password(
  userData.currentPassword,
      userData.newPassword
    )
    .then(data=>console.log(data))
  };

  useEffect(()=>{
    getUserDetails(props.data)
    .then(data=>{
      setDetails({
        name: data.name,
        email: data.email,
        phoneNumber: data.phone
      })

    })
    .catch(error=>console.log(error))
  },[props.data])

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
          <h2>{details.name}</h2>
          <p>{details.email}</p>
          <p>{details.phoneNumber}</p>    
        </div>

      </div>


      {/* User Profile Form */}
      <form className="user-profile-form" onSubmit={handleSubmit}>

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


        <button type="submit">save password</button>
      </form>
    </div>
  );
};

export default Dashboard;
