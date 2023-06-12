<script lang="ts">
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import DuckIcon from "../assets/main-icon.ico";
  import AudioQuack from "../assets/quack.mp3";
  import { urlString } from "../store";
  import { onMount } from "svelte";

  let input: HTMLInputElement;
  let queryString: string = "";
  const quack = typeof Audio !== "undefined" && new Audio(AudioQuack);

  const enterPressed = () => {
    const resultQueryString = encodeURIComponent(queryString ?? "");
    const currentUrl = new URL(window.location.href);
    currentUrl.pathname = "/paperselect";
    currentUrl.searchParams.set("query", resultQueryString);
    urlString.set(new URL(currentUrl));
    goto(currentUrl);
  };

  const buildSummary = () => {
    quack && quack.play();
  };

  const focusInput = () => {
    input.focus();
  };

  onMount(() => {
    const handlePopState = () => {
      const urlState = new URL(window.location.href);
      if (urlState.pathname === "/paperselect") {
        input.value = decodeURIComponent(urlState?.searchParams?.get("query") ?? "");
        urlString.set(urlState);
      }
    };

    handlePopState();
    window.addEventListener("popstate", handlePopState);

    return () => {
      window.removeEventListener("popstate", () => {});
    };
  });

  $: isLandingPage = $page.url.pathname === "/";
</script>

<slot />
<div class:landing={isLandingPage} class:navbar={!isLandingPage}>
  <div class="iconContainer">
    <img
      src={DuckIcon}
      alt="PaperAI"
      on:click={!isLandingPage ? () => buildSummary() : () => {}}
      on:keypress
    />
    <p>{isLandingPage ? "PaperAI" : "Build Summary"}</p>
  </div>
  <div class="inputwrapper" on:click={() => focusInput()} on:keypress>
    <input
      type="text"
      placeholder="search"
      bind:value={queryString}
      bind:this={input}
      on:keypress={(event) => event.key === "Enter" && enterPressed()}
    />
    <div style="cursor: pointer;" on:click={() => enterPressed()} on:keypress>🔍</div>
  </div>
</div>

<style>
  .landing {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 70vh;
    place-items: center;
    place-content: center;
    gap: 4rem;
    transition: all 0.4s;
  }
  .inputwrapper {
    padding: 1rem;
    border-radius: 4rem;
    border: 2px solid rgb(77, 0, 100);
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: text;
    background: white;
  }
  .inputwrapper > input {
    width: 100%;
    outline: none;
    border: none;
    background: none;
  }
  .inputwrapper > div {
    font-size: larger;
  }
  .landing > .inputwrapper {
    width: 50%;
    box-shadow: 0px 0px 49px -3px rgb(44, 44, 44);
  }
  .landing > .iconContainer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .landing > .iconContainer > p {
    font-size: 24px;
    font-weight: 900;
    margin: 0;
  }
  .navbar {
    position: fixed;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    top: 0;
    width: 100%;
    height: 5rem;
    transition: all 0.4s;
  }
  .navbar > .iconContainer {
    position: fixed;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    bottom: 2rem;
    right: 2rem;
    cursor: pointer;
    z-index: 12;
  }
  .navbar > .inputwrapper {
    width: 45%;
    box-shadow: 0px 0px 49px -3px rgb(44, 44, 44);
  }
  .navbar > .iconContainer > img {
    width: 4rem;
    height: 4rem;
    gap: 0px;
  }
  .navbar > .iconContainer > p {
    font-weight: bolder;
    margin: 0;
    pointer-events: none;
  }
</style>
