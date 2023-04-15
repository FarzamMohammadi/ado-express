<script>
  let matrixTheme = true;

  function toggleTheme() {
    matrixTheme = !matrixTheme;
  }
</script>

<div class="terminal-container my-4">
  <pre
    class="terminal-content"
    class:matrix={matrixTheme}>{"asdfasdfasdfasdfasdfasdfasdfasdfasdfsadf"}</pre>
</div>

{#if matrixTheme}
  <button on:click={toggleTheme}> Matrix Theme On </button>
{:else}
  <button on:click={toggleTheme}> Matrix Theme Off </button>
{/if}

<style>
  .terminal-container {
    background-color: black;
    padding: 20px;
    border-radius: 8px;
    overflow-y: auto;
    width: 100%;
    height: 90vh;
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
