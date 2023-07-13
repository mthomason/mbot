<!-- /frontend/src/components/ToolBar.svelte -->
<script lang="ts">

</script>

<nav class="toolbar">
	<ul class="toolbar-list">
		<li class="toolbar-item"><a href="#link1" class="toolbar-link">Link 1</a></li>
		<li class="toolbar-item"><a href="#link2" class="toolbar-link">Link 2</a></li>
		<!-- Add more links as needed -->
	</ul>
</nav>

<style>
nav.toolbar {
	/* background-color: #f8f9fa; */
	padding: 15px 0;
	box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}
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
	/* color: #333; */
	font-size: 16px;
	transition: color 0.3s ease;
}
.toolbar-link:hover {
	color: #007BFF;
}
</style>
