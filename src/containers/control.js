import React, { useEffect, useState } from 'react';
import './control.css'; // Assuming the CSS changes are saved here
import { useNavigate } from 'react-router-dom';
import { getHistory, updateRelay } from '../firebase/Database';

const Control = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [buttonStates, setButtonStates] = useState({
    button1: false,
    button2: false,
    button3: false,
    button4: false
  });
  const [History,setHistory] = useState([])
  const history = useNavigate();

  useEffect(()=>{


    getHistory()
      .then(data=>{
        setHistory(Object.values(data))
     
      })
  },[])

  const handleNavigation = (path) => {
    history(path);
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  const toggleButton = (button,relay) => {
   Object.entries(getDataByDate(History)).map((date, index)=>console.log(date[0],date[1]))
    setButtonStates({ ...buttonStates, [button]: !buttonStates[button] });
    updateRelay({
      relay: relay,
      value: !buttonStates[button]
    })
  };

  
const getDataByDate = (data) => {
  const dates = {};
  // Iterate through the data to collect unique dates and count entries for each date
  Object.values(data).forEach(entry => {
    const date = entry.date;
    if (!dates[date]) {
      dates[date] = 1;
    } else {
      dates[date]++;
    }
  });
  return dates;
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
          onClick={() => toggleButton('button1','6')}
        >
          {buttonStates.button1 ? 'On' : 'Off'}
        </button>
        <button
          className={`button-2 ${buttonStates.button2 ? 'active' : ''}`}
          onClick={() => toggleButton('button2','13')}
        >
          {buttonStates.button2 ? 'On' : 'Off'}
        </button>
        <button
          className={`button-3 ${buttonStates.button3 ? 'active' : ''}`}
          onClick={() => toggleButton('button3','19')}
        >
          {buttonStates.button3 ? 'On' : 'Off'}
        </button>
        <button
          className={`button-4 ${buttonStates.button4 ? 'active' : ''}`}
          onClick={() => toggleButton('button4','26')}
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

          {  Object.entries(getDataByDate(History)).map((data, index) => (
          <tr key={index}>
            <td>{index}</td>
            <td>{data[1]}</td>
            <td>{data[0]}</td>
          </tr>
        ))}
          {/* Add more rows as needed */}
        </tbody>
      </table>
    </div>
  );
};

export default Control;
