import { expect, test } from '@playwright/test';

test('theme switcher works correctly', async ({ page }) => {
	await page.goto('/');

	const html = page.locator('html');

	// 1. Initial theme is light
	await expect(html).toHaveAttribute('data-mode', 'light');
	await page.screenshot({ path: 'light-mode.png' });

	// 2. Toggle to dark mode
	await page.getByLabel('Toggle light/dark mode').click();
	await expect(html).toHaveAttribute('data-mode', 'dark');
	await page.screenshot({ path: 'dark-mode.png' });

	// 3. Reload and check for persistence
	await page.reload();
	await expect(html).toHaveAttribute('data-mode', 'dark');
});
