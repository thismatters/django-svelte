import AuthComponent from './components/AuthComponent.svelte';

const authcomponent = new AuthComponent({
	target: document.getElementById("authcomponent-target"),
	props: JSON.parse(document.getElementById("authcomponent-props").textContent),
});

export default authcomponent;