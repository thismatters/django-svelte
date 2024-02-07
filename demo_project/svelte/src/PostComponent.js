import PostComponent from './components/PostComponent.svelte';

const postcomponent = new PostComponent({
	target: document.getElementById("postcomponent-target"),
	props: JSON.parse(document.getElementById("postcomponent-props").textContent),
});

export default postcomponent;