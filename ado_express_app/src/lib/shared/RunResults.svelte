<script lang="ts">
  import { runResultData } from '../utils/stores/stores';
  let matrixTheme = true;
  let localResultData = [];
  let displayIdleDots = true;
  let lastDataInput = '';

  // Subscribe to changes in $runResultData
  $: {
    localResultData = $runResultData;
    lastDataInput = localResultData[localResultData.length - 1];
    displayIdleDots = !lastDataInput.includes('-ADDTHREEDOTSHERE');
  }

  function toggleTheme() {
    matrixTheme = !matrixTheme;
  }

  runResultData.update((data) => [...data, 'New Item-ADDTHREEDOTSHERE', "da,asdfasfd"]);
  runResultData.update((data) => [...data, "da,123d"]);

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
    <pre class="terminal-content" class:matrix={matrixTheme}>
      {#each localResultData as dataInput}
          {#if dataInput.includes('-ADDTHREEDOTSHERE')}
            {dataInput.replace('-ADDTHREEDOTSHERE', '')} 
              {#if lastDataInput === dataInput}
                {dotText}
              {/if}
          {:else}
            {'\n'}{dataInput}
          {/if}
      {/each}
      {#if displayIdleDots}
        {dotText}
      {/if}
    </pre>    
  </div>

  {#if matrixTheme}
    <button on:click={toggleTheme}> Matrix Theme On </button>
  {:else}
    <button on:click={toggleTheme}> Matrix Theme Off </button>
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
