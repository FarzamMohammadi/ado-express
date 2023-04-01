<script>
  import Tooltip from '../utils/Tooltip.svelte';

  export let label;
  export let id;
  export let bindValue;
  export let required = false;
  export let showInput;
</script>

{#if showInput}
<div class="input-field mb-4">
  <div class="flex items-center justify-between">
    <label for={id} class="font-bold mb-2">{label} </label>
    <Tooltip text="Top tooltip" position="right">
      <i class="mi mi-circle-information"><span class="sr-only">Circle information</span></i>
    </Tooltip>
  </div>
  <input
    type="url"
    {id}
    {required}
    class="bg-gray-50 border-2 border-gray-300 text-gray-900 text-sm rounded-lg focus:outline-none focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    bind:value={bindValue}
  />
</div>
{/if}