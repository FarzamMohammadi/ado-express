<script lang="ts">
  import { RunType, SearchRunMethod } from '../../../models/enums/enums';
  import { ranDeployment } from '../../../utils/stores';

  export let disableSubmitButton: boolean;
  export let handleSubmit: (event: MouseEvent) => void;
  export let runType: string;
  export let runMethod: string;
  export let showSubmitButton: boolean;
  export let submitButtonLabel: string;
  export let runResultDataIsValid: boolean;
  export let setupSearchResultsForDeployment: (event: MouseEvent) => void;

  $: hasSearchResultsReadyForDeployment = !showSubmitButton && runResultDataIsValid && runType === RunType.Search && (runMethod === SearchRunMethod.ViaLatestInEnvironment || runMethod === SearchRunMethod.ViaQuery)
</script>

<div>
  {#if showSubmitButton && !$ranDeployment}
    <div class="flex justify-center pt-4">
      <button
        disabled={disableSubmitButton}
        type="button"
        on:click={handleSubmit}
        class="focus:ring-1 focus:outline-none focus:ring-blue-500 bg-transparent hover:bg-blue-700 text-blue-900 dark:text-blue-500 font-semibold hover:text-white dark:hover:text-white border border-blue-800 hover:border-transparent rounded-lg shadow-lg"
      >
        {submitButtonLabel}
      </button>
    </div>
  {/if}
  <div class="flex flex-row items-center justify-center">
    {#if hasSearchResultsReadyForDeployment}
      <button
        class="focus:ring-1 focus:outline-none focus:ring-blue-500 bg-transparent hover:bg-blue-700 text-blue-900 dark:text-blue-500 font-semibold hover:text-white dark:hover:text-white border border-blue-800 hover:border-transparent rounded-lg shadow-lg"
        on:click={setupSearchResultsForDeployment}>Deploy Search Results</button
      >
    {/if}
  </div>
</div>
