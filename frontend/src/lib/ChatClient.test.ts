import { afterEach, describe, expect, it, vi } from 'vitest';
import ChatClient from './ChatClient';

describe('ChatClient', () => {
	let fetchMock: ReturnType<typeof vi.fn>;

	afterEach(() => {
		vi.unstubAllGlobals();
		vi.restoreAllMocks();
	});

	function useFetchMock() {
		fetchMock = vi.fn();
		vi.stubGlobal('fetch', fetchMock);
		return fetchMock;
	}

	it('rejects an empty prompt without calling fetch', async () => {
		const fetch = useFetchMock();
		const client = new ChatClient();

		await expect(client.postChatMessage()).rejects.toThrow('Message is empty');
		expect(fetch).not.toHaveBeenCalled();
	});

	it('posts the prompt and bearer token to the chat endpoint', async () => {
		const fetch = useFetchMock();
		const response = new Response('', { status: 200 });
		fetch.mockResolvedValue(response);

		const client = new ChatClient();
		client.userChatPrompt = 'Hello mbot';
		client.authIdToken = 'token-123';

		await expect(client.postChatMessage()).resolves.toBe(response);
		expect(fetch).toHaveBeenCalledWith('http://localhost:8000/chat', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: 'Bearer token-123'
			},
			body: JSON.stringify({ message: 'Hello mbot' })
		});
	});

	it('propagates network errors', async () => {
		const fetch = useFetchMock();
		const error = new Error('network down');
		fetch.mockRejectedValue(error);

		const client = new ChatClient();
		client.userChatPrompt = 'Hello';

		await expect(client.postChatMessage()).rejects.toThrow('network down');
	});
});
