import React from "react";
import LoginPage from "./containers/login";

import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";

// import ToastManager from "./components/toast";


// pages
import DashboardPage from "./containers/dashboard";
import Control from "./containers/control";
import Userprofile from "./containers/userprofile";

// import RegisterPage from "./containers/register";
import useAuth from "./firebase/Status";
// import ForgotpasswordPage from "./containers/forgotpassword";
// import ChangepasswordPage from "./containers/changepassword";
// import NotfoundPage from "./containers/notfound";
// import UserProfilePage from "./containers/userprofile";



function App() {
  const { user,data } = useAuth();
  return (
    <>

        {user === "login" && <LogInAdmin  /> }
        {user === "panel" && <AdminIsLogin data={data}/> }

    </>
  );
}

// user need to Login
const LogInAdmin = () =>{
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage/>}/>
        <Route path="*" element={<Navigate to="/"/>}/>
      </Routes>
    </Router>
  )
}

// user is already Login
const AdminIsLogin = ({ data }) => {
  return (
    <Router>
    {/* Userprofile */}
      <Routes>
        <Route path="/" element={<DashboardPage/>}/>
        <Route path="/user-profile" element={<Userprofile data={data}/>}/>
        <Route path="/control" element={<Control/>}/>
        <Route path="*" element={<Navigate to="/" />}/>
      </Routes>
    </Router>
  )
}

export default App;
