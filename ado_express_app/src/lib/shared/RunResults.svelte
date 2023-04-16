<script lang="ts">
  import { runResultData, running } from '../utils/stores/stores';

  let matrixTheme = true;
  let localResultData = [];
  let displayIdleDots = true;
  let lastDataInput = '';

  $: {
    localResultData = $runResultData;
    lastDataInput = localResultData[localResultData.length - 1];
    displayIdleDots = !lastDataInput?.includes('-ADDTHREEDOTSHERE');
  }

  function toggleTheme() {
    matrixTheme = !matrixTheme;
  }

  // runResultData.update((data) => [...data, 'New Item-ADDTHREEDOTSHERE']);
  let dotText = '';
  const updateDots = () => {
    if (dotText.length < 3) {
      dotText += '.';
    } else {
      dotText = '';
    }
  };

  setInterval(updateDots, 400);
</script>

<div>
  <div class="terminal-container my-4">
    <div
      class="terminal-content flex-col items-center justify-end ml-6"
      class:matrix={matrixTheme}
    >
      <span>
        {#each localResultData as dataInput, i}
          {#if i + 1 == localResultData.length}
            {#if dataInput.includes('-ADDTHREEDOTSHERE')}
              <br />{dataInput.replace('-ADDTHREEDOTSHERE', '')}{dotText}
            {:else}
              <br />{dataInput}
            {/if}
          {:else if dataInput.includes('-ADDTHREEDOTSHERE')}
            <br />{dataInput.replace('-ADDTHREEDOTSHERE', '')}
          {:else}
            <br />{dataInput}
          {/if}
        {/each}
      </span>
      {#if $running && displayIdleDots}
        <br />{dotText}
      {/if}
    </div>
  </div>

  {#if matrixTheme}
    <button on:click={toggleTheme}> Matrix Theme: ON </button>
  {:else}
    <button on:click={toggleTheme}> Matrix Theme: OFF </button>
  {/if}
</div>

<style lang="scss">
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
