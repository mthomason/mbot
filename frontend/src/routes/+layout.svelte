<script>
	//  These imports are required for the apps style to work...
	//  Order is important!  Do not change!  First is the theme, then the
	//     skeleton styles, then the app styles.
	// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
	import '@skeletonlabs/skeleton/themes/theme-hamlindigo.css';
	import '@skeletonlabs/skeleton/styles/skeleton.css';
	import '../app.postcss';
	// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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
