<script lang="ts">
  export let condition: Boolean;
</script>

{#if condition}
  <div><slot/></div>
{:else}
  <slot/>
{/if}