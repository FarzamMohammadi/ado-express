<script>
  export let label;
  export let id;
  export let bindValue = false;
</script>

<div class="flex-row" on:click={() => bindValue = !bindValue} on:keypress={() => bindValue = !bindValue}>
  <div class="w-full flex justify-between items-center border-2 border-gray-200 rounded dark:border-gray-700 mt-2 mb-2" {id}>
    <label for={id} class="py-2 m-2 font-bold">{label}</label>
    <input bind:checked={bindValue} id="bordered-checkbox-1" type="checkbox" name={id} class="w-4 h-4 m-2 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
  </div>
</div>
