<script lang="ts">
  import { onDestroy, onMount } from 'svelte';

  export let data = '';
  export let dotText;
  export let showIdleDots = false;

  let displayedText = '';
  let i = 0;

  let typeEffectTimeout: number;

  onMount(() => {
    typeEffect(data, 0, 15);
  });

  onDestroy(() => {
    clearTimeout(typeEffectTimeout);
  });

  function typeEffect(dataInput: string, index: number, delay: number) {
    if (index < dataInput.length) {
      typeEffectTimeout = setTimeout(() => {
        displayedText += dataInput[index];
        typeEffect(dataInput, index + 1, delay);
      }, delay);
    }
  }
</script>

<span>
  {displayedText}
  {#if showIdleDots}
    {dotText}
  {/if}
</span>
