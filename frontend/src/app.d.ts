// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
// and what to do when importing types
declare namespace App {
	// interface Error {}
	// interface Locals {}
	// interface PageData {}
	// interface Platform {}
}

// Allow side-effect imports of PostCSS files.
declare module '*.postcss' {
	const css: string;
	export default css;
}
