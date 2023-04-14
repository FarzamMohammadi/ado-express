<script lang="ts">
    import DarkToggle from './lib/shared/DarkToggle.svelte';
    import RunConfigurationsForm from './lib/shared/components/RunConfigurationsForm.svelte';
    import Navbar from './lib/shared/components/navbar/Navbar.svelte';
</script>

<svelte:head>
  <style>
    body {
      background-color: #eeeeee;
    }
    .dark body {
      background-color: #121820;
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
    <div class="z-50">
      <h1 class="text-6xl font-bold uppercase text-gray-900 dark:text-white mb-2 z-50">ADO EXPRESS</h1>

      <p class="text-md text-gray-900 dark:text-white mb-4">
        A release management tool designed to streamline the Azure DevOps
        release deployment process.
      </p>

      <div class="mb-12">
        <DarkToggle />
      </div>
    </div>

    <div class="z-10">
      <RunConfigurationsForm />
    </div>
  </div>
</main>
