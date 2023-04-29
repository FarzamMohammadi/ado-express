<script lang="ts">
  import { clickOutside } from '../../../../utils/click-outside';
  import Tooltip from '../../utils/Tooltip.svelte';
  import ExcelFileInput from './ExcelFileInput.svelte';
  import ExcelPatternSelector from './ExcelPatternSelector.svelte';

  export let deploymentSelectorHeaders: string[] = [];
  export let showInput: boolean;
  export let showCustomSelector = false;
  let customDeploymentDetailsSelector;
  let showingDeploymentDetailsReadOnlySelection = true;

  function handleClickOutside() {
    showingDeploymentDetailsReadOnlySelection = false;
    showCustomSelector = false;
  }

  function handleClickInside() {
    showingDeploymentDetailsReadOnlySelection = true;
    showCustomSelector = true;
  }

  function handleExcelDeploymentDetailsUpload() {
    customDeploymentDetailsSelector.setDeploymentDetailsValuesToTable();
  }
</script>

{#if showInput}
  <div
    class="w-full border-2 rounded border-gray-600 dark:border-gray-500 mt-2 mb-3 p-2 mx-4"
    id="$deploymentDetails"
    use:clickOutside on:click_outside={handleClickOutside}
    on:click={handleClickInside}
    on:keypress={handleClickInside}
  >
    <div class="flex justify-center ml-3">
      <label
        for="$deploymentDetails"
        class="font-bold text-gray-900 dark:text-white mt-2 mr-1"
        >Deployment Details</label
      >

      <Tooltip text="Top tooltip" position="right">
        <i class="mi mi-circle-information text-gray-900 dark:text-white"
          ><span class="sr-only">Circle information</span></i
        >
      </Tooltip>
    </div>

    <!-- {#if !$running} -->
      {#if showCustomSelector}
        <div class="p-2 mt-2 read-only">
          <ExcelFileInput
            on:onDeploymentDetailsUpload={handleExcelDeploymentDetailsUpload}
          />
        </div>
        <div class="p-2">
          <ExcelPatternSelector
            rows={4}
            headers={deploymentSelectorHeaders}
            bind:this={customDeploymentDetailsSelector}
          />
        </div>
      {:else}
        <div class="my-3">
          <button
            class="bg-transparent hover:bg-green-700 text-green-900 dark:text-green-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-green-800 hover:border-transparent rounded-lg shadow-lg"
            >Manage Selection</button
          >
        </div>
      {/if}
  </div>
{/if}
