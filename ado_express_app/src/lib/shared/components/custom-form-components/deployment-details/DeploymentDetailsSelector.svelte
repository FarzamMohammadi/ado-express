<script lang="ts">
  import { clickOutside } from '../../../../utils/click-outside';
  import { deploymentDetails } from '../../../../utils/stores';
  import Tooltip from '../../utils/Tooltip.svelte';

  import ExcelFileInput from './ExcelFileInput.svelte';
  import ExcelPatternSelector from './ExcelPatternSelector.svelte';

  export let deploymentSelectorHeaders: string[] = [];
  export let isSubmitting;
  export let showCustomSelector = false;
  export let showInput: boolean;

  let customDeploymentDetailsSelector;
  let invalid = false;

  function checkSelectionValidity() {
    invalid = !$deploymentDetails || $deploymentDetails.length <= 0;
  }

  function handleClickInside() {
    showCustomSelector = true;
  }

  function handleClickOutside() {
    if (showCustomSelector) {
      checkSelectionValidity();
      showCustomSelector = false;
    }
  }

  function handleExcelDeploymentDetailsUpload() {
    customDeploymentDetailsSelector.setDeploymentDetailsValuesToTable();
  }

  $: {
    if ((isSubmitting && showInput) || $deploymentDetails.length) {
      checkSelectionValidity();
    }
  }
</script>

{#if showInput}
  <div
    id="$deploymentDetails"
    class="border-2 border-gray-600 dark:border-gray-500 mb-3 mt-2 mx-4 p-2 rounded w-full {invalid ? 'invalid' : ''}"
    use:clickOutside
    on:click_outside={handleClickOutside} on:click={handleClickInside}
    on:keypress={handleClickInside}
  >
    <div class="flex justify-center ml-3">
      <label for="$deploymentDetails" class="font-bold mr-1 mt-2 text-gray-900 dark:text-white {invalid ? 'text-red-500' : ''}">
        Deployment Details {invalid ? '*' : ''}
      </label>

      <Tooltip position="right" text="Top tooltip">
        <i class="mi mi-circle-information text-gray-900 dark:text-white {invalid ? 'text-red-500' : ''}">
          <span class="sr-only">Circle information</span>
        </i>
      </Tooltip>
    </div>

    {#if showCustomSelector}
      <div class="p-2 mt-2 read-only">
        <ExcelFileInput on:onDeploymentDetailsUpload={handleExcelDeploymentDetailsUpload} />
      </div>

      <div class="p-2">
        <ExcelPatternSelector bind:this={customDeploymentDetailsSelector} headers={deploymentSelectorHeaders} rows={4} />
      </div>
    {:else}
      <div class="my-3">
        <button
          class="bg-transparent border border-green-800 dark:hover:text-white dark:text-green-500 font-semibold hover:bg-green-700 hover:border-transparent hover:text-white px-4 py-2 rounded-lg shadow-lg text-green-900"
        >
          Manage Selection
        </button>
      </div>
    {/if}
  </div>
{/if}

<style lang="scss">
  .invalid {
    border-color: red;
    animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
    transform: translate3d(0, 0, 0);
    backface-visibility: hidden;
    perspective: 1000px;
  }

  @keyframes shake {
    10%,
    90% {
      transform: translate3d(-1px, 0, 0);
    }

    20%,
    80% {
      transform: translate3d(2px, 0, 0);
    }

    30%,
    50%,
    70% {
      transform: translate3d(-4px, 0, 0);
    }

    40%,
    60% {
      transform: translate3d(4px, 0, 0);
    }
  }
</style>
