<script>
import { post } from "./api.js";

let fakeInput = "";
let res = null;

async function handleClick() {
  res = await post("api/v1/requires-auth/", {input: fakeInput})
}
</script>


<input type="text" name="fake-input" bind:value="{fakeInput}" />
<button on:click="{handleClick}">POST it</button>
{#if res}
  {res.sgood ? "Sgood" : "Sbad"}
  {res.did_post ? "did post!" : "didn't post :("}
{/if}