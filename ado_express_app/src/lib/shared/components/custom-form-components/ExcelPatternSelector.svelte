<script lang="ts">
  import { DeploymentDetails } from '../../../models/classes/deployment-details.model';

  export let headers: String[];
  export let rows: number;
  export let columns = 6;
  export let disabledColumns: number[] = [];
  let cells = {};

  function addRow() {
    rows += 1;
  }

  function cellId(row, col) {
    return `${row}-${col}`;
  }

  function getBooleanValue(isCrucialUserInput: String) {
    const trueValues = ['t', 'true', 'y', 'yes', '1']

    return trueValues.includes(isCrucialUserInput.toLowerCase())
  }

  export function getDeploymentDetails() {
    let rowsToExclude: number[] = [];
    let userInputValues = [];
    const rowNumberCol = 0;
    const isCrucialCol = 5;

    for (let r = 0; r < rows; r++) {
      let rowData = [];

      for (let c = 0; c < columns; c++) {
        if (c != rowNumberCol) {
          let rowColValue = cells[cellId(r, c)] ?? '';

          if (
            rowColValue === '' &&
            c !== isCrucialCol &&
            !disabledColumns.includes(c)
          ) {
            rowsToExclude.push(r);
            continue;
          }
          else{
            rowData.push(rowColValue);
          }
        }
      }
      userInputValues.push(rowData);
    }   
    let deploymentDetails: DeploymentDetails[] = [];

    for(let row = 0; row < userInputValues.length; row++){
      if (!rowsToExclude.includes(row)){
        deploymentDetails.push(new DeploymentDetails(userInputValues[row][0], userInputValues[row][1], userInputValues[row][2], userInputValues[row][3], getBooleanValue(userInputValues[row][4])));
      }
    }

    return deploymentDetails;
  }

  function handleInput(row, col, event) {
    const id = cellId(row, col);
    cells[id] = event.target.value;
  }

  function RemoveRow() {
    rows -= 1;
  }
</script>

<div class="flex flex-row mb-2 items-center justify-end">
  <button
    disabled={rows >= 25}
    on:click={addRow}
    type="button"
    class="text-gray-900 bg-gradient-to-r hover:bg-gradient-to-br focus:ring-2 focus:outline-none font-semibold rounded-full text-3xl w-10 h-10 flex items-center justify-center m-1 {rows >=
    25
      ? 'from-gray-500 via-gray-600 to-gray-700 focus:ring-gray-300 dark:focus:ring-gray-800 shadow-lg shadow-gray-500/50 dark:shadow-lg dark:shadow-gray-800/80 cursor-not-allowed'
      : 'from-blue-500 via-blue-600 to-blue-700 focus:ring-blue-300 dark:focus:ring-blue-800 shadow-lg shadow-blue-500/50 dark:shadow-lg dark:shadow-blue-800/80'}"
  >
    +
  </button>

  <button
    disabled={rows <= 0}
    on:click={RemoveRow}
    type="button"
    class="text-gray-900 bg-gradient-to-r focus:ring-2 focus:outline-none shadow-lg dark:shadow-lg font-semibold rounded-full text-3xl w-10 h-10 flex items-center justify-center m-1 {rows <=
    0
      ? 'from-gray-500 via-gray-600 to-gray-700 focus:ring-gray-300 dark:focus:ring-gray-800 shadow-lg shadow-gray-500/50 dark:shadow-lg dark:shadow-gray-800/80 cursor-not-allowed'
      : 'from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br focus:ring-red-300 dark:focus:ring-red-800 shadow-red-500/50 dark:shadow-red-800/80 '}"
  >
    -
  </button>
</div>

<div class="grid grid-cols-[repeat(6,minmax(0,auto))] gap-1">
  {#each headers as header, col}
    <input
      class="read-only text-center font-bold h-8 px-2 text-md border border-gray-800 rounded-md focus:outline-none focus:border-blue-500 disabled:bg-gray-900 {col ===
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
          class="read-only text-center font-bold h-8 px-2 text-md border border-gray-800 rounded-md focus:outline-none focus:border-blue-500 disabled:bg-gray-900 w-12"
          type="text"
          value={row + 1}
          disabled={true}
          readonly
        />
      {:else if col === 5}
        <input
          type="checkbox"
          value="true"
          disabled={disabledColumns.includes(col)}
          class="text-center text-sm border border-gray-800 rounded-md focus:outline-none focus:border-blue-500 'w-24'"
          on:input={(event) => handleInput(row, col, event)}
        />
      {:else}
        <input
          disabled={disabledColumns.includes(col)}
          type={col === 3 || col === 4 ? 'number' : 'text'}
          class="text-center h-8 px-2 py-1 text-sm border bg-gray-700 border-gray-800 rounded-md focus:outline-none focus:border-blue-500 {col ===
            3 ||
          col === 3 ||
          col === 4
            ? 'w-24'
            : 'w-full'}
            {disabledColumns.includes(col) ? 'bg-transparent border-none' : 'bg-gray-700'}"
          on:input={(event) => handleInput(row, col, event)}
        />
      {/if}
    {/each}
  {/each}
</div>
