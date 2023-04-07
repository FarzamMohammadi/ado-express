<script>
  import Tooltip from '../../utils/Tooltip.svelte';

  export let label;
  export let id;
  export let bindValue;
  export let required = false;
  export let showInput;

  let showPAT = false;
</script>

{#if showInput}
<div class="password-input mb-4">
  <div class="flex items-center justify-between">
    <label for={id} class="font-bold mb-2">{label} </label>
    <Tooltip text="Top tooltip" position="right">
      <i class="mi mi-circle-information"><span class="sr-only">Circle information</span></i>
    </Tooltip>
  </div>
  <div class="relative divide-x-0 divide-gray-200 hover:divide-x-2 divide-y-0">
    {#if showPAT}
      <input
        type="text"
        {id}
        {required}
        class="bg-gray-50 border-2 border-gray-300 text-gray-900 text-sm rounded-lg focus:outline-none focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        autocomplete="off"
        bind:value={bindValue}
      />
    {:else}
      <input
        type="password"
        {id}
        {required}
        class="bg-gray-50 border-2 border-gray-300 text-gray-900 text-sm rounded-lg focus:outline-none focus:border-blue-500block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        autocomplete="off"
        bind:value={bindValue}
      />
    {/if}
    <button
      type="button"
      class="absolute inset-y-0 right-0 items-center px-2"
      on:click={() => (showPAT = !showPAT)}
    >
      {#if showPAT}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="feather feather-eye"
        >
          <path
            d="M23.928 11.036c-.182-.28-4.441-6.936-11.928-6.936s-11.746 6.656-11.928 6.936a.5.5 0 000 .928C1.184 12.964 5.439 19.5 12 19.5s10.816-6.536 11.928-7.536a.5.5 0 000-.928zM12 16.5a4.5 4.5 0 110-9 4.5 4.5 0 010 9z"
          />
        </svg>
      {:else}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="feather feather-eye-slash"
        >
          <path
            d="M23.928 11.036c-.182-.28-4.441-6.936-11.928-6.936s-11.746 6.656-11.928 6.936a.5.5 0 000 .928C1.184 12.964 5.439 19.5 12 19.5s10.816-6.536 11.928-7.536a.5.5 0 000-.928zM2.5 2.5l19 19M2.5 21.5l19-19"
          />
        </svg>
      {/if}
    </button>
  </div>
</div>
{/if}