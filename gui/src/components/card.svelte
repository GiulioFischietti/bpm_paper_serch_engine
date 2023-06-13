<script lang="ts">
  export let title: string;
  export let description: string;
  export let link: string;
  export let onSelectCallback: (l: string) => void;
  export let onDeselectCallback: (l: string) => void;
  export let initialSelected: boolean | undefined = undefined;

  let root: HTMLDivElement;
  $: selected = initialSelected ?? false;

  const modifyStatus = (value: string) => {
    console.log("entro qui");
    selected = !selected;
    selected && onSelectCallback(value);
    !selected && onDeselectCallback(value);
  };
</script>

<div bind:this={root} class:active={selected} class:card={!selected} on:click={() => modifyStatus(link)} on:keypress>
  <h2><a href={link} target="_blank">{title}</a></h2>
  <p>{description}</p>
  <input
    type="checkbox"
    value={link}
    checked={selected}
  />
</div>

<style>
  .card {
    position: relative;
    width: 100%;
    height: 100%;
    background-color: rgba(128, 128, 128, 0.5);
    backdrop-filter: blur(5px);
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    transition: all 0.4s;
    cursor: pointer;
  }
  h2 {
    margin-left: 2rem;
    margin-right: 2rem;
  }
  p {
    margin-left: 2rem;
    margin-right: 2rem;
  }
  input {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    width: 15px;
    height: 15px;
  }
  .active {
    position: relative;
    width: 100%;
    height: 100%;
    background-color: rgba(69, 183, 82, 0.5);
    backdrop-filter: blur(5px);
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    transition: all 0.4s;
    cursor: pointer;
  }
</style>
