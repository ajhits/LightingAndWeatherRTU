import React from "react";
import LoginPage from "./containers/login";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { PrivateRoute } from "./library/helper";

import ToastManager from "./components/toast";


// pages
import DashboardPage from "./containers/dashboard";
import RegisterPage from "./containers/register";
import ForgotpasswordPage from "./containers/forgotpassword";
import ChangepasswordPage from "./containers/changepassword";
import NotfoundPage from "./containers/notfound";
import UserProfilePage from "./containers/userprofile";
import control from "./containers/control";


function App() {
  return (
    <>
      <Router>
        <Switch>
          <Route exact path="/" component={LoginPage} />
          <Route exact path="/login" component={LoginPage} />
          <Route exact path="/register" component={RegisterPage} />
          <Route exact path="/forgot-password" component={ForgotpasswordPage} />
          <Route exact path="/change-password" component={ChangepasswordPage} />
          <Route exact path="/dashboard" component={DashboardPage} />
          <Route exact path="/user-profile" component={UserProfilePage} />
          <Route exact path="/control" component={control} />
          <Route path="*" component={NotfoundPage} />
        </Switch>
      </Router>
      
      <ToastManager />
    </>
  );
}

export default App;
