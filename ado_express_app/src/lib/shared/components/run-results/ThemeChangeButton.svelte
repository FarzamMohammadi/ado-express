<script lang="ts">
  export let matrixTheme: boolean;
  let buttonClass: string;

  $: if (matrixTheme) {
    buttonClass =
      'focus:ring-1 focus:outline-none focus:ring-green-500 bg-transparent hover:bg-green-700 text-green-900 dark:text-green-500 font-semibold hover:text-white dark:hover:text-white border border-green-800 hover:border-transparent rounded-lg shadow-lg';
  } else {
    buttonClass =
      'focus:ring-1 focus:outline-none focus:ring-purple-500 bg-transparent hover:bg-purple-700 text-purple-900 dark:text-purple-500 font-semibold hover:text-white dark:hover:text-white border border-purple-800 hover:border-transparent rounded-lg shadow-lg';
  }
</script>

<button class={buttonClass} on:click={() => (matrixTheme = !matrixTheme)}> Toggle Theme </button>

<style>
  button {
    cursor: pointer;
    font-size: 14px;
    margin-top: 8px;
  }
</style>
