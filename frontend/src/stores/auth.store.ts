
import { writable, type Writable } from "svelte/store";
import {
	getAuth,
	getIdToken,
	GoogleAuthProvider,
	signInWithPopup,
	signOut,
	type Auth,
	type User,
	type UserCredential,
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

export const authentication: Writable<{
	isLoggedIn: boolean,
	firebaseControlled: boolean,
	idToken: string | null,
	uniqueUserID: string | null,
	user: User | null}> = writable(
		{
			isLoggedIn: false,
			firebaseControlled: false,
			idToken: null,
			uniqueUserID: null,
			user: null
		}
	);

auth.onAuthStateChanged(async (user: User | null) => {
	console.log("Auth state changed.");
	if (user) {
		console.log(user.displayName);
		console.log(user.email);
		console.log(user.photoURL);
		console.log(user.uid);
		console.log(user.providerId);
		console.log(user.emailVerified);
		console.log(user.isAnonymous);
		console.log(user.metadata);
		console.log(user.phoneNumber);
		console.log(user.providerData);
		console.log(user.refreshToken);
		console.log(user.tenantId);
		let idToken: string = await user.getIdToken();
		console.log(user.toJSON());
		console.log(idToken);
		authentication.set({
			isLoggedIn: true,
			firebaseControlled: true,
			idToken: idToken,
			uniqueUserID: user.uid,
			user: user
		});
		console.log("User is logged in.");
		console.log(user);
	} else {
		authentication.set({
			isLoggedIn: false,
			firebaseControlled: true,
			idToken: null,
			uniqueUserID: null,
			user: null
		});
		console.log("User is not logged in.");
	}
});

export async function login() {
	try {
		const provider: GoogleAuthProvider = new GoogleAuthProvider();
		const result: UserCredential = await signInWithPopup(auth, provider);
		let webAuthToken: string = await result.user.getIdToken();
		authentication.set({
			isLoggedIn: true,
			firebaseControlled: true,
			idToken: webAuthToken,
			uniqueUserID: result.user.uid,
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
			idToken: null,
			uniqueUserID: null,
			user: null
		});
	} catch (error) {
		console.error("Error logging out.", error);
	}
}
