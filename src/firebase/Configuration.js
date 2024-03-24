import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getDatabase } from "firebase/database";
import { getFirestore } from "firebase/firestore";
import { getStorage  } from "firebase/storage";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAf0T76wl4Xil88rTg7sLX0wN3_AXzay6Q",
  authDomain: "ai-smart-classroom.firebaseapp.com",
  projectId: "ai-smart-classroom",
  storageBucket: "ai-smart-classroom.appspot.com",
  messagingSenderId: "717041352251",
  appId: "1:717041352251:web:e1c2e4ce912b5d0d4de61e"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// for firebase authentication
export const auth = getAuth(app);

// for firebase storage
export const storage = getStorage();

// for fire store database
export const firestore = getFirestore(app);

// for realtime database
export const database = getDatabase(app);