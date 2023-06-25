<!-- /frontend/src/components/ChatWindow.svelte -->

<script>
	import { onMount } from "svelte";
	let messages = [];
	let newMessage = '';

	onMount(async () => {
		const response = await fetch('http://localhost:8000/chat', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ message: 'Hello!' })
		});
		const data = await response.json();
		messages.push({ role: 'bot', content: data.response });
	});
 
	async function sendMessage() {
		const response = await fetch('http://localhost:8000/chat', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ message: newMessage })
		});
		const data = await response.json();
		messages.push({ role: 'user', content: newMessage });
		newMessage = '';
		messages.push({ role: 'bot', content: data.response });
	}
</script>

<div id="chat-window">
	{#each messages as message (message)}
		<div class={message.role}>
			<p>{message.content}</p>
		</div>
	{/each}
</div>

<input bind:value={newMessage} type="text">
<button on:click={sendMessage}>Send</button>
