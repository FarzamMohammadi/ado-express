<script lang="ts">
    import Navbar from './lib/shared/components/Navbar.svelte';
    import RunConfigurationsForm from './lib/shared/components/RunConfigurationsForm.svelte';
</script>

<svelte:head>
  <style>
    body {
      @apply  bg-gradient-to-r from-gray-300 via-gray-100 to-gray-600;
    }
  </style>
</svelte:head>

<main>
  <div>
    <Navbar />
  </div>

  <div class="flex flex-col items-center min-w-full min-h-screen justify-center to-gray-600 pb-8"> 
      <div>
        <h1 class="text-6xl font-bold text-center uppercase py-10 text-gray-900">
          ADO EXPRESS
        </h1>
      </div>
  
      <div>
        <RunConfigurationsForm />
      </div>
   
  </div>
</main>
