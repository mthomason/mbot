<!-- /frontend/src/components/ToolBar.svelte -->
<script>
	import { onMount, onDestroy } from 'svelte';
	import { login, logout } from '../stores/auth.store'
	import { authentication } from '../stores/auth.store'

	let user = null;

	const unsubscribe = authentication.subscribe((value) => {
		user = value;
	});

	onDestroy(() => {
		unsubscribe();
	});
</script>

<nav class="toolbar">
{#if user}
	<button on:click={logout}>Logout</button>
	<div>Welcome, {user.displayName}</div>
{:else}
	<button on:click={login}>Login with Google</button>
{/if}
	<!--ul class="toolbar-list">
		<li class="toolbar-item"><a href="#link1" class="toolbar-link">Link 1</a></li>
		<li class="toolbar-item"><a href="#link2" class="toolbar-link">Link 2</a></li>
	</ul-->
</nav>

<style>
nav.toolbar {
	padding: 15px 0;
	box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}
/*
.toolbar-list {
	list-style-type: none;
	margin: 0;
	padding: 0;
	display: flex;
	justify-content: space-around;
}
.toolbar-item {
	padding: 0 10px;
}
.toolbar-link {
	text-decoration: none;
	color: #f8f9fa;
	font-size: 16px;
	transition: color 0.3s ease;
}
.toolbar-link:hover {
	color: #007BFF;
}
*/
</style>
