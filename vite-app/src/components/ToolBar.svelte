<!-- /frontend/src/components/ToolBar.svelte -->
<script>
	import { onMount, onDestroy } from 'svelte';
	import { login, logout, authentication } from '../stores/auth.store'

	let user = null;

	const unsubscribe = authentication.subscribe((value) => {
		user = value;
	});

	onDestroy(() => {
		unsubscribe();
	});
</script>

<nav class="toolbar">
	<div class="placeholder"></div>
{#if user}
	<div class="items-center space-x-2 hidden xl:inline-flex">
		<div class="avatar-container">
			<img src={user?.photoURL}
				 alt={user?.displayName}
				 class="h-12 w-12 avatar circle" />
			<div class="avatar-tooltip">
				<p>{user?.displayName}</p>
				<p>{user?.email}</p>
				<p>Logged in with Google</p>
				<button on:click={logout} class="logout-button">Logout</button>
			</div>
		</div>
	</div>
{:else}
	<button on:click={login} class="login-button">Login with Google</button>
{/if}
</nav>

<style>
/*General Styles*/
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
}

.placeholder {
	flex-grow: 1;
}

.avatar-container {
	position: relative;
	cursor: pointer;
}

/*Avatar Styles*/
.avatar.circle {
	width: 32px;
	height: 32px;
	border-radius: 50%;
	object-fit: cover;
}

/*Tooltip Styles*/
.avatar-tooltip {
	display: none;
	position: absolute;
	background-color: #333;
	color: #fff;
	padding: 15px;
	border-radius: 10px;
	top: 100%;
	right: 0;
	transform: translateY(10px);
	width: 200px;
	z-index: 1;
	box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
}

.avatar-tooltip p {
	margin-bottom: 10px;
}

.avatar-tooltip::after {
	content: '';
	position: absolute;
	top: 0;
	right: 15px;
	border-width: 5px;
	border-style: solid;
	border-color: #333 transparent transparent transparent;
}

.avatar-container:hover .avatar-tooltip, 
.avatar-container:active .avatar-tooltip {
	display: block;
}

/*Button Styles*/
.logout-button, .login-button {
	padding: 10px 20px;
	border: none;
	border-radius: 4px;
	color: #fff;
	cursor: pointer;
	transition: all 0.3s ease;
}

.logout-button {
	background-color: #f44336; /* Red */
}

.logout-button:hover {
	background-color: #d32f2f;
}

.login-button {
	background-color: #4285F4; /* Google Blue */
}

.login-button:hover {
	background-color: #3367d6;
}

@media screen and (max-width: 768px) {
	.items-center {
		flex-direction: column;
	}
}
</style>
