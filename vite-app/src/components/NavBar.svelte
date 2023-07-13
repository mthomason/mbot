<!-- /frontend/src/components/NavBar.svelte -->
<script lang="ts">
	/*
	import type { SvelteComponentTyped } from "svelte";
	class ComponentName extends SvelteComponentTyped<{propertyName: string;}> {}
	*/
</script>

<!-- o -->
<nav class="navbar">
	<ul class="navbar-list">
		<li class="navbar-item"><a href="#link1" class="navbar-link">Link 1</a></li>
		<li class="navbar-item"><a href="#link2" class="navbar-link">Link 2</a></li>
		<!-- Add more links as needed -->
	</ul>
</nav>

<!-- links -->
<!--div class="flex items-center space-x-3 font-semibold">
	<a href="/main">Main</a>
	<a href="/chat">Chat</a>
	<a href="/about">About</a>
</div-->

<style>
.navbar {
	/* background-color: #f8f9fa; */
	padding: 15px 0;
	box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

.navbar-list {
	list-style-type: none;
	margin: 0;
	padding: 0;
	display: flex;
	justify-content: space-around;
}
/*
.navbar-item {
	  padding: 0 10px;
}
*/
.navbar-link {
	text-decoration: none;
	/* color: #333; */
	color: #f8f9fa;
	font-size: 16px;
	transition: color 0.3s ease;
}

.navbar-link:hover {
	color: #007BFF;
}

</style>
