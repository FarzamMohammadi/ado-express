<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  export let headers: String[];
  export let rows: number;
  export let columns: number;
  let cells = {};

  function cellId(row, col) {
    return `${row}-${col}`;
  }

  function handleInput(row, col, event) {
    const id = cellId(row, col);
    cells[id] = event.target.value;
    dispatch('cellChange', { row, col, value: event.target.value });
  }

  function exportData() {
    let output = [];
    for (let r = 0; r < rows; r++) {
      let rowData = [];
      for (let c = 0; c < columns; c++) {
        rowData.push(cells[cellId(r, c)] || '');
      }
      output.push(rowData);
    }
    dispatch('dataExport', output);
  }

  $: gridColsClass = `grid grid-cols-[repeat(${columns},minmax(0,1fr))] gap-1`;
</script>

<div class={gridColsClass}>
  {#each headers as header}
    <input
      class="read-only text-center font-bold w-full h-8 px-2 text-md border border-gray-800 rounded-md focus:outline-none focus:border-blue-500 disabled:bg-gray-900"
      type="text"
      value={header}
      disabled={true}
      readonly
    />
  {/each}

  {#each Array(rows).fill(null) as _, row}
    {#each Array(columns).fill(null) as _, col}
      <input
        type="text"
        class="text-center w-full h-8 px-2 py-1 text-sm border bg-gray-700 border-gray-800 rounded-md focus:outline-none focus:border-blue-500"
        on:input={(event) => handleInput(row, col, event)}
      />
    {/each}
  {/each}
</div>