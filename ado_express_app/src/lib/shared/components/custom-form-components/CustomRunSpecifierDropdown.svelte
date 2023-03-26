<script>
  import { onMount } from 'svelte';
  import { RunType } from '../../../models/enums/enums';
  import { clickOutside } from '../../../utils/click-outside';
  import Tooltip from '../utils/Tooltip.svelte';

  let categories = [
    {
      name: RunType.Search,
      tasks: [
        'Via Environment',
        'Via Latest in Environment',
        'Via Number',
        'Via Query',
      ],
    },
    {
      name: RunType.Deploy,
      tasks: ['Via Number', 'Via Latest in Environment'],
    },
  ];

  let selectedCategory = null;
  export let selectedCategoryName = null;
  export let selectedTask = null;

  let dropdownButton;
  let dropdownList;

  let dropdownOpen = false;

  const closeDropdown = () => {
    dropdownOpen = false;
  };

  const handleClickOutside = () => {
    if (dropdownOpen) {
      closeDropdown();
    }
  };

  const toggleDropdown = () => {
    dropdownOpen = !dropdownOpen;
  };

  const selectCategory = (category) => {
    selectedCategory = category;
    selectedTask = null;
  };

  const selectTask = (task) => {
    selectedCategoryName = selectedCategory.name;
    selectedTask = task;
    closeDropdown();
  };

  onMount(() => {
    // destroy popper instance if dropdown is closed on component unmount
    return () => {
      if (dropdownOpen) {
        dropdownOpen = !dropdownOpen;
      }
    };
  });
</script>

<div class="relative" use:clickOutside on:click_outside={handleClickOutside}>
  <button
    class="w-full px-4 text-left text-gray-800 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-indigo-500 flex items-center justify-between"
    on:click={toggleDropdown}
    aria-haspopup="true"
    aria-expanded={dropdownOpen ? 'true' : 'false'}
    bind:this={dropdownButton}
  >
    <div>
      {#if selectedCategory}
        {selectedCategory.name}
        {#if selectedTask} &raquo; {selectedTask} {/if}
      {:else}
        Select run type
      {/if}
    </div>

    <div class="relative">
      <Tooltip text="Top tooltip" position="right">
        <i class="mi mi-circle-information"
          ><span class="sr-only">Circle information</span></i
        >
      </Tooltip>
    </div>
  </button>

  {#if dropdownOpen}
    <div
      class="absolute w-full mt-2 bg-transparent rounded-md shadow-lg"
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="options-menu"
      bind:this={dropdownList}
    >
      {#each categories as category}
        <button
          class="flex items-center justify-start w-full px-4 py-2 bg-stone-900 text-gray-200 rounded-lg hover:bg-gray-800"
          on:click={() => selectCategory(category)}
        >
          <span class="text-lg font-semibold">{category.name}</span>
        </button>
        {#if selectedCategory === category}
          {#each category.tasks as task}
            <button
              class="flex items-center justify-start w-full px-4 py-2 bg-stone-800 text-gray-200 rounded hover:bg-gray-700"
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
