<!-- /frontend/src/components/LeftNavBar.svelte -->
<script lang="ts">
	import { Dialog } from '@skeletonlabs/skeleton-svelte';

	let items: {title: string; content: string; anchor: string; }[] = [
		{ title: 'Home', content: 'Home', anchor: '/' },
		{ title: 'Chat', content: 'Chat', anchor: '/chat' },
		{ title: 'Account', content: 'Account', anchor: '/account' },
		{ title: 'Browser', content: 'Browser', anchor: '/browser' },
		{ title: 'About', content: 'About', anchor: '/about' },
	];

</script>

<nav class="list-nav p-4">
	<ul>
		{#each items as item (item.title)}
			<li>
				<Dialog.CloseTrigger>
					<a href="{item.anchor}" title="{item.title}">
						{item.content}
					</a>
				</Dialog.CloseTrigger>
			</li>
		{/each}
	</ul>
</nav>

<style>

</style>
