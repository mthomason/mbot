<!-- /frontend/src/components/TestChatDisplay.svelte -->

<script lang="ts">
	import { onMount, afterUpdate } from "svelte";
	import ChatClient from "./ChatClient";
	import MarkdownIt from "markdown-it";

	let chatClient: ChatClient = new ChatClient();
	let chatWindowElement: HTMLTextAreaElement;

	const markdownDecoder = new MarkdownIt();

	function scrollToBottom() {
		const chatWindow = document.getElementById('chat-window');
		chatWindow.scrollTop = chatWindow.scrollHeight;
	}

	/**
	 * Run after the component mounts.
	 * @param void
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
	 * Run after the component updates.
	 * @param void
	 */
	afterUpdate(() => {
		scrollToBottom();
	});

	function isString(value) {
		if (typeof value === 'string' && value !== null) {
			return true;
		} else {
			return false;
		}
	}

	/**
	 * Send a message to the chat server and receive a response.
	 * @param {Event} event
	 */
	 async function sendChatMessageAsync(event: Event) {
		try {
			if (!chatClient.userChatPrompt) return;

			event.preventDefault(); // prevent form from refreshing the page

			const response = await chatClient.postChatMessage();
			chatClient.messages = [...chatClient.messages,
					{ role: "user", content: chatClient.userChatPrompt }];
			
			//chatClient.userChatPrompt = "";

			const reader = response.body.getReader();
			let chunks = "";

			const textDecoder: TextDecoder = new TextDecoder("utf-8");
			//const messageBuilder: MessageBuilder = new MessageBuilder();

			//const botBlockMessageLog = [""];
			//const botBlockLog = [botBlockMessageLog];

			while (true) {
				const { done, value } = await reader.read();
				if (done) break;
				chunks += textDecoder.decode(value);
				const endOfMessageIndex = chunks.indexOf("\n\n");

				if (endOfMessageIndex !== -1) {
					
					const messageString = chunks.slice(0, endOfMessageIndex);
					chunks = chunks.slice(endOfMessageIndex + 2);
					const data = JSON.parse(messageString);
					const botMessage = data.choices[0].delta.content;

					if (isString(botMessage)) {

						//messageBuilder.addToken(botMessage);
						//console.log(`Block Count: ${messageBuilder.getBlockCount()}`);
						//console.log(`Last Block Html: '${messageBuilder.getBlockHtml()}'`);
						//botBlockMessageLog.push(botMessage);

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
			//let messageHtml = messageBuilder.getHtml();
			//console.log(`Message Html: '${messageHtml}'`);
		} catch (error) {
			console.error(error);
		}
	}

	/**
	 * Send a message to the chat server and receive a response.
	 * @param {KeyboardEvent} event
	 */
	 async function handleKeyDown(event: KeyboardEvent) {
		// keyCode 13 is the Enter key
		const key = event.key || String.fromCharCode(event.keyCode);
		if ((key === 'Enter' || key === '\n') && !event.shiftKey) {
			await sendChatMessageAsync(event);
		}
	}

	/**
	 * Send a message to the chat server and receive a response.
	 * @param {MouseEvent} event
	 */
	 async function handleClick(event: MouseEvent) {
		if (event.shiftKey) {
			chatClient.userChatPrompt += "\n";
		} else {
			await sendChatMessageAsync(event);
		}
	}


</script>

<div id="chat-window">

	<!-- Display message stream in HTML. -->
	<!--
	{#each chatClient.messages as message, index (index)}
		<div class={message.role}>
			{#if message.role === "user"}
				<p>
					{message.content}
				</p>
			{:else if message.role === "bot"}
				{#each chatClient.messagesFormatted[index] as block, index (index)}
					<p>
						{@html block}
					</p>
				{/each}
			{/if}
		</div>
	{/each}
	-->

	<!-- Display message stream. -->
	{#each chatClient.messages as message, index (index)}
		<div class={message.role}>
			<p>{@html markdownDecoder.render(message.content)}</p>
		</div>
	{/each}

</div>

<form id="mbot-form" on:keydown={handleKeyDown}>
	<textarea bind:this={chatWindowElement}
			  bind:value={chatClient.userChatPrompt} />
	<button type="submit" on:click={handleClick}>Send</button>
</form>

<style>
	@import './ChatWindow.css';
</style>
