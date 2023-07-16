Hi Top-Level-Lead-Architect-and-WebDev-GPT,

Give me modern but stripped down html and css for a basic but modern application skeleton layout with the following requirements:
1. I want it to have a LeftNavBar which fills up the vertical height.  When the content of that bar is filled, it will add scrollbars to the left nav bar.  You can add example content to the LeftNavBar.
2. I want it to have a bottom bar which fills up the horizontal width, until it bumps into the left nav bar.  When the content of that bar is filled, it will add scrollbars to the bottom bar.  In VS Code, this section has a terminal.
3. The main body content will have a chat window.
4. I don't want this done using a grid, because that is hackish, but it could be done using flexbox or flex columns or whatever.

I basically want the outline for a VS Code style user interface, using modern HTML 5 and CSS.

We are building a chatbot application.  It is a client-server application.  The frontend client is built in Svelte.  The backend is currently a restful API using Python3/FastAPI.

Everything is in a folder called `mbot`.  The frontend is in `mbot/vite-app` and the backend is in `mbot/backend`.

The backend is currently a restful API, built with Python3 and FastAPI.

The frontend is currently a Svelte app, built with Vite.

We are using Firebase for authentication.  The database will be on AWS S3 service.

Here's some details about the application.

`./vite-app/package.json
```
{
	"name": "vite-app",
	"private": true,
	"version": "0.0.0",
	"type": "module",
	"scripts": {
		"dev": "vite",
		"build": "vite build",
		"preview": "vite preview"
	},
	"devDependencies": {
		"@sveltejs/vite-plugin-svelte": "^2.0.4",
		"@types/markdown-it": "^12.2.3",
		"svelte": "^4.0.5",
		"typescript": "^5.1.6",
		"vite": "^4.4.3"
	},
	"dependencies": {
		"@tsconfig/svelte": "^5.0.0",
		"firebase": "^9.23.0",
		"markdown-it": "^13.0.1",
		"svelte-preprocess": "^5.0.4"
	}
}
```

`./vite-app/index.html`
```
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<link rel="icon" type="image/svg+xml" href="/vite.svg" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>mbot</title>
	</head>
	<body>
		<div id="app"></div>
		<script type="module" src="/src/main.ts" lang="ts"></script>
	</body>
</html>
```

`./vite-app/src/main.ts`
```
import "./app.css";
import App from "./App.svelte";

const app: App = new App({
	target: document.getElementById('app') as HTMLElement,
});

export default app
```

`./vite-app/src/App.svelte`
```
<script>
	import ChatWindow from './components/ChatWindow.svelte';
	import NavBar from './components/NavBar.svelte';
	import ToolBar from './components/ToolBar.svelte';
</script>
<ToolBar />
<header class="bg-secondary p-4 flex justify-between items-center text-white">
	<h1 class="font-bold text-sm md:text-2xl tracking-widest">mbot</h1>
</header>
<NavBar />
<main>
	<div class="app-chat-block">
		<ChatWindow />
	</div>
</main>
```

`./vite-app/src/stores/auth.store.ts`
```

import { writable, type Writable } from "svelte/store";
import {
	getAuth,
	onAuthStateChanged,
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
/* ... */
};

const firebaseApp: FirebaseApp = (getApps().length === 0) ?
	initializeApp(firebaseConfig) : getApp();

const auth: Auth = getAuth(firebaseApp);

export const authentication: Writable<User | null> = writable(null);

auth.onAuthStateChanged((user: User | null) => {
	if (user) {
		authentication.set(user);
		console.log("User is logged in.");
		console.log(user);
	} else {
		authentication.set(null);
		console.log("User is not logged in.");
	}
});

export async function login() {
	try {
		const provider: GoogleAuthProvider = new GoogleAuthProvider();
		const result: UserCredential = await signInWithPopup(auth, provider);
		authentication.set(result.user);
	} catch (error) {
		console.error("Error logging in.", error);
	}
}

export async function logout() {
	try {
		await signOut(auth);
		authentication.set(null);
	} catch (error) {
		console.error("Error logging out.", error);
	}
}
```

