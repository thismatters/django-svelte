<script>
import { get } from "../lib/api.js";
let isAuth = false;
let didClick = false;

async function handleClick() {
  console.log("clicked!");
  let res = await get("api/v1/requires-auth/");
  if (res.sgood) {
    isAuth = true;
  }
  didClick = true;
}
</script>

<h1>Check your auth status</h1>
<button on:click="{handleClick}">Check Auth!</button>
{#if isAuth}
  <h2>You're Auth!</h2>
{:else if didClick}
  <h2>You're not Auth!</h2>
{/if}


<style>
h1 {
  text-transform: uppercase;
  font-size: 4em;
  font-weight: 100;
}
</style>