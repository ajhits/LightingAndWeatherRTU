import React, { useEffect } from "react";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "./Configuration";

function useAuth() {
  const [user, setUser] = React.useState();
  const [data, setData] = React.useState();

  useEffect(() => {
    const unsubscribeFromAuthStateChanged = onAuthStateChanged(auth, (user) => {
      if (user) {
        // User is signed in, see docs for a list of available properties
        // https://firebase.google.com/docs/reference/js/firebase.User
        setUser("panel");
        setData(user);
      } else {
        // User is signed out
        setUser("login");
        setData(null);
      }
    });

    return unsubscribeFromAuthStateChanged;
  }, []);

  return {
    user,
    data
  };
}

export default useAuth