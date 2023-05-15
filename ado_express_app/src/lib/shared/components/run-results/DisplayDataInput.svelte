<script lang="ts">
    export let data = '';
  export let showIdleDots = false;
  export let dotText;

  let displayedText = '';
  let i = 0;

  $: {
    displayedText = '';
    typeEffect(data, 0, 15);
  }

  function typeEffect(dataInput: string, i: number, delay: number) {
    if (i < dataInput.length) {
      setTimeout(() => {
        displayedText += dataInput[i];
        typeEffect(dataInput, i + 1, delay);
      }, delay);
    }
  }
</script>

<span>
  {displayedText}
  {#if showIdleDots}{dotText}{/if}
</span>