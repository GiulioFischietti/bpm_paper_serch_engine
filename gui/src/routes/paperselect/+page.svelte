<script lang="ts">
  import { documentResults } from "../../assets/mockups";
  import type { CardContent } from "../../models/models";
  import Rollerloader from "../../components/rollerloader.svelte";
  import DuckNavigation from "../../assets/duck_navigation.png";
  import Card from "../../components/card.svelte";
  import { urlString } from "../../store";

  $: currentPage = 0;
  $: queryString = $urlString?.searchParams?.get("query") ?? "";

  let currentList: CardContent[] = [];

  const getList = async (query: string, page: number): Promise<CardContent[]> => {
    /**@todo: add GET with pagination and find a way to re-trigger this function on href change */
    console.log("entro qui", { query, page });
    const startIndex = page >= 0 ? page * 6 : 0;
    documentResults.forEach((d) => (d.title = query));
    currentList = documentResults.filter((d) => true).slice(startIndex, startIndex + 6);
    return currentList;
  };
</script>

<div class="cardsContainer">
  {#await getList(queryString, currentPage)}
    <Rollerloader />
  {:then results}
    {#each results as result}
      <Card {...result} />
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
    src={DuckNavigation}
    alt="Prev Page"
    height="48px"
    on:click={currentPage > 0 ? () => currentPage-- : () => {}}
    on:keypress
  />
  {currentPage}
  <img
    src={DuckNavigation}
    alt="Next Page"
    height="48px"
    on:click={currentList.length > 0 ? () => currentPage++ : () => {}}
    on:keypress
  />
</div>

<style>
  :root {
    --navbar-heigth: 7rem;
    --footbar-height: 3rem;
  }
  .cardsContainer {
    margin-top: var(--navbar-heigth);
    display: grid;
    grid-template-columns: auto auto auto;
    gap: 2rem;
    height: calc(100vh - var(--navbar-heigth) - 0.5rem);
    margin-left: 2rem;
    margin-right: 1.5rem;
    overflow: hidden;
    overflow-y: auto;
    height: 470px;
    column-gap: 5rem;
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
