<script lang="ts">
  import type { CardContent } from "../../models/models";
  import Rollerloader from "../../components/rollerloader.svelte";
  import DuckNavigation from "../../assets/duck_navigation.png";
  import DisabledNavigation from "../../assets/duck_navigation_disabled.png";
  import Card from "../../components/card.svelte";
  import { urlString } from "../../store";
  
  $: currentPage = 0;
  $: queryString = $urlString?.searchParams?.get("query") ?? "";
  
  let currentList: CardContent[] = [];
  const initialList: string[] = [];

  $: selectedList = initialList;

  export let data: {pyApi: string};

  const cardSelect = (l: string): boolean => {
    if(selectedList.length >= 4) return false;
    selectedList = selectedList.concat(l);
    return true;
  };
  const cardDeselect = (l: string)=> {
    selectedList = selectedList.filter((sl) => sl !== l);
  };

  const getList = async (query: string, page: number): Promise<CardContent[]> => {
    const response: CardContent[] = await (
      await fetch(`${data.pyApi}/search?query=${query}&page=${page}`, {
        method: "GET",
        mode: "cors",
        headers: {
          accept: "application/json",
        },
      })
    ).json();
    currentList = response.map(l => l);
    return currentList;
  };
</script>

<div class="cardsContainer">
  {#await getList(decodeURIComponent(queryString), currentPage)}
    <Rollerloader />
  {:then results}
    {#each results as result}
      <Card
        {...result}
        onSelectCallback={cardSelect}
        onDeselectCallback={cardDeselect}
        initialSelected={selectedList.includes(result.link)}
      />
    {/each}
  {:catch error}
    <h1 style="color: red;">
      Failed to load results: {`${error?.code ?? 500}: ${
        error?.message ?? "Internal Server Error"
      }`}
    </h1>
  {/await}
</div>
<div class="footer">
  <img
    src={currentPage > 0 ? DuckNavigation : DisabledNavigation}
    alt="Prev Page"
    height="48px"
    on:click={currentPage > 0 ? () => currentPage-- : () => {}}
    on:keypress
    class:disabled={currentPage <= 0}
  />
  {currentPage}
  <img
    src={currentList.length > 0 ? DuckNavigation : DisabledNavigation}
    alt="Next Page"
    height="48px"
    on:click={currentList.length > 0 ? () => currentPage++ : () => {}}
    on:keypress
    class:disabled={currentList.length <= 0}
  />
</div>
<div class="counter">Selected: {selectedList.length}/4</div>

<style>
  :root {
    --navbar-heigth: 7rem;
    --footbar-height: 3rem;
  }
  .counter{
    position: fixed;
    bottom: 1.3%;
    right: 3.4%;
    font-size: 11px;
  }
  .disabled{
    pointer-events: none;
  }
  .cardsContainer {
    margin-top: var(--navbar-heigth);
    display: grid;
    grid-template-columns: auto auto auto;
    gap: 2rem;
    height: calc(100vh - var(--navbar-heigth) - 0.5rem);
    margin-left: 2rem;
    margin-right: 3rem;
    overflow: hidden;
    overflow-y: auto;
    height: 470px;
    column-gap: 2rem;
  }
  .footer {
    position: fixed;
    bottom: 2rem;
    width: calc(100% - 4rem);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5rem;
    user-select: none;
  }
  .footer > img {
    cursor: pointer;
  }
  .footer > img:nth-child(2) {
    transform: scaleX(-1);
  }
  @media screen and (max-width: 800px) {
    .cardsContainer {
      grid-template-columns: auto auto;
      margin-left: 1.5rem;
    }
  }
  @media screen and (max-width: 500px) {
    .footer {
      justify-content: start;
      gap: 0.5rem;
    }
    .cardsContainer {
      grid-template-columns: auto;
      margin-left: 0.5rem;
      margin-right: 0.5rem;
    }
  }
</style>
