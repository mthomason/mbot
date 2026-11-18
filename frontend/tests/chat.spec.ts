import { expect, test } from '@playwright/test';

const PREVIEW_ORIGIN = 'http://127.0.0.1:4173';

test('sends a prompt and renders the streamed reply', async ({ page }) => {
	let captured: { body: unknown; authorization: string | undefined } | null = null;

	await page.route('http://localhost:8000/chat', async (route) => {
		const request = route.request();
		const corsHeaders = {
			'access-control-allow-origin': PREVIEW_ORIGIN,
			'access-control-allow-methods': 'POST, OPTIONS',
			'access-control-allow-headers': 'authorization, content-type'
		};

		if (request.method() === 'OPTIONS') {
			await route.fulfill({ status: 204, headers: corsHeaders });
			return;
		}

		captured = {
			body: JSON.parse(request.postData() ?? '{}'),
			authorization: request.headers()['authorization']
		};

		await route.fulfill({
			status: 200,
			headers: {
				...corsHeaders,
				'content-type': 'application/x-ndjson'
			},
			body:
				[
					JSON.stringify({ user_id: 'test-user', content: 'Hello', is_end: false }),
					JSON.stringify({ user_id: 'test-user', content: ' **world**', is_end: true })
				].join('\n') + '\n'
		});
	});

	await page.goto('/');
	await page.getByPlaceholder('Write a message...').fill('Hi there');
	await page.getByRole('button', { name: 'Send' }).click();

	await expect(page.locator('.user')).toContainText('Hi there');

	const botMessage = page.locator('.bot').last();
	await expect(botMessage).toContainText('Hello world');
	await expect(botMessage.locator('strong')).toHaveText('world');

	expect(captured).not.toBeNull();
	expect(captured!.body).toEqual({ message: 'Hi there' });
	expect(captured!.authorization).toMatch(/^Bearer\b/);
});
