import React, { useState } from 'react';
import './control.css'; // Assuming the CSS changes are saved here
import { useNavigate } from 'react-router-dom';

const Control = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [buttonStates, setButtonStates] = useState({
    button1: false,
    button2: false,
    button3: false,
    button4: false
  });
  const history = useNavigate();

  const handleNavigation = (path) => {
    history(path);
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  const toggleButton = (button) => {
    setButtonStates({ ...buttonStates, [button]: !buttonStates[button] });
  };

  return (
    <div className={`dashboard-container ${isDarkMode ? 'dark-mode' : ''}`}>
      {/* Header */}
      <div className="header">
        <button className="account-icon" onClick={() => handleNavigation('/user-profile')}>
          <i className="fas fa-user"></i>
        </button>
        <button className="mode-toggle" onClick={toggleDarkMode}>
          {isDarkMode ? 'Light Mode' : 'Dark Mode'}
        </button>
        <button className="control-btn" onClick={() => handleNavigation('/dashboard')}>
          Dashboard
        </button>
        <button className="logout-button" onClick={() => handleNavigation('/login')}>
          Logout
        </button>
      </div>

      {/* Button Controls */}
      <div className="central-components">
        <button
          className={`button-1 ${buttonStates.button1 ? 'active' : ''}`}
          onClick={() => toggleButton('button1')}
        >
          {buttonStates.button1 ? 'On' : 'Off'}
        </button>
        <button
          className={`button-2 ${buttonStates.button2 ? 'active' : ''}`}
          onClick={() => toggleButton('button2')}
        >
          {buttonStates.button2 ? 'On' : 'Off'}
        </button>
        <button
          className={`button-3 ${buttonStates.button3 ? 'active' : ''}`}
          onClick={() => toggleButton('button3')}
        >
          {buttonStates.button3 ? 'On' : 'Off'}
        </button>
        <button
          className={`button-4 ${buttonStates.button4 ? 'active' : ''}`}
          onClick={() => toggleButton('button4')}
        >
          {buttonStates.button4 ? 'On' : 'Off'}
        </button>
      </div>

      <br></br><br></br>
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

export default Control;
