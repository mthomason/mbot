<!-- /frontend/src/components/ChatWindow.svelte -->

<script lang="ts">
	import { onMount, afterUpdate } from "svelte";
	import MarkdownIt from "markdown-it";
	import ChatClient from "../lib/ChatClient";

	let chatClient: ChatClient = new ChatClient();
	let chatWindowElement: HTMLTextAreaElement;
	const markdownDecoder: MarkdownIt = new MarkdownIt();

	/**
	 * @function sendChatMessageAsync
	 * @description
	 * Send a message to the chat server and receive a response.
	 * @param {Event} event
	 * @returns void
	 */
	async function sendChatMessageAsync(event: Event) {
		try {
			if (!chatClient.userChatPrompt) return;

			event.preventDefault(); // prevent form from refreshing the page

			const response = await chatClient.postChatMessage();
			chatClient.messages = [...chatClient.messages, { role: "user", content: chatClient.userChatPrompt }];
			chatClient.userChatPrompt = "";
			const reader = response.body?.getReader();
			if (reader === null || reader === undefined) {
				throw new Error("Reader is null or undefined.");
			}
			let chunks: string = "";
			const decoder = new TextDecoder("utf-8");
			let messageInMarkdown = "";
			while (true) {
				const { done, value } = await reader.read();

				chunks += decoder.decode(value);
				const endOfMessageIndex: number = chunks.indexOf("\n\n");

				if (endOfMessageIndex !== -1) {
					const messageString: string = chunks.slice(0, endOfMessageIndex);
					chunks = chunks.slice(endOfMessageIndex + 2);
					const data: any = JSON.parse(messageString);
					const botMessage: string = data.choices[0].delta.content;

					if (botMessage) {
						if (chatClient.messages[chatClient.messages.length - 1].role === "user") {
							chatClient.messages = [
								...chatClient.messages,
								{ role: "bot", content: botMessage },
							];
							messageInMarkdown = botMessage;
						} else {
							messageInMarkdown = messageInMarkdown += botMessage;
							chatClient.messages[chatClient.messages.length - 1].content = markdownDecoder.render(messageInMarkdown);
						}
						console.log(botMessage);
					}

					if (data.choices[0].finish_reason === "stop") {
						console.log("Conversation ended");
						break;
					}
				}
				if (done) break;
			
			}
		} catch (error) {
			console.error(error);
		}
	}

	/**
	 * @function handleKeyDown
	 * @description
	 * Send a message to the chat server and receive a response.
	 * @param {KeyboardEvent} event
	 * @returns void
	 */
	async function handleKeyDown(event: KeyboardEvent) {
		// keyCode 13 is the Enter key
		const key = event.key || String.fromCharCode(event.keyCode);
		if ((key === 'Enter' || key === '\n') && !event.shiftKey) {
			await sendChatMessageAsync(event);
		}
	}

	/**
	 * @function handleClick
	 * @description
	 * Send a message to the chat server and receive a response.
	 * @param {MouseEvent} event
	 * @returns void
	 */
	 async function handleClick(event: MouseEvent) {
		if (event.shiftKey) {
			chatClient.userChatPrompt += "\n";
		} else {
			await sendChatMessageAsync(event);
		}
	}

	/**
	 * @function scrollToBottom
	 * @description
	 * Scroll to the bottom of the chat window.
	 * @param void
	 * @returns void
	 */
	function scrollToBottom() {
		const chatWindow = document.getElementById('chat-window');
		if (chatWindow === null || chatWindow === undefined) return;
		chatWindow.scrollTop = chatWindow.scrollHeight;
	}

	/**
	 * @function onMount
	 * @description
	 * Run after the component mounts.
	 * @param void
	 * @returns void
	 */
	 onMount(() => {
		try {
			chatWindowElement.focus();
			chatWindowElement.scrollTop = chatWindowElement.scrollHeight;
		} catch (error) {
			console.error(error);
		}
	});

	/**
	 * @function afterUpdate
	 * @description
	 * Run after the component updates.
	 * @param void
	 * @returns void
	 */
	 afterUpdate(() => {
		try {
			scrollToBottom();
		} catch (error) {
			console.error(error);
		}
	});

</script>

<div id="chat-window">
	<!-- Display message stream. -->
	{#each chatClient.messages as message, index (index)}
		<div class={message.role}>
			<p>{@html message.content}</p>
		</div>
	{/each}
</div>

<form id="mbot-form">
	<textarea bind:this={chatWindowElement}
			  bind:value={chatClient.userChatPrompt}
			  on:keydown={handleKeyDown} />
	<button type="submit" on:click={handleClick}>Send</button>
</form>

<style>
	/* @import './ChatWindow.css'; */
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

#mbot-form {
	display: flex;
	flex-direction: row;
	max-width: 800px;
	margin: 0 auto var(--spacing-small) auto;
	padding: var(--spacing-medium);
	border-radius: var(--radius-small);
	/*background-color: var(--color-dark);*/
	color: var(--color-dark);
}

.bot,
.user {
	max-width: 70%;
	padding: var(--spacing-small);
	margin-bottom: var(--spacing-small);
	border-radius: var(--radius-small);
	color: var(--color-dark);
	text-align: left;
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
	min-height: 5vh;
	max-height: 20vh;
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
