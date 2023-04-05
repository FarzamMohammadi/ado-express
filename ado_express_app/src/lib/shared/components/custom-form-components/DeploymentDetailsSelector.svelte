<script lang="ts">
  import { onMount } from 'svelte';
  import ExcelFileInput from './ExcelFileInput.svelte';
  import ExcelPatternSelector from './ExcelPatternSelector.svelte';

  export let deploymentDetails;
  export let deploymentSelectorHeaders: string[] = [];
  export let showInput: boolean;
  let deploymentDetailsType = 'file';
  let customDeploymentDetailsSelector;

  onMount(() => {
    // Perform any initialization or setup here
  });
</script>

{#if showInput}
  <div
    class="min-w-full border-2 border-gray-200 rounded dark:border-gray-700 mt-2 mb-2 p-2 mx-4"
    id="deploymentDetails"
  >
    <label for="deploymentDetails" class="font-bold text-gray-900"
      >Deployment Details</label
    >

    <div class="pb-2 pt-2 text-gray-900">
      <label class="pr-3">
        <input
          type="radio"
          name="deploymentDetailsType"
          value="file"
          bind:group={deploymentDetailsType}
        />
        Excel File
      </label>

      <label>
        <input
          type="radio"
          name="deploymentDetailsType"
          value="custom"
          bind:group={deploymentDetailsType}
        />
        Manual Input
      </label>
    </div>

    {#if deploymentDetailsType === 'custom'}
      <div class="p-2">
        <ExcelPatternSelector
          rows={4}
          headers={deploymentSelectorHeaders}
          bind:this={customDeploymentDetailsSelector}
        />
      </div>
    {:else if deploymentDetailsType === 'file'}
      <div class="p-2">
        <ExcelFileInput bind:deploymentDetails />
      </div>
    {/if}
  </div>
{/if}
