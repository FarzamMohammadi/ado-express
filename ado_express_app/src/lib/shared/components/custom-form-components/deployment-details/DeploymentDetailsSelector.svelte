<script lang="ts">
  import { clickOutside } from '../../../../utils/click-outside';
  import { deploymentDetails } from '../../../../utils/stores';
  import Tooltip from '../../utils/Tooltip.svelte';
  import ExcelFileInput from './ExcelFileInput.svelte';
  import ExcelPatternSelector from './ExcelPatternSelector.svelte';

  export let deploymentSelectorHeaders: string[] = [];
  export let showInput: boolean;
  export let showCustomSelector = false;
  export let isSubmitting;
  let invalid = false;
  let customDeploymentDetailsSelector;

  function handleClickOutside() {
    if (showCustomSelector){
      checkSelectionValidity();
      showCustomSelector = false;
    }
  }

  function handleClickInside() {
    showCustomSelector = true;
  }

  function handleExcelDeploymentDetailsUpload() {
    customDeploymentDetailsSelector.setDeploymentDetailsValuesToTable();
  }

  function checkSelectionValidity() {
    invalid = !$deploymentDetails || $deploymentDetails.length <= 0;
  }


  $ : {
    if (isSubmitting && showInput || $deploymentDetails.length) {
      checkSelectionValidity();
    }
  }
</script>

{#if showInput}
  <div
    class="w-full border-2 rounded border-gray-600 dark:border-gray-500 mt-2 mb-3 p-2 mx-4 {invalid ? 'invalid' : ''}"
    id="$deploymentDetails"
    use:clickOutside on:click_outside={handleClickOutside}
    on:click={handleClickInside}
    on:keypress={handleClickInside}
  >
    <div class="flex justify-center ml-3">
      <label
        for="$deploymentDetails"
        class="font-bold text-gray-900 dark:text-white mt-2 mr-1 {invalid ? 'text-red-500' : ''}"
        >Deployment Details {invalid ? '*' : ''} </label
      >

      <Tooltip text="Top tooltip" position="right">
        <i class="mi mi-circle-information text-gray-900 dark:text-white {invalid ? 'text-red-500' : ''}"
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

<style lang="scss">
  .invalid {
    border-color: red;
    animation: shake 0.82s cubic-bezier(.36,.07,.19,.97) both;
    transform: translate3d(0, 0, 0);
    backface-visibility: hidden;
    perspective: 1000px;
  }

  @keyframes shake {
    10%, 90% {
      transform: translate3d(-1px, 0, 0);
    }
    
    20%, 80% {
      transform: translate3d(2px, 0, 0);
    }

    30%, 50%, 70% {
      transform: translate3d(-4px, 0, 0);
    }

    40%, 60% {
      transform: translate3d(4px, 0, 0);
    }
  }
</style>