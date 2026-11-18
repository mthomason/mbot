import js from '@eslint/js';
import svelte from 'eslint-plugin-svelte';
import globals from 'globals';
import ts from 'typescript-eslint';

export default ts.config(
	js.configs.recommended,
	...ts.configs.recommended,
	...svelte.configs.recommended,
	{
		languageOptions: {
			globals: {
				...globals.browser,
				...globals.node
			}
		}
	},
	{
		files: ['**/*.svelte'],
		languageOptions: {
			parserOptions: {
				parser: ts.parser
			}
		}
	},
	{
		rules: {
			// markdown-it escapes raw HTML in its source by default, so rendering its
			// generated Markdown output with {@html} is intentional here.
			'svelte/no-at-html-tags': 'off',
			// The browser-info page intentionally inspects untyped navigator properties.
			'@typescript-eslint/no-explicit-any': 'off'
		}
	},
	{
		ignores: [
			'.svelte-kit/',
			'build/',
			'node_modules/',
			'test-results/',
			'playwright-report/'
		]
	}
);
