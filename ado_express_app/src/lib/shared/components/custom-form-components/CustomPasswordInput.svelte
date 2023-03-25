<script>
  export let label;
  export let id;
  export let bindValue;

  let showPAT = false;
</script>

<div class="password-input mb-4">
  <label for={id} class="block font-bold mb-2">{label}</label>
  <div class="relative">
    {#if showPAT}
      <input
        type="text"
        {id}
        class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
        autocomplete="off"
        bind:value={bindValue}
      />
    {:else}
      <input
        type="password"
        {id}
        class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
        autocomplete="off"
        bind:value={bindValue}
      />
    {/if}
    <button
      class="absolute inset-y-0 right-0 flex items-center px-2 text-gray-700"
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
