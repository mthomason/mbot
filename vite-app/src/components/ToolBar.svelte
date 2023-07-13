<!-- /frontend/src/components/ToolBar.svelte -->
<script>
	import { onMount, onDestroy } from 'svelte';
	import { login, logout, authentication } from '../stores/auth.store'

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
	<div class="items-center space-x-2 hidden xl:inline-flex">
		<img src={user?.photoURL}
			 alt={user?.displayName}
			 class="h-12 w-12 avatar circle" />
		<div class="flex flex-col">
			<p>{user?.displayName}</p>
			<p>{user?.email}</p>
		</div>
		<button on:click={logout} class="bg-white p-2 rounded-full text-black">Logout</button>
	</div>
{:else}
	<button on:click={login}>Login with Google</button>
{/if}
</nav>

<style>

img.avatar.circle {
	height: 32px;
	aspect-ratio: auto 32 / 32;
	width: 32px;
}

.avatar {
	background-color: var(--color-avatar-bg);
	border-radius: var(--borderRadius-medium, 6px);
	box-shadow: 0 0 0 1px var(--color-avatar-border);
	display: inline-block;
	flex-shrink: 0;
	line-height: 1;
	overflow: hidden;
	vertical-align: middle;
}

.circle {
	border-radius: var(--borderRadius-full, 50%) !important;
}

</style>
