<script>
	import svelteLogo from './assets/svelte.svg'
	import viteLogo from '/vite.svg'
	import Counter from './lib/Counter.svelte'
	import ChatWindow from './components/ChatWindow.svelte';
	import TestChatDisplay from './components/TestChatDisplay.svelte';
	import NavBar from './components/NavBar.svelte';
</script>

<header class="bg-secondary p-4 flex justify-between items-center text-white">
	<NavBar />
</header>
<main>
	<!--
		<a href="https://vitejs.dev">Vite JS Site</a>
		<a href="https://svelte.dev">Svelte Site</a>
	-->
	<div class="app-chat-block">
		<!--TestChatDisplay /-->
		<ChatWindow />
	</div>
</main>
