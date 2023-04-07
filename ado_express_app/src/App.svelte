<script lang="ts">
  import RunConfigurationsForm from './lib/shared/components/RunConfigurationsForm.svelte';
  import Navbar from './lib/shared/components/utils/navbar/Navbar.svelte';
</script>

<svelte:head>
  <style>
    body {
      @apply bg-gradient-to-r from-gray-300 via-gray-100 to-gray-600;
    }
  </style>
</svelte:head>

<main>
  <div>
    <Navbar />
  </div>

  <div
    class="flex flex-col items-center min-w-full min-h-screen justify-center to-gray-600 pb-8"
  >
    <div class="text-center">
      <h1 class="text-6xl font-bold uppercase py-10 text-gray-900">
        ADO EXPRESS
      </h1>

      <hr class=" border-gray-900 border-t-4 mx-auto mb-8 w-2/12" />
    </div>

    <div>
      <RunConfigurationsForm />
    </div>
  </div>
</main>
