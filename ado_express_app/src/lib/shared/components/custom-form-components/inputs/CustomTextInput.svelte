<script>
  import { onMount } from 'svelte';
  import Tooltip from '../../utils/Tooltip.svelte';

  export let label;
  export let id;
  export let bindValue;
  export let required = true;
  export let showInput = true;

  let textarea;
  let expand = false;
  const textLengthToExtendAt = 40;

  onMount(() => {
    textarea.addEventListener('input', () => {
      const textLength = textarea.value.length;
      const threshold = textLengthToExtendAt;

      if (textLength >= threshold) {
        expand = true;
      } else {
        expand = false;
      }
    });
  });
</script>

{#if showInput}
<div class="input-field mb-4">
  <div class="flex items-center justify-between">
    <label for={id} class="font-bold mb-2">{label} </label>
    <Tooltip text="Top tooltip" position="right">
      <i class="mi mi-circle-information"><span class="sr-only">Circle information</span></i>
    </Tooltip>
  </div>

  <textarea
    {id}
    {required}
    rows="1"
    class="resize-none border-2 rounded p-2 w-full {expand
      ? 'h-24 transition-all duration-500 ease-in-out'
      : 'h-11'}  text-gray-900 text-sm rounded-lg focus:outline-none focus:border-blue-500 w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500"
    bind:value={bindValue}
    bind:this={textarea}
  />
</div>
{/if}