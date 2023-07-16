<!-- /frontend/src/components/LeftNavBar.svelte -->
<script lang="ts">

	let items: {title: string; content: string; }[] = [
		{ title: 'Unread Emails', content: 'Content 1' },
		{ title: 'Old Messages', content: 'Content 2' },
		{ title: 'Documents', content: 'Content 3' }
	];
</script>

<aside class="left-nav-bar">
	<ul>
		{#each items as item (item.title)}
			<li>
				<h2>{item.title}</h2>
				<p>{item.content}</p>
			</li>
		{/each}
	</ul>
</aside>

<style>
	.left-nav-bar {
		width: 250px;
		height: 100vh;
		overflow-y: auto;
		position: fixed;
		left: 0;
		top: 0;
		padding: 1em;
		box-sizing: border-box;
		background: lightslategray;
	}
	.left-nav-bar ul {
		list-style: none;
		padding: 0;
		margin: 0;
	}
	.left-nav-bar li {
		margin-bottom: 1em;
	}
</style>