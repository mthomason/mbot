<!-- /frontend/src/components/ChatWindow.svelte -->

<script>
	

	import { onMount } from "svelte";

	class ChatClient {
	constructor() {
		this.messages = [];
		this.newMessage = "";
	}

	/**
	 * Post a message to the chat server.
	 * @param {string} message
	 */
	async postChatMessage(message) {
		if (!this.newMessage) throw new Error("Message is empty");
		if (this.newMessage.length === 0) throw new Error("Message is empty");

		const response = await fetch("http://localhost:8000/chat", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ message: this.newMessage }),
			});
		return response;
	}

	/**
	 * Send a message to the chat server and process the response.
	 */
	/*
	async sendChatMessageAsync() {
		try {
			if (!this.newMessage) return;

			const response = await this.postChatMessage(this.newMessage);
			this.messages = [...this.messages, { role: "user", content: this.newMessage }];
			//this.newMessage = "";
			const reader = response.body.getReader();
			let chunks = "";
			while (true) {
				const { done, value } = await reader.read();
				if (done) break;
				chunks += new TextDecoder("utf-8").decode(value);
				const endOfMessageIndex = chunks.indexOf("\n\n");
				if (endOfMessageIndex !== -1) {
					const messageString = chunks.slice(0, endOfMessageIndex);
					chunks = chunks.slice(endOfMessageIndex + 2);
					const data = JSON.parse(messageString);
					const botMessage = data.choices[0].delta.content;
					if (botMessage) {
						if (this.messages[this.messages.length - 1].role === "user") {
							this.messages = [
								...this.messages,
								{ role: "bot", content: botMessage },
							];
						} else {
							this.messages[this.messages.length - 1].content += botMessage;
						}
						console.log(botMessage);
					}
					if (data.choices[0].finish_reason === "stop") {
						console.log("Conversation ended");
						break;
					}
				}
			}
		} catch (error) {
			console.error(error);
		}
	}
	*/

}
	
	let chatClient = new ChatClient();

	// Add the 'messages' variable with the new user or bot messages.
	/**
	 * @param {string} message
	 * @param {string} role
	 */
	function addChatMessages(message, role) {
		chatClient.messages = [...chatClient.messages, { role: role, content: message }, ];
	}

	// Update the 'messages' variable with the new user or bot messages.
	/**
	 ** @param {string} message
	 ** @param {string} role
	 **/
	function updateChatMessages(message, role) {
		if (chatClient.messages[chatClient.messages.length - 1].role !== role) {
			throw new Error("The last message is not from the same role");
		}
		chatClient.messages[chatClient.messages.length - 1].content += message;
	}

	// Decode chunks of data received from the server and find the end of each message.
	/**
     * @param {ReadableStreamDefaultReader<Uint8Array>} reader
     */
	async function decodeChunks(reader) {
		let chunks = "";
		let utf8Decoder = new TextDecoder("utf-8");

		while (true) {
			const { done, value } = await reader.read();
			if (done) break;

			chunks += utf8Decoder.decode(value);
			const endOfMessageIndex = chunks.indexOf("\n\n");

			if (endOfMessageIndex !== -1) {
				const messageString = chunks.slice(0, endOfMessageIndex);
				chunks = chunks.slice(endOfMessageIndex + 2);

				return { chunks, messageString };
			}
		}
	}
	
	// Process the data in each message, including updating the 'messages' variable and handling the 'stop' finish reason.
	/**
     * @param {number} index
     * @param {string} token
     */
	function processChatMessageData(index, token) {
		if (index === 0) {
			addChatMessages(token, "bot");
		} else {
			updateChatMessages(token, "bot");
		}
	}

	async function sendChatMessageAsync() {
		try {
			if (!chatClient.newMessage) return;

			const response = await chatClient.postChatMessage(chatClient.newMessage);
			chatClient.messages = [...chatClient.messages, { role: "user", content: chatClient.newMessage }];
			chatClient.newMessage = "";
			const reader = response.body.getReader();
			let chunks = "";
			while (true) {
				const { done, value } = await reader.read();
				if (done) break;
				chunks += new TextDecoder("utf-8").decode(value);
				const endOfMessageIndex = chunks.indexOf("\n\n");
				if (endOfMessageIndex !== -1) {
					const messageString = chunks.slice(0, endOfMessageIndex);
					chunks = chunks.slice(endOfMessageIndex + 2);
					const data = JSON.parse(messageString);
					const botMessage = data.choices[0].delta.content;
					if (botMessage) {
						if (chatClient.messages[chatClient.messages.length - 1].role === "user") {
							chatClient.messages = [
								...chatClient.messages,
								{ role: "bot", content: botMessage },
							];
						} else {
							chatClient.messages[chatClient.messages.length - 1].content += botMessage;
						}
						console.log(botMessage);
					}
					if (data.choices[0].finish_reason === "stop") {
						console.log("Conversation ended");
						break;
					}
				}
			}
		} catch (error) {
			console.error(error);
		}
	}

</script>

<div id="chat-window">
	{#each chatClient.messages as message, index (index)}
		<div class={message.role}>
			<p>{message.content}</p>
		</div>
	{/each}
</div>

<div id="message-input">
	<textarea bind:value={chatClient.newMessage} />
	<button on:click={async () => {
		await sendChatMessageAsync();
	}}>Send</button>
</div>

<style>
	:root {
		--color-primary: #4caf50;
		--color-secondary: #ffc107;
		--color-dark: #333;
		--color-light: #fff;
		--spacing-small: 10px;
		--spacing-medium: 20px;
		--spacing-large: 30px;
		--radius-small: 5px;
	}

	#chat-window {
		display: flex;
		flex-direction: column;
		max-width: 800px;
		height: 50vh; /*was 70vh; */
		margin: 0 auto var(--spacing-small) auto;
		padding: var(--spacing-medium);
		border-radius: var(--radius-small);
		background-color: var(--color-dark);
		color: var(--color-light);
		overflow: auto;
	}

	#message-input {
		display: flex;
		flex-direction: row;
	}

	.bot,
	.user {
		max-width: 70%;
		padding: var(--spacing-small);
		margin-bottom: var(--spacing-small);
		border-radius: var(--radius-small);
		color: var(--color-dark);
	}

	.bot {
		align-self: flex-start;
		background-color: var(--color-light);
	}

	.user {
		align-self: flex-end;
		background-color: var(--color-secondary);
		color: var(--color-dark);
	}

	textarea {
		padding: var(--spacing-small);
		border: none;
		border-radius: var(--radius-small);
		resize: none;
		overflow: auto;
		min-height: 5vh; /* Set minimum height */
		max-height: 20vh; /* Set maximum height */
		flex: auto;
	}

	button {
		padding: var(--spacing-small);
		border: none;
		border-radius: var(--radius-small);
		background-color: var(--color-primary);
		color: var(--color-light);
		cursor: pointer;
		transition: background-color 0.3s ease;
		margin: 0 var(--spacing-small) 0 var(--spacing-small);
	}

	button:hover {
		background-color: darken(var(--color-primary), 10%);
	}
</style>
