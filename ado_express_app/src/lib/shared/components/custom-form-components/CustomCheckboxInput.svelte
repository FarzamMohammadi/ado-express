<script>
  export let label;
  export let id;
  export let bindValue;
</script>

<div class="explicit-release-values flex-row mb-4">
  <div class="flex justify-between mb-3">
    <label for="explicitReleaseValues" {id} class="font-bold">{label}</label>
    <input type="checkbox" bind:checked={bindValue} />
  </div>
</div>
