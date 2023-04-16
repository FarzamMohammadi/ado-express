<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import type { IRunResultData } from '../../models/interfaces/irun-result-data';
  import { runResultData, running } from '../../utils/stores/stores';

  let matrixTheme = true;
  let localResultData: IRunResultData[] = [];
  export let displayIdleDots = false;
  let displayDataInputs: string[] = [];

  function typeEffect(
    dataInput: string,
    i: number,
    dataIndex: number,
    speed = 50,
    delay = 50
  ) {
    if (i < dataInput.length) {
      displayDataInputs[dataIndex] =
        (displayDataInputs[dataIndex] || '') + dataInput[i];
      setTimeout(() => typeEffect(dataInput, i + 1, dataIndex, speed), delay);
    }
  }

  function updateDots() {
    if (dotText.length < 3) {
      dotText += '.';
    } else {
      dotText = '';
    }
  }
  function toggleTheme() {
    matrixTheme = !matrixTheme;
  }

  let unsubscribeRunResultData;

  onMount(() => {
    localResultData = $runResultData;
    displayDataInputs = localResultData.map(() => '');

    localResultData.forEach((dataInput, index) => {
      typeEffect(dataInput.text || '', 0, index);
    });

    // Subscribe to runResultData store
    unsubscribeRunResultData = runResultData.subscribe(($runResultData) => {
      if (localResultData.length !== $runResultData.length) {
        const newIndex = $runResultData.length - 1;
        localResultData = $runResultData;
        
        displayIdleDots = false; // Might adjust later but for now, never show idling dots
        //displayIdleDots = !localResultData[newIndex].showIdleDots;

        displayDataInputs = [...displayDataInputs, ''];
        typeEffect(localResultData[newIndex].text || '', 0, newIndex);
      }
    });
  });

  onDestroy(() => {
    // Unsubscribe from runResultData store
    unsubscribeRunResultData();
  });

  let dotText = '';
  setInterval(updateDots, 400);
</script>

<div>
  <div>
    <div class="terminal-container my-4">
      <div
        class="terminal-content flex-col items-center justify-end ml-6 mr-6"
        class:matrix={matrixTheme}
      >
        <div class="dataInput-container">
          {#each displayDataInputs as dataInput, i}
            <span>
              {dataInput}
              {#if localResultData[i].showIdleDots && i + 1 == displayDataInputs.length}{dotText}{/if}
            </span>
          {/each}
        </div>
        {#if $running && displayIdleDots}
          <br />{dotText}
        {/if}
      </div>
    </div>
  </div>

  {#if matrixTheme}
    <button on:click={toggleTheme}> Matrix Theme: ON </button>
  {:else}
    <button on:click={toggleTheme}> Matrix Theme: OFF </button>
  {/if}
</div>

<style lang="scss">
  .dataInput-container {
    display: block;
    word-break: break-all;
  }

  .terminal-container {
    background-color: black;
    padding-block: 20px;
    border-radius: 8px;
    overflow-y: auto;
    width: 100%;
    height: 80vh;
  }

  .terminal-content {
    font-family: 'Courier New', monospace;
    font-size: 16px;
    white-space: pre-wrap;
    word-wrap: break-word;
    text-align: left;
  }

  .terminal-content.matrix {
    color: lime;
  }

  .terminal-content:not(.matrix) {
    color: white;
  }

  button {
    margin-top: 8px;
    font-size: 14px;
    cursor: pointer;
  }
</style>
