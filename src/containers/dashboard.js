import React, { useEffect, useState } from 'react';
import './Dashboard.css'; // Import CSS file
import { useNavigate } from 'react-router-dom';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { LogoutSession } from '../firebase/Authentication';
import { getHistory } from '../firebase/Database';

const Dashboard = () => {
  const [isDarkMode] = useState(false);
  const [History,setHistory] = useState([])
  const [Enter,setEnter] = useState([])
  const [Exit,setExit] = useState([])
  const history = useNavigate(); // Initialize useNavigate hook


  const filtered = (data,date,value) =>{
    return Object.values(data).filter(entry => {
      return entry.date === String(date).replace(",","") && entry.person_status === value;
    });
  } 

  const today = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: '2-digit', // Ensure the day is represented with two digits
  });
  
  // Adjusting the date format to remove comma and add leading zero if necessary
  const formattedToday = today.replace(",", "").replace(/\b(\d{1})\b/g, "0$1");
  
  console.log(formattedToday); // Output: "April 01 2024"
  

  useEffect(()=>{


    getHistory()
      .then(data=>{
        

        // const filteredData = Object.values(data).filter(entry => String(entry.date) === String(today).replace(",",""));
        // console.log("Filtered data:", filteredData); 
        setHistory(data)
        setEnter(filtered(data,today,'person in'))
        setExit(filtered(data,today,'person out'))
      })
  },[today])

  const handleNavigation = (path) => {
    history(path);
  };

  const handleLogout = () => {
    LogoutSession();
  };

  const goToSettings = () => {
    // Redirect to settings page
    history('/user-profile');
  };

  // const toggleDarkMode = () => {
  //   setIsDarkMode(!isDarkMode);
  // };

  return (
    <div className={`dashboard-container ${isDarkMode ? 'dark-mode' : ''}`}>
      {/* Header */}
      <div className="header">
        <button className="account-icon" onClick={goToSettings}>
          <i className="fas fa-user"></i>
        </button>
        {/* <button className="mode-toggle" onClick={toggleDarkMode}>
          {isDarkMode ? 'Light Mode' : 'Dark Mode'}
        </button> */}
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
        {/* <div className="info-box">
          <h2>User</h2>
          <p>John Doe</p>
        </div> */}

        
        {/* Enter Info */}
        <div className="info-box">
          <h2>Enter</h2>
          <p>{Enter.length}</p>
        </div>
        {/* Exit Info */}
        <div className="info-box">
          <h2>Exit</h2>
          <p>{Exit.length}</p>
        </div>
        {/* Today's Info */}
        <div className="info-box">
          <h2>Today</h2>
          <p>{String(today).replace(",","")}</p>
        </div>
      </div>

      {/* Table Component */}
      <h2 className="table-name">Daily Record</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Status</th>
            <th>Date</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {/* Example row */}
          {Object.values(History)
          .filter(data=> data.date === String(today).replace(",",""))
          .map((value,key)=>(
            <tr key={key}>
            <td>{key}</td>
            <td>{value.person_status}</td>
            <td>{value.date}</td>
            <td>{value.time}</td>
          </tr>
          ))}
 
          {/* Add more rows as needed */}
        </tbody>
      </table>
    </div>
  );
};

export default Dashboard;
