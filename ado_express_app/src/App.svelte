<script lang="ts">
  import Navbar from './lib/shared/components/Navbar.svelte';
  import RunConfigurationsForm from './lib/shared/components/RunConfigurationsForm.svelte';
</script>

<main>
  <div>
    <Navbar />
  </div>

  <div
    class="flex flex-col items-center justify-center h-screen bg-gradient-to-br from-pink-500 to-orange-500"
  >
    <div class="text-gray-900">
      <h1 class="text-6xl font-bold text-center uppercase mb-4 py-10">
        ADO EXPRESS
      </h1>

      <div class="py-5">
        <RunConfigurationsForm />
      </div>
    </div>
  </div>
</main>
