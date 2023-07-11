


import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

import "./app.css";
import App from "./App.svelte";

const firebaseConfig = {
	apiKey: "AIzaSyABNk9oM5G2gZZy0_XrKAT-eAPI7q6feLs",
	authDomain: "mbotfbase.firebaseapp.com",
	projectId: "mbotfbase",
	storageBucket: "mbotfbase.appspot.com",
	messagingSenderId: "311121570177",
	appId: "1:311121570177:web:e6472526cb1d1eedaba080",
	measurementId: "G-5GXRMHKLR5"
};
const firebaseApp = initializeApp(firebaseConfig)
const auth = getAuth(firebaseApp);

auth.onAuthStateChanged(user => {
	if (user) {
		console.log(user);
	} else {
		console.log("User is logged out.")
	}
});

const app = new App({
	target: document.getElementById('app'),
});

export default app
