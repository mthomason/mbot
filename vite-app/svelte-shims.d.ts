declare module "*.svelte" {
	import { SvelteComponent } from "svelte";
	const value: { default: typeof SvelteComponent };
	export default value;
}
