<script lang="ts">
  export let title: string; 
  export let description: string; 
  export let link: string;
</script>

<style>
  .card{
    width: 100%;
    height: 100%;
  }
</style>

<div class="card">
  <h2><a href={link} target="_blank">{title}</a></h2>
  <p>{description}</p>
</div>