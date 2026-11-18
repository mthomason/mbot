import { expect, test } from '@playwright/test';

test('home page renders the app shell and chat controls', async ({ page }) => {
	await page.goto('/');

	await expect(page.getByText(/mbot \(💬🤖\)/)).toBeVisible();
	await expect(page.getByRole('heading', { name: 'Home', level: 2 })).toBeVisible();
	await expect(page.getByPlaceholder('Write a message...')).toBeVisible();
	await expect(page.getByRole('button', { name: 'Send' })).toBeVisible();
});

test('primary routes render their content', async ({ page }) => {
	const routes: Array<[string, string]> = [
		['/about', 'About'],
		['/account', 'Account'],
		['/browser', 'Browser Information'],
		['/chat', 'Chat'],
		['/dev', 'Chat']
	];

	for (const [route, heading] of routes) {
		await page.goto(route);
		await expect(page.getByRole('heading', { name: heading, level: 2 })).toBeVisible();
	}
});

test('sidebar links navigate between pages', async ({ page }) => {
	await page.goto('/');
	await page.getByRole('link', { name: 'About' }).click();

	await expect(page).toHaveURL(/\/about$/);
	await expect(page.getByRole('heading', { name: 'About', level: 2 })).toBeVisible();
});
