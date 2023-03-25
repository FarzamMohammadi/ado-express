<script>
  import { createPopper } from '@popperjs/core';
  import { onMount } from 'svelte';
  import { clickOutside } from '../../utils/click-outside';

  let categories = [
    {
      name: 'Search',
      tasks: [
        'Via Environment',
        'Via Latest in Environment',
        'Via Number',
        'Via Query',
      ],
    },
    {
      name: 'Deploy',
      tasks: ['Via Number', 'Via Latest in Environment'],
    },
  ];

  let selectedCategory = null;
  export let selectedCategoryName = null;
  export let selectedTask = null;

  let dropdownButton;
  let dropdownList;

  let dropdownOpen = false;
  let dropdownPopover = null;

  const closeDropdown = () => {
    dropdownOpen = false;
    dropdownPopover.destroy();
    dropdownPopover = null;
  };

  const handleClickOutside = () => {
    if (dropdownOpen) {
      closeDropdown();
    }
  };

  const toggleDropdown = () => {
    dropdownOpen = !dropdownOpen;
    
    if (dropdownOpen) {
      dropdownPopover = createPopper(dropdownButton, dropdownList, {
        placement: 'bottom-start',
        modifiers: [
          {
            name: 'offset',
            options: {
              offset: [0, 10],
            },
          },
        ],
      });
    } else {
      dropdownPopover.destroy();
      dropdownPopover = null;
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
  };

  onMount(() => {
    // destroy popper instance if dropdown is closed on component unmount
    return () => {
      if (dropdownPopover) {
        dropdownPopover.destroy();
        dropdownPopover = null;
      }
    };
  });
</script>

<div class="relative" use:clickOutside on:click_outside={handleClickOutside}>
  <button
    class="w-full px-4 py-2 text-left text-gray-800 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-indigo-500"
    on:click={toggleDropdown}
    aria-haspopup="true"
    aria-expanded={dropdownOpen ? 'true' : 'false'}
    bind:this={dropdownButton}
  >
    {#if selectedCategory}
      {selectedCategory.name}
      {#if selectedTask} &raquo; {selectedTask} {/if}
    {:else}
      Select a category
    {/if}
  </button>
  {#if dropdownOpen}
    <div
      class="absolute w-full mt-2 bg-white rounded-md shadow-lg"
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="options-menu"
      bind:this={dropdownList}
    >
      {#each categories as category}
        <button
          class="flex items-center justify-between w-full px-4 py-2 text-gray-200 rounded hover:bg-gray-800"
          on:click={() => selectCategory(category)}
        >
          <span class="text-lg font-semibold">{category.name}</span>
        </button>
        {#if selectedCategory === category}
          {#each category.tasks as task}
            <button
              class="flex items-center justify-between w-full px-4 py-2 text-gray-200 rounded hover:bg-gray-800"
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
