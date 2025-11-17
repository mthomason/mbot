<script lang="ts">
	import { Sun, Moon } from '@lucide/svelte';
	import { onMount } from 'svelte';

	let isDark = false;

	onMount(() => {
		// Get stored preference, or default to system
		const stored = localStorage.getItem('theme');
		if (stored === 'dark') {
			isDark = true;
		} else if (stored === 'light') {
			isDark = false;
		} else {
			// No stored preference — use OS preference
			isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
		}
		applyTheme(isDark);
	});

	function toggle() {
		isDark = !isDark;
		applyTheme(isDark);
	}

	function applyTheme(dark: boolean) {
		if (dark) {
			document.documentElement.classList.add('dark');
			localStorage.setItem('theme', 'dark');
		} else {
			document.documentElement.classList.remove('dark');
			localStorage.setItem('theme', 'light');
		}
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
