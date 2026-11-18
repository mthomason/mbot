import { expect, test } from '@playwright/test';

test('theme toggle switches to dark mode and persists', async ({ page }) => {
	await page.goto('/');
	await page.evaluate(() => localStorage.removeItem('mode'));
	await page.reload();

	const html = page.locator('html');
	await expect(html).toHaveAttribute('data-mode', 'light');

	await page.getByLabel('Toggle light/dark mode').click();
	await expect(html).toHaveAttribute('data-mode', 'dark');

	await page.reload();
	await expect(html).toHaveAttribute('data-mode', 'dark');
});
