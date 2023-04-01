<script lang="ts">
  import Navbar from './lib/shared/components/Navbar.svelte';
  import RunConfigurationsForm from './lib/shared/components/RunConfigurationsForm.svelte';
</script>

<main>
  <div>
    <Navbar />
  </div>

  <div class="flex flex-col items-center min-w-full min-h-screen justify-center bg-gradient-to-br from-pink-500 to-orange-500 pb-8">
    
    <div>
      <h1 class="text-6xl font-bold text-center uppercase py-10 text-gray-900">
        ADO EXPRESS
      </h1>

      <RunConfigurationsForm />
    </div>

  </div>
</main>
