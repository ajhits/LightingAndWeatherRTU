import React, { useEffect, useState } from 'react';
import './control.css'; // Assuming the CSS changes are saved here
import { useNavigate } from 'react-router-dom';
import { getHistory, updateRelay } from '../firebase/Database';
import axios from 'axios';

const Control = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [buttonStates, setButtonStates] = useState({
    button1: false,
    button2: false,
    button3: false,
    button4: false
  });
  const [History,setHistory] = useState([]);
  const [currentTime, setCurrentTime] = useState('');
  const [todayDate, setTodayDate] = useState('');
  const [temperature, setTemperature] = useState(34.4);
  const history = useNavigate();

  useEffect(()=>{

    let isLightsOn = false;
    let isFanOn = false;
    
    // History
    getHistory().then(data=>{
    
      setHistory(Object.values(data));
    });

    // date
    const intervalId = setInterval(() => {

      const currentHour = new Date().getHours();
      if (!isLightsOn && currentHour >= 17) {
        console.log("Lights on");

        updateRelay({
          relay: 6,
          value: true
        });

        setButtonStates({ ...buttonStates, button1: true }); 
        isLightsOn = true; // Update state variable

      } 
      
      setCurrentTime(new Date().toLocaleTimeString());
    }, 1000);
    setTodayDate(new Date().toLocaleDateString());

    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=14.5905&lon=121.1040&appid=68d66ae5bea72e2ae26bb322cd719393`;

    axios.get(apiUrl)
      .then(response => {

        const data = response.data;
        const temperature = Math.round(data.main.temp - 273.15);
        console.log(temperature)
        setTemperature(temperature);

        if (!isFanOn && temperature >= 34){
          console.log("Fan On")
          updateRelay({
            relay: 13,
            value: !buttonStates['button2'] 
          });

          setButtonStates({ ...buttonStates, button2: !buttonStates['button2'] }); 
          isFanOn = true;
        }
      })
      .catch(error => {
        console.error('Error fetching weather data:', error);
      });

    return () => clearInterval(intervalId);
  },[]);

  const handleNavigation = (path) => {
    history(path);
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  const toggleButton = (button,relay) => {
  
    setButtonStates({ ...buttonStates, [button]: !buttonStates[button] });
    updateRelay({
      relay: relay,
      value: !buttonStates[button]
    });
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
          onClick={e =>{ e.preventDefault(); toggleButton('button1','6'); } }
        >
          {buttonStates.button1 ? 'Lights On' : ' Lights Off'}
        </button>
        <button
          className={`button-2 ${buttonStates.button2 ? 'active' : ''}`}
          onClick={e =>{ e.preventDefault(); toggleButton('button2','13'); }}
        >
          {buttonStates.button2 ? 'Fan On' : 'Fan Off'}
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
      <br></br>
      {/* Display Text for Time, Date, and Temperature */}
      <div>
        <p>Current Time: {currentTime}</p>
        <p>Today's Date: {todayDate}</p>
        <p>Temperature: {temperature}</p>
      </div>

      <br/><br/>
      {/* Table Component */}
      <h2 className="table-name">Daily Record</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Enter Count</th>
            <th>Date</th>
         
          </tr>
        </thead>
        <tbody>
          {/* Example row */}
          {Object.entries(getDataByDate(History)).map((data, index) => (
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
