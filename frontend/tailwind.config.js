
export default {
	darkMode: ['attr', 'data-mode'],
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		'./node_modules/@skeletonlabs/skeleton/**/*.{html,js,svelte,ts}',
	],
	theme: {
		extend: {}
	},
	plugins: [
		require('@tailwindcss/typography')
	]
};
