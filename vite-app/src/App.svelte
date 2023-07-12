<script>

	import { onDestroy } from 'svelte';
	import { authentication } from './stores/auth.store'
	import ChatWindow from './components/ChatWindow.svelte';
	import NavBar from './components/NavBar.svelte';
/*
	const unsubscribe_auth = authentication.subscribe((user) => {
		if (user) {
			console.log(user)
		} else {
			console.log('no user')
		}
	});

	onDestroy(() => {
		unsubscribe_auth();
	});
*/
</script>
<header class="bg-secondary p-4 flex justify-between items-center text-white">
	<h1 class="font-bold text-sm md:text-2xl tracking-widest">mbot</h1>
</header>
<NavBar />
<main>
	<div class="app-chat-block">
		<ChatWindow />
	</div>
</main>
