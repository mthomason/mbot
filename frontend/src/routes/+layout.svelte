<script>
	import '@skeletonlabs/skeleton/themes/theme-skeleton.css';
	import '@skeletonlabs/skeleton/styles/skeleton.css';
	import '../app.postcss';
	import { AppShell, AppBar, LightSwitch } from '@skeletonlabs/skeleton';
	import Login from '../components/Login.svelte';
</script>

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				💬🤖
			</svelte:fragment>
			<svelte:fragment slot="trail">
				<LightSwitch /><Login />
			</svelte:fragment>
			<svelte:fragment slot="headline">mbot</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<slot />
</AppShell>
