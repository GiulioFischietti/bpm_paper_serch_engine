<script lang="ts">
  import { page } from "$app/stores"
  import { goto } from "$app/navigation"
  import Conditionalwrapper from "../components/conditionalwrapper.svelte";
  import DuckIcon from "../assets/main-icon.ico"
  
  let input: HTMLInputElement;
  let queryString: string = "";
  
  const enterPressed = () => {
    queryString = encodeURIComponent(queryString ?? "");
    goto(`/paperselect?query=${queryString}`);
  }

  const focusInput = () => {
    input.focus();
  }

  $: isLandingPage = $page.url.pathname === "/";

  
</script>

<style>
  .landing{
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 70vh;
    place-items: center;
    place-content: center;
    gap: 4rem;
  }
  .inputwrapper{
    padding: 1rem;
    border-radius: 4rem;
    border: 2px solid black;
    display: flex; 
    justify-content: center;
    align-items: center;
    cursor: text;
  }
  .inputwrapper > input {
    width: 100%;
    outline: none;
    border: none;
    pointer-events: none;
  }
  .inputwrapper > div{
    font-size: larger;
  }
  .landing > .inputwrapper{
    width: 50%;
  }
  .navbar{
    position: fixed;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;  
    top: 0;
    width: 100%;
    height: 5rem;
  }
  .navbar > img{
    width: 2.5rem;
    height: 2.5rem;
  }
</style>

<div class:landing={isLandingPage} class:navbar={!isLandingPage}>
  {#if isLandingPage}
  <div style="display: flex; flex-direction: column; justify-content:center; align-items: center">
    <img src={DuckIcon} alt="PaperAI">
    <h1>PaperAI</h1>
  </div>
  {/if}
  <Conditionalwrapper condition={!isLandingPage}>
  <div class="inputwrapper" on:click={() => focusInput()} on:keypress>
    <input 
      type="text" 
      placeholder="search" 
      bind:value={queryString} 
      bind:this={input}
      on:keypress={(event) => event.key === "Enter" && enterPressed()}>
      <div style="cursor: pointer;" on:click={() => enterPressed()} on:keypress>🔍</div>
  </div>
  </Conditionalwrapper>
  {#if !isLandingPage}
    <img src={DuckIcon} alt="PaperAI">
  {/if}
</div>

<slot></slot>