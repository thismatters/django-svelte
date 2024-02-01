<script>
import { post } from "./api.js";

let fakeInput = "";
let res = null;

async function handleClick() {
  res = await post("api/v1/requires-auth/", {input: fakeInput})
}
</script>

<h1>POST something. make it good.</h1>

<input type="text" name="fake-input" bind:value="{fakeInput}" />
<button on:click="{handleClick}">POST it</button>
{#if res}
  <h2>{res.sgood ? "Good" : "Bad"}
  {res.did_post ? "did post!" : "didn't post :("}</h2>
{/if}