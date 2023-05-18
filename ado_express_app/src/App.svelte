<script lang="ts">
  import RunConfigurationsForm from './lib/shared/components/RunConfigurationsForm.svelte';
  import CustomRunSpecifierDropdown from './lib/shared/components/custom-form-components/CustomRunSpecifierDropdown.svelte';
  import Navbar from './lib/shared/components/navbar/Navbar.svelte';
  import RunResults from './lib/shared/components/run-results/RunResults.svelte';
  import DarkToggle from './lib/shared/components/utils/DarkToggle.svelte';
  import { running } from './lib/utils/stores';
  import { websocketStore } from './lib/utils/websocketStores/websocket-store';

  let formStyle;
  let isSubmitting;
  let resultStyle;
  let runMethod;
  let runType;

  websocketStore.connect();

  $: formStyle = `transform: ${$running ? 'translateX(-25%)' : 'translateX(0)'} width: ${$running ? '100%' : '50%'};`;
  $: resultStyle = `width: ${$running ? '50%' : '0'}; transform: ${$running ? 'translateX(25%)' : 'translateX(0)'}; max-width: 35vw; min-width: ${$running ? '35vw' : '0'};`;
</script>

<svelte:head>
  <style>
    body {
      background-color: #eeeeee;
    }
    .dark body {
      background-color: #1a1e24;
    }
  </style>
</svelte:head>

<main class="min-w-full min-h-screen bg-[#eeeeee] dark:bg-[#1a1e24]">

  <Navbar />

  <div class="flex flex-col items-center justify-center to-gray-600 pb-8">

    <h1 class="z-50 text-4xl font-bold text-gray-900 dark:text-white mb-5 max-w-4xl">
      Effortlessly Manage ADO Releases & Deployments
    </h1>
    
    <p class="z-50 text-md text-gray-900 dark:text-white mb-4 max-w-3xl">
      ADO Express is a meticulously crafted release management tool, tailored
      to simplify and enhance the Azure DevOps release deployment process.
    </p>

    <div class="z-50 mb-12">
      <DarkToggle />
    </div>

    <div class="w-[500px] mb-12 z-40">
      <CustomRunSpecifierDropdown
        bind:selectedCategoryName={runType}
        bind:selectedTask={runMethod}
        bind:isSubmitting
      />
    </div>

    {#if $running}
      <a
        class="my-4 bg-transparent hover:bg-purple-700 text-purple-900 dark:text-purple-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-purple-800 hover:border-transparent rounded-lg shadow-lg"
        data-sveltekit-preload-data="tap"
        href="/"
      >
        Clear Form & Results
      </a>
    {/if}

    <div class="z-30 flex justify-center items-center max-w-screen">
      
      <div class="smooth-transition" style={formStyle}>
        <RunConfigurationsForm
          bind:running={$running}
          bind:runType
          bind:runMethod
          bind:isSubmitting
        />
      </div>

      <div class="overflow-hidden smooth-transition items-center z-30" style={resultStyle}>
        <RunResults />
      </div>
      
    </div>
    
  </div>
</main>

<style>
  .smooth-transition {
    transition: all 2s ease;
  }
</style>
