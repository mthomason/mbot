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

			event.preventDefault();

			const response = await chatClient.postChatMessage();
			chatClient.messages = [...chatClient.messages,
					{ role: "user", content: chatClient.userChatPrompt }];
			chatClient.userChatPrompt = "";
			const reader = response.body?.getReader();
			if (reader === null || reader === undefined) {
				throw new Error("Reader is null or undefined.");
			}
			let chunks: string = "";
			const decoder = new TextDecoder("utf-8");
			let messageInMarkdownArray: string[] = [];

			while (true) {
				const { done, value } = await reader.read();
	
				chunks += decoder.decode(value);
				const endOfMessageIndex = chunks.indexOf("\n\n");

				if (endOfMessageIndex !== -1) {
					const messageString = chunks.slice(0, endOfMessageIndex);
					chunks = chunks.slice(endOfMessageIndex + 2);
					try {
						const data = JSON.parse(messageString);
						await displayBotMessageAsync(messageInMarkdownArray, data.choices[0].delta.content);
						if (data.choices[0].finish_reason === "stop") {
							console.log("Conversation ended");
							break;
						}
					} catch (e) {
						console.error('Error processing message chunk:', e);
					}
				}
				
				if (done) {
					if (chunks.length > 0) {
						const chunkArray = chunks.split("\n\n");
						for (const chunk of chunkArray) {
							if (chunk.trim() === '') continue;
							try {
								const data = JSON.parse(chunk);
								await displayBotMessageAsync(messageInMarkdownArray, data.choices[0].delta.content);
								if (data.choices[0].finish_reason === "stop") {
									console.log("Conversation ended");
								}
							} catch (e) {
								console.error('Error processing the final chunk:', e, 'Chunk:', chunk);
							}
						}
					}
					break;
				}
			}
			messageInMarkdownArray.length = 0;
		} catch (error) {
			console.error(error);
		}
	}

	function displayBotMessageAsync(chunks: string[], chunk: string) {
		if (chunk) {
			if (chatClient.messages[chatClient.messages.length - 1].role === "user") {
				chunks.push(chunk);
				chatClient.messages = [...chatClient.messages, { role: "bot", content: chunk },];
			} else {
				chunks.push(chunk);
				chatClient.messages[chatClient.messages.length - 1].content = markdownDecoder.render(chunks.join(""));
			}
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

<div id="chat-window"
	 class="w-full h-96 overflow-auto p-4 bg-gray-200 rounded-lg">
	{#each chatClient.messages as message, index (index)}
		<div class="{message.role}
					{`message p-2 mb-2 rounded-lg ${message.role === 'user' ?
						'bg-blue-400 text-white ml-auto' :
						'bg-gray-400 text-black mr-auto'}`}">
			<p class="prose">{@html message.content}</p>
		</div>
	{/each}
</div>

<div id="mbot-prompt" class="mt-4 flex items-center">
	<!--button class="input-group-shim bg-blue-500 text-white p-2 rounded-lg">
		+
	</button-->
	<textarea bind:value={chatClient.userChatPrompt}
			  on:keydown={handleKeyDown}
			  class="bg-transparent border-0 ring-0 flex-grow mx-2 p-2
						rounded-lg border-2 border-gray-200"
			  name="prompt"
			  id="prompt"
			  placeholder="Write a message..."
			  rows="1"
	/>
	<button class="variant-filled-primary bg-blue-500 text-white p-2
						rounded-lg"
			on:click={handleClick}>Send</button>
</div>

<style>
	.message {
		max-width: 80%;
		word-wrap: break-word;
	}
</style>
