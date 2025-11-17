<script lang="ts">
	import { Sun, Moon } from '@lucide/svelte';
	import { onMount } from 'svelte';

	let isDark = false;

	onMount(() => {
		const stored = localStorage.getItem('mode');
		if (stored === 'dark') {
			isDark = true;
		} else if (stored === 'light') {
			isDark = false;
		} else {
			isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
		}
		applyTheme(isDark);
	});

	function toggle() {
		isDark = !isDark;
		applyTheme(isDark);
	}

	function applyTheme(dark: boolean) {
		const mode = dark ? 'dark' : 'light';
		document.documentElement.setAttribute('data-mode', mode);
		localStorage.setItem('mode', mode);
	}
</script>

<button
	class="btn btn-sm flex items-center gap-2"
	type="button"
	on:click={toggle}
	aria-label="Toggle light/dark mode">
	{#if isDark}
		<Sun class="w-4 h-4" />
	{:else}
		<Moon class="w-4 h-4" />
	{/if}
</button>
