<script lang="ts">
  import type { DeploymentDetails } from '../../../../models/classes/deployment-details.model';
  import { clickOutside } from '../../../../utils/click-outside';
  import Tooltip from '../../utils/Tooltip.svelte';
  import DeploymentDetailSelectionResults from './DeploymentDetailSelectionResults.svelte';
  import ExcelFileInput from './ExcelFileInput.svelte';
  import ExcelPatternSelector from './ExcelPatternSelector.svelte';

  export let deploymentDetails: DeploymentDetails[];
  export let deploymentSelectorHeaders: string[] = [];
  export let showInput: boolean;
  export let deploymentDetailsType;
  export let customDeploymentDetailsSelector;
  let showResults = true;

  function handleClickOutside() {
    showResults = false;
  }

  function handleClickInside() {
    showResults = true;
  }
</script>

{#if showInput}
  <div
    class="w-full border-2 rounded border-gray-600 dark:border-gray-500 mt-2 mb-3 p-2 mx-4"
    id="deploymentDetails"
    use:clickOutside
    on:click_outside={handleClickOutside}
    on:click={handleClickInside}
    on:keypress={handleClickInside}
  >
    <div class="flex justify-center ml-3">
      <label for="deploymentDetails" class="font-bold text-gray-900 dark:text-white mt-2 mr-1"
        >Deployment Details</label
      >

      <Tooltip text="Top tooltip" position="right">
        <i class="mi mi-circle-information text-gray-900 dark:text-white"
          ><span class="sr-only">Circle information</span></i
        >
      </Tooltip>
    </div>

    <div class="flex justify-center pb-2 pt-2 text-gray-900 dark:text-white">
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
          bind:deploymentDetails
          bind:this={customDeploymentDetailsSelector}
        />
      </div>
    {:else if deploymentDetailsType === 'file'}
      <div class="p-2">
        <ExcelFileInput bind:deploymentDetails />
      </div>
    {/if}

    {#if deploymentDetails.length}
      <DeploymentDetailSelectionResults
        bind:deploymentDetails
        bind:showResults
        on:removeDeploymentDetails={() => (deploymentDetails = [])}
      />
    {/if}

    {#if !showResults && deploymentDetails.length}
      <button
        class="bg-transparent hover:bg-green-700 text-green-900 dark:text-green-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-green-800 hover:border-transparent rounded-lg shadow-lg"
        >Show Selection</button
      >
    {/if}
  </div>
{/if}
