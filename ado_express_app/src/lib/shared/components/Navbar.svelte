<script lang="ts">
  let isMenuOpen = false;

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
  }
</script>

<nav>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">
      <div class="">
        <div class="ml-10 flex items-baseline space-x-4">
          <a
            href="#"
            class="text-md font-medium text-gray-900 px-3 py-2 border-2 border-gray-200 rounded dark:border-gray-700 hover:bg-gray-300"
            >Contact</a
          >
          <a
            href="#"
            class="text-md font-medium text-gray-900 px-3 py-2 border-2 border-gray-200 rounded dark:border-gray-700 hover:bg-gray-300"
            >About</a
          >
        </div>
      </div>

      <div>
        <a
          target="_blank"
          href="https://github.com/FarzamMohammadi/ado-express"
        >
          <img
            class="h-10 w-26 rounded-lg shadow-lg hover:shadow-xl transition duration-500 ease-in-out transform hover:-translate-y-0.5"
            src="./src/assets/logo.png"
            alt="Logo"
          />
        </a>
      </div>
    </div>
    <div class="flex items-center justify-end">
      <div class="-mr-2 flex md:hidden">
        <button
          type="button"
          class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:bg-gray-100 focus:text-gray-900 transition duration-150 ease-in-out"
          aria-label="Main menu"
          aria-expanded="false"
          on:click={toggleMenu}
        >
          <svg
            class="block h-6 w-6"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
          <svg
            class="hidden h-6 w-6"
            stroke="currentColor"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>

  <div class={`${isMenuOpen ? 'block' : 'hidden'} md:hidden`}>
    <div class="px-2 pt-2 pb-3 sm:px-3">
      <a
        href="#"
        class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-white border-2 border-gray-200 rounded dark:border-gray-700"
        >Home</a
      >
      <a
        href="#"
        class="mt-1 block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-white border-2 border-gray-200 rounded dark:border-gray-700"
        >About</a
      >
    </div>
  </div>
</nav>
