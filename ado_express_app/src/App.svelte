<script lang="ts">
  import RunConfigurationsForm from './lib/shared/components/RunConfigurationsForm.svelte';
  import Navbar from './lib/shared/components/navbar/Navbar.svelte';
</script>

<svelte:head>
  <style>
    body {
      @apply bg-gradient-to-r from-gray-300 via-gray-100 to-gray-600;
    }
  </style>
</svelte:head>

<main class="min-w-full min-h-screen">
  <div>
    <Navbar />
  </div>

  <div
  class="flex flex-col items-center justify-center to-gray-600 pb-8"
  >
    <div>
      <h1 class="text-6xl font-bold uppercase pt-10 pb-5 text-gray-900">
        ADO EXPRESS
      </h1>


      <p class="text-md text-gray-900 pb-8">
        A release management tool designed to streamline the Azure DevOps release deployment process.
      </p>

      <hr class="border-gray-900 border-t-4 mx-auto mb-8 w-2/12" />
    </div>

    <div>
      <RunConfigurationsForm />
    </div>
  </div>
</main>
