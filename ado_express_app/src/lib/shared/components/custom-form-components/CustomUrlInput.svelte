<script>
  export let label;
  export let id;
  export let bindValue;
</script>

<div class="input-field mb-4">
  <label for={id} class="font-bold mb-2">{label}</label>
  <input
    type="url"
    {id}
    class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    bind:value={bindValue}
  />
</div>
