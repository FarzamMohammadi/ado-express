<script>
  import { onMount } from 'svelte';
  import Tooltip from '../../utils/Tooltip.svelte';

  let expand = false;
  let invalid = false;
  let state = { focused: false };
  let textarea;
  const textLengthToExtendAt = 25;

  export let bindValue;
  export let id;
  export let isSubmitting = false;
  export let label;
  export let required;
  export let showInput = true;

  const handleBlur = () => (invalid = required && !bindValue);

  const handleFocus = () => (state.focused = true);

  const handleInput = () => {
    const textLength = textarea.value.length;
    invalid = required && textLength === 0;
    expand = textLength >= textLengthToExtendAt;
  };

  onMount(() => {
    textarea.addEventListener('input', handleInput);
  });

  $: if (isSubmitting && !state.focused && !bindValue) {
    invalid = required;
  }
</script>

{#if showInput}
  <div class="input-field mb-4">
    <div class="flex items-center justify-between">
      <label for={id} class={`font-bold mb-2 ${invalid ? 'text-red-500' : ''}`}>
        {label}
        {invalid ? '*' : ''}
      </label>

      <Tooltip text="Top tooltip" position="right">
        <i class="mi mi-circle-information">
          <span class="sr-only">Circle information</span>
        </i>
      </Tooltip>
    </div>

    <textarea
      id={id}
      required={required}
      rows="1"
      bind:value={bindValue}
      bind:this={textarea}
      on:focus={handleFocus}
      on:blur={handleBlur}
      class={`resize-none border-2 rounded p-2 w-full ${
        expand ? 'h-24 transition-all duration-500 ease-in-out' : 'h-11'
      } text-gray-900 text-sm rounded-lg focus:outline-none focus:border-blue-600 dark:focus:border-sky-500 w-full p-2.5 bg-gray-50 dark:bg-gray-700 dark:border-gray-600 border-gray-500 dark:text-white dark:focus:ring-blue-500 ${
        invalid ? 'invalid' : ''
      }`}
    />
  </div>
{/if}

<style lang="scss">
  .invalid {
    border-color: red;
    animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
    transform: translate3d(0, 0, 0);
    backface-visibility: hidden;
    perspective: 1000px;
  }

  @keyframes shake {
    10%,
    90% {
      transform: translate3d(-1px, 0, 0);
    }

    20%,
    80% {
      transform: translate3d(2px, 0, 0);
    }

    30%,
    50%,
    70% {
      transform: translate3d(-4px, 0, 0);
    }

    40%,
    60% {
      transform: translate3d(4px, 0, 0);
    }
  }
</style>
