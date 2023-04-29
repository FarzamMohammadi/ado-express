<script>
  import { onMount } from 'svelte';
  import Tooltip from '../../utils/Tooltip.svelte';

  export let label;
  export let id;
  export let bindValue;
  export let required = true;
  export let showInput = true;
  export let isSubmitting = false;

  let invalid = false;
  let textarea;
  let expand = false;
  const textLengthToExtendAt = 25;

  let state = {
    focused: false
  };

  function handleFocus() {
    state.focused = true;
  }

  function handleBlur() {
    invalid = required && !bindValue;
  }

  onMount(() => {
    textarea.addEventListener('input', () => {
      const textLength = textarea.value.length;
      const threshold = textLengthToExtendAt;
      invalid = required && textLength === 0;

      if (textLength >= threshold) {
        expand = true;
      } else {
        expand = false;
      }
    });
  });

  $: if (isSubmitting && !state.focused && !bindValue) {
    invalid = required;
  }
</script>


{#if showInput}
<div class="input-field mb-4">
  <div class="flex items-center justify-between">
    <label for={id} class="font-bold mb-2 {invalid ? 'text-red-600' : ''}">{label} {invalid ? '*' : ''} </label>
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
      : 'h-11'}  text-gray-900 text-sm rounded-lg focus:outline-none focus:border-blue-600 dark:focus:border-sky-500 w-full p-2.5 bg-gray-50 dark:bg-gray-700 border-gray-500 dark:text-white dark:focus:ring-blue-500 {invalid ? 'invalid' : ''}"
    on:focus={handleFocus}
    on:blur={handleBlur}
    bind:value={bindValue}
    bind:this={textarea}
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
