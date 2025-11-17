<script lang="ts">
	import '../styles/app.css';
	import '../app.postcss';

	import {
		AppBar, Dialog, Portal
	} from '@skeletonlabs/skeleton-svelte';
	import { XIcon } from '@lucide/svelte';
	import Login from '../components/Login.svelte';
	import LeftNavBar from '../components/LeftNavBar.svelte';
	import LightSwitch from '../components/LightSwitch.svelte';

	const animBackdrop = 'transition transition-discrete opacity-0 starting:data-[state=open]:opacity-0 data-[state=open]:opacity-100';
	const animDrawer = 'transition transition-discrete opacity-0 -translate-x-full starting:data-[state=open]:opacity-0 starting:data-[state=open]:-translate-x-full data-[state=open]:opacity-100 data-[state=open]:translate-x-0';

	let tag = "div";

</script>

<!-- Drawer (mobile sidebar) -->
<Dialog>
	<!-- Trigger button lives in the AppBar -->
	<Portal>
		<!-- Backdrop -->
		<Dialog.Backdrop
			class="fixed inset-0 z-50 bg-surface-50-950/50 {animBackdrop}"
		/>

		<!-- Drawer panel -->
		<Dialog.Positioner class="fixed inset-0 z-50 flex justify-start">
			<Dialog.Content
				class="h-screen card bg-surface-100-900 w-sm p-4 shadow-xl {animDrawer}"
			>
				<header class="flex justify-between items-center mb-4">
					<Dialog.Title class="text-xl font-bold">Menu</Dialog.Title>
					<Dialog.CloseTrigger class="btn-icon preset-tonal">
						<XIcon />
					</Dialog.CloseTrigger>
				</header>

				<!-- Your sidebar content -->
				<LeftNavBar />
			</Dialog.Content>
		</Dialog.Positioner>
	</Portal>

	<!-- PAGE LAYOUT -->
	<div class="flex flex-col min-h-screen bg-surface-50 dark:bg-surface-900">

		<!-- Header -->
		<AppBar class="flex justify-between items-center px-4">
			<!-- Left side: logo + mobile drawer trigger -->
			<div class="flex items-center space-x-4">
				<Dialog.Trigger class="lg:hidden btn btn-sm">
					<svg viewBox="0 0 100 80" class="fill-token w-4 h-4">
						<rect width="100" height="20" />
						<rect y="30" width="100" height="20" />
						<rect y="60" width="100" height="20" />
					</svg>
				</Dialog.Trigger>
				<strong class="text-xl uppercase">mbot (💬🤖)</strong>
			</div>

			<!-- Right side: LightSwitch + Login -->
			<div class="flex items-center space-x-4">
				<LightSwitch />
				<Login />
			</div>
		</AppBar>

		<!-- MAIN CONTENT ROW -->
		<div class="flex flex-1">

			<!-- Desktop persistent sidebar -->
			<aside class="hidden lg:block w-64 border-r bg-surface-100 dark:bg-surface-800">
				<LeftNavBar />
			</aside>

			<!-- Main page content -->
			<main class="flex-1 p-6">
				<slot />
			</main>
		</div>

	</div>
</Dialog>

<style>
	.login-block {
		display: flex;
		align-items: center;
	}
</style>