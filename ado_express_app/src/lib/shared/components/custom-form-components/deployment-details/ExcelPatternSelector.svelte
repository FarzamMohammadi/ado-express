<script lang="ts">
  import { onMount } from 'svelte';
  import { DeploymentDetail } from '../../../../models/classes/deployment-detail.model';
  import { ToastType } from '../../../../models/enums/enums';
  import { deploymentDetails } from '../../../../utils/stores';
  import Toast from '../../utils/Toast.svelte';

  export let disabledColumns: number[] = [];
  export let headers: String[];
  export let rows: number;

  let cells = {};
  const columns = 6;

  function addRow() {
    rows += 1;
    updateDeploymentDetails();
  }

  function cellId(row, col) {
    return `${row}-${col}`;
  }

  function handleInput(row, col, event) {
    const id = cellId(row, col);
    if (col === 5) {
      cells[id] = event.target.checked;
    } else {
      cells[id] = event.target.value;
    }
    updateDeploymentDetails();
  }

  function removeRow() {
    if (rows > 0) {
      rows -= 1;
      for (let col = 1; col <= columns; col++) {
        delete cells[cellId(rows, col)];
      }
      updateDeploymentDetails();
    }
  }

  export function setDeploymentDetailsValuesToTable() {
    if ($deploymentDetails.length) {
      rows = $deploymentDetails.length;
      for (let r = 0; r < rows; r++) {
        const deploymentDetail = $deploymentDetails[r];
        cells[cellId(r, 1)] = deploymentDetail.releaseProjectName;
        cells[cellId(r, 2)] = deploymentDetail.releaseName;
        cells[cellId(r, 3)] = deploymentDetail.releaseNumber;
        cells[cellId(r, 4)] = deploymentDetail.releaseRollback;
        cells[cellId(r, 5)] = deploymentDetail.isCrucial;
      }
    }
  }

  function showToast(type: ToastType, message: string, duration?: number): void {
    new Toast({
      target: document.body,
      props: {
        type,
        message,
        duration,
      },
    });
  }

  function updateDeploymentDetails() {
    $deploymentDetails = Array(rows)
      .fill(null)
      .map((_, row) => new DeploymentDetail(cells[cellId(row, 1)], cells[cellId(row, 2)], cells[cellId(row, 3)], cells[cellId(row, 4)], cells[cellId(row, 5)]))
      .filter((deploymentDetail) =>
        deploymentDetail.releaseNumber && deploymentDetail.releaseRollback && deploymentDetail.releaseNumber < deploymentDetail.releaseRollback
          ? showToast(
              ToastType.Error,
              deploymentDetail.releaseName
                ? `Release number cannot be less than rollback number: Release: ${deploymentDetail.releaseName}`
                : `Release number cannot be less than rollback number`,
            )
          : deploymentDetail.releaseProjectName && deploymentDetail.releaseName,
      );
  }

  onMount(() => {
    setDeploymentDetailsValuesToTable();
  });
</script>

<div class="flex flex-row mb-2 justify-between">
  <div class="flex items-center">
    <a
      href="/Deployment-Details-Template.xlsx"
      class="bg-transparent hover:bg-purple-700 text-purple-900 dark:text-purple-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-purple-800 hover:border-transparent rounded-lg shadow-lg"
    >
      Download Excel Template
    </a>
  </div>

  <div class="flex items-center">
    <button
      disabled={rows >= 25}
      on:click={addRow}
      type="button"
      class="text-gray-900 leading-none bg-gradient-to-r hover:bg-gradient-to-br focus:ring-2 focus:outline-none font-semibold rounded-full text-3xl w-10 h-10 flex items-center justify-center m-1 {rows >=
      25
        ? 'from-gray-500 via-gray-600 to-gray-700 focus:ring-gray-300 dark:focus:ring-gray-800 shadow-lg shadow-gray-500/50 dark:shadow-lg dark:shadow-gray-800/80 cursor-not-allowed'
        : 'from-blue-500 via-blue-600 to-blue-700 focus:ring-blue-300 dark:focus:ring-blue-800 shadow-lg shadow-blue-500/50 dark:shadow-lg dark:shadow-blue-800/80'}"
    >
      +
    </button>

    <button
      disabled={rows <= 0}
      on:click={removeRow}
      type="button"
      class="text-gray-900 leading-none bg-gradient-to-r focus:ring-2 focus:outline-none shadow-lg dark:shadow-lg font-semibold rounded-full text-3xl w-10 h-10 flex items-center justify-center m-1 {rows <=
      0
        ? 'from-gray-500 via-gray-600 to-gray-700 focus:ring-gray-300 dark:focus:ring-gray-800 shadow-lg shadow-gray-500/50 dark:shadow-lg dark:shadow-gray-800/80 cursor-not-allowed'
        : 'from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br focus:ring-red-300 dark:focus:ring-red-800 shadow-red-500/50 dark:shadow-red-800/80 '}"
    >
      -
    </button>
  </div>
</div>

<div class="grid grid-cols-[repeat(6,minmax(0,auto))] gap-1 mb-3">
  {#each headers as header, col}
    <input
      class="read-only text-center font-bold h-8 px-2 text-md border border-gray-800 rounded-md focus:outline-none focus:border-blue-500 disabled:bg-gray-900 dark:disabled:bg-gray-800 {col ===
      0
        ? 'w-12'
        : col === 3 || col === 4 || col === 5
        ? 'w-24'
        : 'w-full'}"
      type="text"
      value={header}
      disabled={true}
      readonly
    />
  {/each}

  {#each Array(rows).fill(null) as _, row}
    {#each Array(columns).fill(null) as _, col}
      {#if col === 0}
        <input
          class="read-only text-center font-bold h-8 px-2 text-md border border-gray-800 rounded-md focus:outline-none focus:border-blue-500 disabled:bg-gray-900 dark:disabled:bg-gray-800 w-12"
          type="text"
          value={row + 1}
          disabled={true}
          readonly
        />
      {:else if col === 5}
        <input
          type="checkbox"
          bind:checked={cells[cellId(row, col)]}
          disabled={disabledColumns.includes(col)}
          class="text-center text-sm border border-gray-800 rounded-md focus:outline-none focus:border-blue-500 w-24"
          on:input={(event) => handleInput(row, col, event)}
        />
      {:else if col === 3 || col === 4}
        <input
          bind:value={cells[cellId(row, col)]}
          disabled={disabledColumns.includes(col)}
          type="number"
          class="text-center h-8 px-2 py-1 text-sm border bg-gray-700 border-gray-800 rounded-md focus:outline-none focus:border-blue-500 w-24"
          on:input={(event) => handleInput(row, col, event)}
        />
      {:else}
        <input
          bind:value={cells[cellId(row, col)]}
          disabled={disabledColumns.includes(col)}
          type="text"
          class="text-center h-8 px-2 py-1 text-sm border bg-gray-700 border-gray-800 rounded-md focus:outline-none focus:border-blue-500 w-full"
          on:input={(event) => handleInput(row, col, event)}
        />
      {/if}
    {/each}
  {/each}
</div>
