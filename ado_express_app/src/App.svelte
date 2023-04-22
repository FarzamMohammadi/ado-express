<script lang="ts">
  import RunConfigurationsForm from './lib/shared/components/RunConfigurationsForm.svelte';
  import RunResults from './lib/shared/components/RunResults.svelte';
  import CustomRunSpecifierDropdown from './lib/shared/components/custom-form-components/CustomRunSpecifierDropdown.svelte';
  import Navbar from './lib/shared/components/navbar/Navbar.svelte';
  import DarkToggle from './lib/shared/components/utils/DarkToggle.svelte';
  import { running } from './lib/utils/stores';

  // function setRunStatus() {
  //   $running = !$running;
  // }

  let runType;
  let runMethod;
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
  <!-- <button on:click={setRunStatus}>asdfsadf</button> -->

  <div>
    <Navbar />
  </div>

  <div class="flex flex-col items-center justify-center to-gray-600 pb-8">
    <div class="z-50 mb-5">
      <h1
        class="text-4xl font-bold text-gray-900 dark:text-white z-50 max-w-4xl"
      >
        Effortlessly Manage ADO Releases & Deployments
      </h1>
    </div>

    <div class="z-50">
      <h6 class="text-md text-gray-900 dark:text-white mb-4 max-w-3xl">
        ADO Express is a meticulously crafted release management tool, tailored
        to simplify and enhance the Azure DevOps release deployment process.
      </h6>
    </div>

    <div class="z-50 mb-12">
      <DarkToggle />
    </div>

    <div class="w-[500px] mb-12 z-40">
      <CustomRunSpecifierDropdown
        bind:selectedCategoryName={runType}
        bind:selectedTask={runMethod}
      />
    </div>

    <div
      class="z-30 flex justify-center items-center"
      style="max-width: 100vw;"
    >
      <div
        class="smooth-transition"
        style="transform: {$running ? 'translateX(-25%)' : 'translateX(0)'}
        width: {$running ? '100%' : '50%'}"
      >
        <RunConfigurationsForm
          bind:running={$running}
          bind:runType
          bind:runMethod
        />
      </div>

      <div
        class="overflow-hidden smooth-transition items-center"
        style="
          width: {$running ? '50%' : '0'};
          transform: {$running ? 'translateX(25%)' : 'translateX(0)'};
          max-width: 35vw;
          min-width: {$running ? '35vw' : '0'};
        "
      >
        <RunResults />
      </div>
    </div>
  </div>
</main>

<style>
  .smooth-transition {
    transition: all 3s ease;
  }
</style>
