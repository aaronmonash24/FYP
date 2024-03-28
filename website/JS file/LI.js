// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyC9XLDV7n32YRIVbLnB_raDKi9cPsbTEjk",
  authDomain: "end-of-year-project-f8758.firebaseapp.com",
  projectId: "end-of-year-project-f8758",
  storageBucket: "end-of-year-project-f8758.appspot.com",
  messagingSenderId: "61188274891",
  appId: "1:61188274891:web:083e5bc3dfe8221c0a394e",
  measurementId: "G-MHB3N9BRNG",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// get ref to database services

const analytics = getAnalytics(app);
