<!-- /frontend/src/routes/about/+page.svelte -->

<div class="container p-10 space-y-4">
	<header class="bg-secondary p-4 flex justify-between items-center">
		<h2 class="h2 font-sans font-bold text-sm md:text-2xl tracking-widest">About</h2>
	</header>
	<main class="space-y-4">
		<div>
			<h3 class="h3">Overview</h3>
			<p>
				<strong>mbot</strong> is an open-source starter project for building AI-powered chatbot applications. Combining a modern tech stack of <strong>Svelte</strong> for the frontend and <strong>FastAPI</strong> for the backend, it provides Firebase authentication and integrates seamlessly with OpenAI APIs.
			</p>
			<p>
				This project is designed for:
			</p>
			<ul class="list-disc list-inside mt-2">
				<li><strong>AI startup enthusiasts</strong> building chat applications.</li>
				<li><strong>Developers</strong> exploring Svelte and FastAPI.</li>
				<li><strong>Hobbyists</strong> experimenting with OpenAI's GPT models.</li>
			</ul>
		</div>
		<div>
			<h3 class="h3">Features</h3>
			<ul class="list-disc list-inside mt-2">
				<li>Modern Frontend: Built with SvelteKit for reactive UI.</li>
				<li>FastAPI Backend: Async API integration with OpenAI.</li>
				<li>Secure Authentication: Firebase for user authentication.</li>
				<li>Boilerplate for AI Apps: A great foundation for interactive AI chat solutions.</li>
			</ul>
		</div>
		<div>
			<h3 class="h3">Source Code</h3>
			<p>
				The source code for this project is available on GitHub:
				<a href="https://github.com/mthomason/mbot" target="_blank" class="text-primary-500 hover:underline">https://github.com/mthomason/mbot</a>
			</p>
		</div>
	</main>
</div>
