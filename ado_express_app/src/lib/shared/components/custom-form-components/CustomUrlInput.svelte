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
    class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
    bind:value={bindValue}
  />
</div>
