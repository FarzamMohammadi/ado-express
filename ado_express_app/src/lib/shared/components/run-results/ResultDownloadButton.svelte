<script lang="ts">
  import { runResultData } from '../../../utils/stores';

  export let matrixTheme: boolean;
  let buttonClass: string;

  function downloadResultsAsJSONFile(): void {
    const jsonString = JSON.stringify($runResultData);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'results.json';
    anchor.click();

    setTimeout(() => {
      URL.revokeObjectURL(url);
      anchor.remove();
    }, 0);
  }

  $: if (matrixTheme) {
    buttonClass =
      'focus:ring-1 focus:outline-none focus:ring-green-500 bg-transparent hover:bg-green-700 text-green-900 dark:text-green-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-green-800 hover:border-transparent rounded-lg shadow-lg';
  } else {
    buttonClass =
      'focus:ring-1 focus:outline-none focus:ring-purple-500 bg-transparent hover:bg-purple-700 text-purple-900 dark:text-purple-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-purple-800 hover:border-transparent rounded-lg shadow-lg';
  }
</script>

<button class={buttonClass} on:click={downloadResultsAsJSONFile}> Download JSON </button>

<style>
  button {
    cursor: pointer;
    font-size: 14px;
    margin-top: 8px;
  }
</style>
