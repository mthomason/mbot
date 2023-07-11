<script>
	import ChatWindow from './components/ChatWindow.svelte';
	import NavBar from './components/NavBar.svelte';
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
