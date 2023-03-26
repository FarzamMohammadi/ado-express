<script>
  import { onMount } from 'svelte';

  export let label;
  export let id;
  export let bindValue;

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

<div class="input-field mb-4">
  <label for={id} class="font-bold mb-2">{label}</label>
  <textarea
    bind:this={textarea}
    rows="1"
    class="resize-none transition-all duration-500 ease-in-out border-2 rounded p-2 w-full {expand
      ? 'h-24'
      : 'h-11'} bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    {id}
    bind:value={bindValue}
  />
</div>
