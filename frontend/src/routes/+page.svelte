<!-- /frontend/src/routes/+page.svelte -->
<script>
	import ChatWindow from '../components/ChatWindow.svelte';
	import NavBar from '../components/NavBar.svelte';
	import ToolBar from '../components/ToolBar.svelte';
	//import LeftNavBar from '../components/LeftNavBar.svelte';
	//import BottomNavBar from '../components/BottomNavBar.svelte';
</script>

<ToolBar />
<header class="bg-secondary p-4 flex justify-between items-center text-white">
	<h1 class="font-bold text-sm md:text-2xl tracking-widest">mbot</h1>
</header>
<NavBar />
<!--LeftNavBar /-->
<main>
	<div class="app-chat-block">
		<ChatWindow />
	</div>
</main>
<!--BottomNavBar /-->

	<!-- @import '../styles/app.css'; -->

<style>
	@import '../styles/app.css';
</style>
