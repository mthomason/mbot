<!-- /frontend/src/components/ChatWindow.svelte -->

<script>
	import { onMount } from "svelte";
	let messages = [];
	let newMessage = '';

	onMount(async () => {
		try {
			const response = await fetch('http://localhost:8000/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ message: 'Hello!' })
			});
			const data = await response.json();
			messages = [...messages, { role: 'bot', content: data.response }];
			// messages.push({ role: 'bot', content: data.response });
		} catch (error) {
			console.error(error);
		}
	});
 
	/*
	async function sendMessage() {
		try {
			if (!newMessage) return;
			const response = await fetch('http://localhost:8000/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ message: newMessage })
			});

			const data = await response.json();
			messages = [...messages, { role: 'user', content: newMessage }];
			newMessage = '';
			messages = [...messages, { role: 'bot', content: data.response }];
		} catch (error) {
			console.error(error);
		}
	}
	*/

/*
	async function sendMessage() {
		try {
			if (!newMessage) return;
*/
			/*
			const response = await fetch('http://localhost:8000/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ message: newMessage })
			});
*/
			//const stream = new ReadableStream(getSomeSource());
/*
			const response = await fetch('http://localhost:8000/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ message: newMessage })
			});

			for await (const chunk of response.body) {
				// Do something with each chunk
				// Here we just accumulate the size of the response.
				//total += chunk.length;
			}
			*/
/*
			const reader = response.body.getReader();
			let chunks = '';
			let fullBotMessage = '';
			//do (await reader.read()).value
			//while (reader.read().done === false);

			let d = await reader.read();

			reader.read().then(({ done, value }) => {
				if (done) {
					console.log('Stream complete');
					return;
				}
				// value for fetch streams is a Uint8Array
				const chunk = new TextDecoder("utf-8").decode(value);
				console.log(chunk);
				// Do something with each 'chunk'
			});
*/				
/*
			while (true) {
				const { done, value } = await reader.read();
				if (done) break;



				chunks += new TextDecoder("utf-8").decode(value);

				// Let's assume the Python server returns complete JSON objects separated by a line break
				let jsonChunks = chunks.split('\n\n').filter(Boolean);

				let counter = 0;
				for (let chunk of jsonChunks) {
					let data;
					try {
						data = JSON.parse(chunk);
					} catch (error) {
						// If we can't parse chunk as JSON, it might be incomplete. We leave it in chunks for the next iteration.
						chunks = chunk;
						break;
					}

					const botMessage = data.choices[0].delta.content;

					if (botMessage) {
						fullBotMessage += botMessage;
					}

					//console.log('Conversation ended');
					//messages = [...messages, { role: 'user', content: newMessage }];
					//newMessage = '';
					if (counter == 0) {
						messages = [...messages,
							{ role: 'user', content: newMessage },
							{ role: 'bot', content: fullBotMessage }
						];
						newMessage = '';
					} else {
						messages[messages.length - 1].content += botMessage;
					}
					//messages = [...messages, { role: 'bot', content: fullBotMessage }];
					//console.log(fullBotMessage);
					//fullBotMessage = '';
					counter = counter + 1;
					if (data.choices[0].finish_reason === 'stop') {
						break;
					}
				}
			}
			*/
			/*
		} catch (error) {
			console.error(error);
		}
	}
*/

	async function sendMessage() {

		try {

			if (!newMessage) return;

			const response = await fetch('http://localhost:8000/chat', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ message: newMessage })
			});
		
			const reader = response.body.getReader();
			let chunks = '';
		
			while (true) {
				const { done, value } = await reader.read();
				if (done) break;

				chunks += new TextDecoder("utf-8").decode(value);
				const endOfMessageIndex = chunks.indexOf('\n\n');
			
				if (endOfMessageIndex !== -1) {
					const messageString = chunks.slice(0, endOfMessageIndex);
					chunks = chunks.slice(endOfMessageIndex + 2);
				
					const data = JSON.parse(messageString);
					const botMessage = data.choices[0].delta.content;
				
					if (botMessage) {
						messages = [...messages, { role: 'user', content: newMessage }];
						newMessage = '';
						messages = [...messages, { role: 'bot', content: botMessage }];
						console.log(botMessage);
					}
				
					if (data.choices[0].finish_reason === 'stop') {
						console.log('Conversation ended');
						break;
					}
				}
			}
		} catch (error) {
			console.error(error);
		}
	}

</script>

<style>
	:root {
		--color-primary: #4CAF50;
		--color-secondary: #FFC107;
		--color-dark: #333;
		--color-light: #FFF;
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

	.bot, .user {
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

<div id="chat-window">
	{#each messages as message, index (index)}
	<div class={message.role}>
		<p>{message.content}</p>
	</div>
	{/each}
</div>

<div id="message-input">
	<textarea bind:value={newMessage}></textarea>
	<button on:click={sendMessage}>Send</button>
</div>
