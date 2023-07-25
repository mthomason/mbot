
import { writable, type Writable } from "svelte/store";
import {
	getAuth,
	GoogleAuthProvider,
	signInWithPopup,
	signOut,
	type Auth,
	type User,
	type UserCredential
} from "firebase/auth";
import {
	initializeApp,
	getApp,
	getApps,
	type FirebaseOptions,
	type FirebaseApp
} from "firebase/app";

const firebaseConfig: FirebaseOptions = {
	apiKey: "AIzaSyABNk9oM5G2gZZy0_XrKAT-eAPI7q6feLs",
	authDomain: "mbotfbase.firebaseapp.com",
	projectId: "mbotfbase",
	storageBucket: "mbotfbase.appspot.com",
	messagingSenderId: "311121570177",
	appId: "1:311121570177:web:e6472526cb1d1eedaba080",
	measurementId: "G-5GXRMHKLR5"
};

const firebaseApp: FirebaseApp = (getApps().length === 0) ?
	initializeApp(firebaseConfig) : getApp();

const auth: Auth = getAuth(firebaseApp);

//export const authentication: Writable<User | null> = writable(null);
export const authentication: Writable<{
	isLoggedIn: boolean,
	firebaseControlled: boolean,
	user: User | null}> = writable(
		{
			isLoggedIn: false, firebaseControlled: false, user: null
		}
	);

//onMount(() => {
	auth.onAuthStateChanged((user: User | null) => {
		if (user) {
			authentication.set({
				isLoggedIn: true,
				firebaseControlled: true,
				user: user
			});
			console.log("User is logged in.");
			console.log(user);
		} else {
			authentication.set({
				isLoggedIn: false,
				firebaseControlled: true,
				user: null
			});
			console.log("User is not logged in.");
		}
	});
//});

export async function login() {
	try {
		const provider: GoogleAuthProvider = new GoogleAuthProvider();
		const result: UserCredential = await signInWithPopup(auth, provider);
		authentication.set({
			isLoggedIn: true,
			firebaseControlled: true,
			user: result.user
		});
	} catch (error) {
		console.error("Error logging in.", error);
	}
}

export async function logout() {
	try {
		await signOut(auth);
		authentication.set({
			isLoggedIn: false,
			firebaseControlled: true,
			user: null
		});
	} catch (error) {
		console.error("Error logging out.", error);
	}
}
