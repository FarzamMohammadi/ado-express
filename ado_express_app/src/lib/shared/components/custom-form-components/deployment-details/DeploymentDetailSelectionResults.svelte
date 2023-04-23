<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { DeploymentDetail } from '../../../../models/classes/deployment-detail.model';

  const dispatch = createEventDispatcher();

  export let deploymentDetails: DeploymentDetail[];
  export let showResults;

  function removeDeploymentDetails() {
    dispatch('removeDeploymentDetails');
  }
</script>

{#if showResults}
  <div class="flex flex-col items-center border-2 rounded border-gray-500 m-2">
    <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div class="inline-block min-w-full py-2 sm:px-6 lg:px-8">
        <div class="overflow-hidden">
          <table
            class="min-w-full text-center text-md font-normal text-gray-900 dark:text-gray-300"
          >
            <thead class="border-b font-medium text-gray-800 dark:text-white">
              <tr>
                <th scope="col" class="px-6 py-4">#</th>
                <th scope="col" class="px-6 py-4">Project Name</th>
                <th scope="col" class="px-6 py-4">Release Name</th>
                <th scope="col" class="px-6 py-4">Release #</th>
                <th scope="col" class="px-6 py-4">Rollback #</th>
                <th scope="col" class="px-6 py-4">Crucial</th>
              </tr>
            </thead>
            <tbody>
              {#each deploymentDetails as row, i}
                <tr class="border-b">
                  <td class="whitespace-nowrap px-6 py-4 font-medium"
                    >{i + 1}</td
                  >
                  <td class="whitespace-nowrap px-6 py-4"
                    >{row.releaseProjectName}</td
                  >
                  <td class="whitespace-nowrap px-6 py-4">{row.releaseName}</td>
                  <td class="whitespace-nowrap px-6 py-4"
                    >{row.releaseNumber}</td
                  >
                  <td class="whitespace-nowrap px-6 py-4"
                    >{row.releaseRollback}</td
                  >
                  <td class="whitespace-nowrap px-6 py-4">{row.isCrucial}</td>
                </tr>
              {/each}
            </tbody>
          </table>
          <div class="flex flex-col justify-start mt-4">
            <p class="text-gray-900 dark:text-gray-200 font-bold mb-2">
              Something missing?
            </p>
            <button
              on:click={() => removeDeploymentDetails()}
              class="bg-transparent hover:bg-red-700 text-red-900 dark:text-red-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-red-800 hover:border-transparent rounded-lg shadow-lg"
              >Remove Values</button
            >
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th,
  td {
    padding: 8px;
    text-align: center;
    border-bottom: 1px solid #ddd;
  }
  tr:hover td {
    background-color: #f5f5f528;
  }
</style>
