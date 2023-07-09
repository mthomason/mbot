<script>
	import ChatWindow from './components/ChatWindow.svelte';
	import NavBar from './components/NavBar.svelte';
</script>
<header class="bg-secondary p-4 flex justify-between items-center text-white">
	<NavBar />
</header>
<main>
	<div class="app-chat-block">
		<ChatWindow />
	</div>
</main>
