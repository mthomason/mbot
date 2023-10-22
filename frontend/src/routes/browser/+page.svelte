<script lang="ts">
	// Function to gather browser information
	function getPropertyFromString(obj: Object, str: string) {
		return obj.hasOwnProperty(str) ? (obj as any)[str] : null;
	}
	function getBrowserInfo() {
		return {
			appCodeName: navigator.appCodeName,
			appName: navigator.appName,
			appVersion: navigator.appVersion,
			clipboard: navigator.clipboard,
			userAgent: navigator.userAgent,
			connection: getPropertyFromString(navigator, "connection"),
			contacts: getPropertyFromString(navigator, "contacts"),
			cookieEnabled: navigator.cookieEnabled,
			credentials: navigator.credentials,
			deviceMemory: getPropertyFromString(navigator, "deviceMemory"),
			doNotTrack: navigator.doNotTrack,
			geolocation: navigator.geolocation,
			globalPrivacyControl : getPropertyFromString(navigator, "globalPrivacyControl"),
			onLine: navigator.onLine,
			gpu: getPropertyFromString(navigator, "gpu"),
			pdfViewerEnabled: navigator.pdfViewerEnabled,
			plugins: navigator.plugins,
			serviceWorker: navigator.serviceWorker,
			storage: navigator.storage,
			scheduling: getPropertyFromString(navigator, "scheduling"),
			language: navigator.language,
			onlineStatus: navigator.onLine,
			screenHeight: window.screen.height,
			screenWidth: window.screen.width,
			viewportHeight: document.documentElement.clientHeight,
			viewportWidth: document.documentElement.clientWidth,
	  };
	}
  
	// Executing the function and storing the information in a variable
	let browserInfo = getBrowserInfo();
</script>

<!-- HTML to display the information -->
<svelte:head>
	<title>Browser Information</title>
</svelte:head>

<div>
	<h1>Browser Information</h1>
	<ul>
	  {#each Object.entries(browserInfo) as [key, value]}
		<li><strong>{key}:</strong> {value}</li>
	  {/each}
	</ul>
</div>

<style>
	div {
	  font-family: Arial, sans-serif;
	  margin: 0 auto;
	  padding: 20px;
	  max-width: 600px;
	}
	ul {
	  list-style: none;
	  padding: 0;
	}
	li {
	  margin: 10px 0;
	}
</style>
