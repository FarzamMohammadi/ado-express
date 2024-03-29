<script lang="ts">
  import { onMount } from 'svelte';

  import { DeploymentRunMethod, RunType, SearchRunMethod } from '../../../models/enums/enums';
  import { clickOutside } from '../../../utils/click-outside';
  import Tooltip from '../utils/Tooltip.svelte';

  export let isSubmitting;
  export let selectedCategoryName = null;
  export let selectedTask = null;

  let categories = [
    {
      name: RunType.Deploy,
      tasks: [DeploymentRunMethod.ViaNumber],
    },
    {
      name: RunType.Search,
      tasks: [SearchRunMethod.ViaEnvironment, SearchRunMethod.ViaLatestInEnvironment, SearchRunMethod.ViaNumber, SearchRunMethod.ViaQuery],
    },
  ];

  let dropdownButton;
  let dropdownList;
  let dropdownOpen = false;
  let invalid = false;
  let selectedCategory = null;

  const checkSelectionValidity = () => {
    invalid = !selectedCategoryName || !selectedTask;
  };

  const closeDropdown = () => {
    dropdownOpen = false;
    checkSelectionValidity();
  };

  const handleClickOutside = () => {
    if (dropdownOpen) {
      closeDropdown();
    }
  };

  const selectCategory = (category) => {
    selectedCategory = category;
    selectedTask = null;
  };

  const selectTask = (task) => {
    selectedCategoryName = selectedCategory.name;
    selectedTask = task;
    closeDropdown();
    checkSelectionValidity();
  };

  const toggleDropdown = () => {
    dropdownOpen = !dropdownOpen;
  };

  onMount(() => {
    return () => {
      if (dropdownOpen) {
        closeDropdown();
      }
    };
  });

  $: {
    if (selectedCategoryName) {
      selectedCategory = categories.find((category) => category.name === selectedCategoryName);
    }

    if (isSubmitting) {
      checkSelectionValidity();
    }
  }
</script>

<div class="relative lg:w-full w-5/6 mx-auto" use:clickOutside on:click_outside={handleClickOutside}>
  <button
    class="w-full px-4 text-left text-gray-800 dark:text-white bg-white dark:bg-gray-700 border border-gray-500 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-indigo-500 flex items-center justify-between {invalid
      ? 'invalid'
      : ''}"
    on:click={toggleDropdown}
    aria-haspopup="true"
    aria-expanded={dropdownOpen ? 'true' : 'false'}
    bind:this={dropdownButton}
  >
    <div class={invalid ? 'text-red-500' : ''}>
      {#if selectedCategory}
        {selectedCategory.name}
        {#if selectedTask}
          &raquo;
          {selectedTask}
        {/if}
      {:else}
        Select run type {invalid ? '*' : ''}
      {/if}
    </div>

    <div class="relative flex flex-row items-center {invalid ? 'text-red-500' : ''}">
      <Tooltip text="Top tooltip" position="right">
        <i class="mi mi-circle-information"><span class="sr-only">Circle information</span></i>
      </Tooltip>

      <div class="ml-2">
        <svg class="w-4 h-4 ml-2" aria-hidden="true" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </div>
  </button>

  {#if dropdownOpen}
    <div class="absolute w-full mt-2 bg-transparent rounded-md shadow-lg" role="menu" aria-orientation="vertical" aria-labelledby="options-menu" bind:this={dropdownList}>
      {#each categories as category}
        <button
          type="button"
          class="flex items-center justify-between w-full px-4 py-2 hover:bg-gray-600 bg-gray-900 dark:bg-neutral-800
        dark:hover:bg-gray-600 dark:hover:text-white text-white"
          on:click={() => selectCategory(category)}
        >
          <span class="text-lg font-semibold">{category.name}</span>

          {#if selectedCategory === category}
            <svg class="w-4 h-4 ml-2" aria-hidden="true" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          {:else}
            <svg aria-hidden="true" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path
                fill-rule="evenodd"
                d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                clip-rule="evenodd"
              />
            </svg>
          {/if}
        </button>

        {#if selectedCategory === category}
          {#each category.tasks as task}
            <button
              class="flex items-center justify-start w-full px-4 py-2 text-gray-200 rounded hover:bg-gray-700
            bg-gray-800 dark:bg-neutral-700 dark:hover:bg-gray-600 dark:hover:text-white"
              on:click={() => selectTask(task)}
            >
              <small class="ml-3 italic">{task}</small>
            </button>
          {/each}
        {/if}
      {/each}
    </div>
  {/if}
</div>

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
