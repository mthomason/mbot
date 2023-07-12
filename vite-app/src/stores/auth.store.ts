
import { writable } from "svelte/store";

export const authentication = writable({
	isLoggedIn: false,
	firebaseControlled: false,
	user: null,
});

//export const setAuthStore = (authStoreData: { isLoggedIn: boolean; firebaseControlled: boolean; user: null;}) => {
//	authStore.set(authStoreData);
//}
