<script>
  export let bindValue = false;
  export let id;
  export let label;
  export let showInput;

  const toggleValue = () => (bindValue = !bindValue);
</script>

{#if showInput}
  <div class="flex-row" on:click={toggleValue} on:keypress={toggleValue}>
    <div class="w-full flex justify-between items-center border-2 border-gray-200 rounded dark:border-gray-700 mt-2 mb-2" id={id}>
      <label for={id} class="py-2 m-2 font-bold">{label}</label>

      <input
        bind:checked={bindValue}
        id={id}
        type="checkbox"
        name={id}
        class="w-4 h-4 m-2 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
      />
    </div>
  </div>
{/if}
