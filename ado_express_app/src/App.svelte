<script lang="ts">
  import RunConfigurationForm from "./lib/shared/components/RunConfigurationForm.svelte";
  import Navbar from "./lib/shared/components/Navbar.svelte";
</script>

<main class="container mx-auto px-4">
  <div>
    <Navbar />
  </div>

  <div class="flex flex-col items-center justify-center h-screen bg-gradient-to-br from-pink-500 to-orange-500 text-white">
    <div class="text-gray-900">

      <h1 class="text-6xl font-bold text-center uppercase mb-4 py-10">
        ADO EXPRESS
      </h1>

      <div class="py-10">
        <RunConfigurationForm />
      </div>
      
    </div>
  </div>
</main>

<style>
</style>
