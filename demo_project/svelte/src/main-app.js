import App from './App.svelte';

const app = new App({
	target: document.getElementById("app-target"),
	props: JSON.parse(document.getElementById("app-props").textContent),
});

export default app;