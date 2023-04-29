<script>
    import Tooltip from '../../utils/Tooltip.svelte';

  export let label;
  export let id;
  export let bindValue;
  export let required;
  export let showInput;
  export let isSubmitting;

  let invalid = false;

  function checkInputValidity() {
    if (required) {
      try {
        new URL(bindValue);
      } catch (_) {
        invalid = true;
        return;
      }
    }

    invalid = false;
  }

  $: if (isSubmitting) {
    checkInputValidity();
  }
</script>

{#if showInput}
<div class="input-field mb-4">
  <div class="flex items-center justify-between">
    <label for={id} class="font-bold mb-2 {invalid ? 'text-red-500' : ''}">{label} {invalid ? '*' : ''}</label>
    <Tooltip text="Top tooltip" position="right">
      <i class="mi mi-circle-information"><span class="sr-only">Circle information</span></i>
    </Tooltip>
  </div>
  <input
    type="url"
    {id}
    {required}
    class="bg-gray-50 border-2 text-gray-900 text-sm rounded-lg focus:outline-none focus:border-blue-600 dark:focus:border-sky-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 {invalid ? 'invalid' : ''}"
    on:blur={checkInputValidity}
    bind:value={bindValue}
  />
</div>
{/if}

<style lang="scss">
  .invalid {
    border-color: red;
    animation: shake 0.82s cubic-bezier(.36,.07,.19,.97) both;
    transform: translate3d(0, 0, 0);
    backface-visibility: hidden;
    perspective: 1000px;
  }

  @keyframes shake {
    10%, 90% {
      transform: translate3d(-1px, 0, 0);
    }
    
    20%, 80% {
      transform: translate3d(2px, 0, 0);
    }

    30%, 50%, 70% {
      transform: translate3d(-4px, 0, 0);
    }

    40%, 60% {
      transform: translate3d(4px, 0, 0);
    }
  }
</style>