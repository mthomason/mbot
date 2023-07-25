<!-- /frontend/src/components/LeftNavBar.svelte -->
<script lang="ts">
	import { drawerStore } from '@skeletonlabs/skeleton';

	let items: {title: string; content: string; anchor: string; }[] = [
		{ title: 'Chat', content: 'Chatbot', anchor: '/' },
		{ title: 'Home', content: 'Home', anchor: '/' },
		{ title: 'About', content: 'About', anchor: '/about' },
	];

	function drawerClose(): void {
		drawerStore.close();
	}

</script>

<nav class="list-nav p-4">
	<ul>
		{#each items as item (item.title)}
			<li>
				<a href="{item.anchor}" title="{item.title}"
				   on:click={drawerClose}>
					{item.content}
				</a>
			</li>
		{/each}
	</ul>
</nav>

<style>

</style>
