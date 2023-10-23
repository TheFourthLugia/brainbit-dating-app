// Import the functions you need from the SDKs you need
  		import { initializeApp } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-app.js";
  		import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.4.0/firebase-analytics.js";
  		// TODO: Add SDKs for Firebase products that you want to use
  		// https://firebase.google.com/docs/web/setup#available-libraries

  		// Your web app's Firebase configuration
  		// For Firebase JS SDK v7.20.0 and later, measurementId is optional
 		const firebaseConfig = {
    		apiKey: "AIzaSyCsicBUwHKkpBWIdqD-eKVnv31RE0fUsEQ",
    		authDomain: "neurobit-dating.firebaseapp.com",
    		projectId: "neurobit-dating",
    		storageBucket: "neurobit-dating.appspot.com",
    		messagingSenderId: "164425965182",
    		appId: "1:164425965182:web:0542e471e0268c4d31c22f",
		measurementId: "G-JTSGZE9XWW"
  		};
  		// Initialize Firebase
  		const app = initializeApp(firebaseConfig);
  		const analytics = getAnalytics(app);
