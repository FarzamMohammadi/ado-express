<script lang="ts">
  import { deploymentDetails } from '../../../../utils/stores';
  export let showingDeploymentDetailsReadOnlySelection: boolean;
</script>

{#if showingDeploymentDetailsReadOnlySelection}
  <div class="border-2 border-gray-500 flex flex-col items-center m-2 rounded">
    <div class="lg:-mx-8 overflow-x-auto sm:-mx-6">
      <div class="inline-block lg:px-8 min-w-full py-2 sm:px-6">
        <div class="overflow-hidden">
          <table class="dark:text-gray-300 font-normal min-w-full text-center text-gray-900 text-md">
            <thead class="border-b dark:text-white font-medium text-gray-800">
              <tr>
                <th class="px-6 py-4" scope="col">#</th>
                <th class="px-6 py-4" scope="col">Project Name</th>
                <th class="px-6 py-4" scope="col">Release Name</th>
                <th class="px-6 py-4" scope="col">Release #</th>
                <th class="px-6 py-4" scope="col">Rollback #</th>
                <th class="px-6 py-4" scope="col">Crucial</th>
              </tr>
            </thead>
            <tbody>
              {#each $deploymentDetails as row, i}
                <tr class="border-b">
                  <td class="font-medium px-6 py-4 whitespace-nowrap">{i + 1}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{row.releaseProjectName}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{row.releaseName}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{row.releaseNumber}</td>
                  <td class="px-6 py-4 whitespace-nowrap">{row.releaseRollback}</td>
                  <td class="px-6 py-4">{row.isCrucial}</td>
                </tr>
              {/each}
            </tbody>
          </table>
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
