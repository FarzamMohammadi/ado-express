<script lang="ts">
  import { onMount } from 'svelte';
  import ExploreBtn from './ExploreBtn.svelte';

  const breakpoint = 768;

  let isMenuOpen = false;
  let isMobile = false;
  let showLinks = false;

  function checkScreenSize() {
    isMobile = window.innerWidth <= breakpoint;
  }

  function handleResize() {
    checkScreenSize();
  }

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
  }

  function handleMouseEnter() {
    showLinks = true;
  }

  function handleMouseLeave() {
    showLinks = false;
  }

  onMount(() => {
    window.addEventListener('resize', handleResize);
    checkScreenSize();
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  });
</script>

<nav>
  <div class="w-full mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-14" on:mouseleave={handleMouseLeave}>
      <div class="flex justify-center items-center">
        <div class="flex items-center space-x-3">
          <a target="_blank" href="https://github.com/FarzamMohammadi/ado-express" on:mouseenter={handleMouseEnter}>
            <img
              class={`h-16 w-26 mr-2 rounded-lg shadow-lg hover:shadow-xl transition duration-500 ease-in-out transform hover:-translate-y-1 border-2 border-gray-700 dark:border-gray-600 ${
                isMobile ? 'w-22' : ''
              }`}
              src="./logo.png"
              alt="Logo of the application name, 'ADO Express'"
            />
          </a>

          {#if showLinks && !isMobile}
            <a
              target="_blank"
              href="https://github.com/FarzamMohammadi"
              class="text-md font-medium text-gray-900 dark:text-white px-3 py-2 border-2 rounded border-gray-700 dark:border-gray-600 hover:bg-gray-200 dark:hover:bg-gray-800 hover:shadow-xl"
              >About</a
            >
            <a
              target="_blank"
              href="https://github.com/FarzamMohammadi/ado-express/issues"
              class="text-md font-medium text-gray-900 dark:text-white px-3 py-2 border-2 rounded border-gray-700 dark:border-gray-600 hover:bg-gray-200 dark:hover:bg-gray-800 hover:shadow-xl"
              >Contact</a
            >
            <a
              target="_blank"
              href="https://github.com/FarzamMohammadi/ado-express#readme"
              class="text-md font-medium text-gray-900 dark:text-white px-3 py-2 border-2 rounded border-gray-700 dark:border-gray-600 hover:bg-gray-200 dark:hover:bg-gray-800 hover:shadow-xl"
              >Technical FAQs</a
            >
          {/if}
        </div>
      </div>

      <div on:mouseenter={handleMouseLeave} class="m-1">
        <ExploreBtn />
      </div>
    </div>

    <div class="flex items-center justify-end m-3">
      <div class="mt-2 flex md:hidden">
        <button
          type="button"
          class="inline-flex items-center justify-center p-2 rounded-md border-2 border-gray-400 text-gray-500 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 focus:text-gray-900 dark:text-white transition duration-150 ease-in-out"
          aria-label="Main menu"
          aria-expanded="false"
          on:click={toggleMenu}
        >
          <svg class="block h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg class="hidden h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>

  <div class={`${isMenuOpen ? 'block' : 'hidden'} md:hidden`}>
    <div class="px-2 pt-2 pb-3 sm:px-3">
      <a
        target="_blank"
        href="https://github.com/FarzamMohammadi"
        class="mt-1 block px-3 py-2 rounded-md text-base text-md font-medium text-gray-900 dark:text-white border-2 border-gray-700 dark:border-gray-600 hover:bg-gray-200 dark:hover:bg-gray-800 hover:shadow-xl"
        >About</a
      >
      <a
        target="_blank"
        href="https://github.com/FarzamMohammadi/ado-express/issues"
        class="mt-1 block px-3 py-2 rounded-md text-base text-md font-medium text-gray-900 dark:text-white border-2 border-gray-700 dark:border-gray-600 hover:bg-gray-200 dark:hover:bg-gray-800 hover:shadow-xl"
        >Contact</a
      >
      <a
        target="_blank"
        href="https://github.com/FarzamMohammadi/ado-express#readme"
        class="mt-1 block px-3 py-2 rounded-md text-base text-md font-medium text-gray-900 dark:text-white border-2 border-gray-700 dark:border-gray-600 hover:bg-gray-200 dark:hover:bg-gray-800 hover:shadow-xl"
        >Technical FAQs</a
      >
    </div>
  </div>
</nav>
