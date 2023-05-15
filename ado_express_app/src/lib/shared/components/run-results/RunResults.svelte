<script lang="ts">
  import { writable } from 'svelte/store';
  import DisplayDataInput from './DisplayDataInput.svelte';
  import LiveDeploymentStatus from './LiveDeploymentStatus.svelte';

  import { onDestroy, onMount } from 'svelte';
  import type { IDeploymentStatuses } from '../../../models/interfaces/ilive-deployment-details.interface';
  import type { IDisplayedRunResultData } from '../../../models/interfaces/irun-result-data';
  import {
      displayedRunResultData,
      runResultData,
  } from '../../../utils/stores/stores';
  import { deploymentStatusStore } from '../../../utils/websocketStores/deployment-status-store';
  import { genericMessageStore } from '../../../utils/websocketStores/generic-message-store';

  const displayDataInputsStore = writable([]);
  let displayItems = [];
  let dotText = '';
  let matrixTheme = true;
  let localResultData: IDisplayedRunResultData[] = [];
  export let displayIdleDots = false;
  let displayDataInputs: string[] = [];
  displayDataInputsStore.subscribe((value) => {
    console.log(value);
    console.log(displayItems);
    displayDataInputs = value;
  });
  let deploymentStatuses: IDeploymentStatuses = {};
  let prevGenericMessageDataLength = 0;

  let newLocalResultItems = [];
  let newGenericMessageItems = [];
  let lastMessageIndex = -1;

  const unsubscribeDeploymentStatus = deploymentStatusStore.subscribe(
    (value) => {
      deploymentStatuses = {
        ...deploymentStatuses,
        ...value,
      };
    }
  );

  function downloadResultsAsJSONFile(): void {
    const jsonString = JSON.stringify($runResultData);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'results.json';
    anchor.click();

    setTimeout(() => {
      URL.revokeObjectURL(url);
      anchor.remove();
    }, 0);
  }

  let percentage = 0;

  function updateDots() {
    if (dotText.length < 3) {
      dotText += '.';
      percentage = percentage + 5;
    } else {
      dotText = '';
    }
  }
  function toggleTheme() {
    matrixTheme = !matrixTheme;
  }

  let unsubscribeDisplayedRunResultData;

  onMount(() => {
    localResultData = $displayedRunResultData;
    displayDataInputs = new Array(
      localResultData.length + $genericMessageStore.length
    ).fill('');

    unsubscribeDisplayedRunResultData = displayedRunResultData.subscribe(
      ($displayedRunResultData) => {
        if (localResultData.length !== $displayedRunResultData.length) {
          localResultData = $displayedRunResultData;
          displayIdleDots = false;
          displayDataInputs = [...displayDataInputs, ''];
        }
      }
    );
  });

  onDestroy(() => {
    unsubscribeDeploymentStatus();
    unsubscribeDisplayedRunResultData();
  });

  setInterval(updateDots, 400);

  let prevLocalResultDataLength = localResultData.length;
  let prevDeploymentStatusKeys = new Set(Object.keys(deploymentStatuses));
  let prevDeploymentStatuses: IDeploymentStatuses = {};
  let messageCount = 0;

  // Reactive updates for in file localResultData update & deploymentStatuses update
  $: {
    const localResultDataLength = localResultData.length;
    const genericMessageDataLength = $genericMessageStore.length;

    // Process new localResultData items
    if (localResultDataLength !== prevLocalResultDataLength) {
      for (let i = prevLocalResultDataLength; i < localResultDataLength; i++) {
        let newItem = {
          type: 'message',
          data: localResultData[i],
        };
        newLocalResultItems.push(newItem);
        displayDataInputsStore.update((inputs) => {
          inputs[messageCount] =
            (inputs[messageCount] || '') + localResultData[i].message;
          return inputs;
        });
        messageCount++;
      }
      prevLocalResultDataLength = localResultDataLength;
    }

    // Process new genericMessageData items
    if (genericMessageDataLength !== prevGenericMessageDataLength) {
      for (
        let i = prevGenericMessageDataLength;
        i < genericMessageDataLength;
        i++
      ) {
        let newItem = {
          type: 'message',
          data: $genericMessageStore[i],
        };
        newGenericMessageItems.push(newItem);
        displayDataInputsStore.update((inputs) => {
          inputs[messageCount] =
            (inputs[messageCount] || '') + $genericMessageStore[i].message;
          return inputs;
        });
        messageCount++;
      }
      prevGenericMessageDataLength = genericMessageDataLength;
    }

    // Merge new items into displayItems
    if (newLocalResultItems.length > 0 || newGenericMessageItems.length > 0) {
      displayItems = displayItems.concat(
        newLocalResultItems,
        newGenericMessageItems
      );

      // Update lastMessageIndex
      lastMessageIndex = displayItems.length - 1;

      newLocalResultItems = [];
      newGenericMessageItems = [];
    }
  }

  $: {
    const newDeploymentStatuses = { ...deploymentStatuses };
    const newDeploymentStatusKeys = new Set(Object.keys(newDeploymentStatuses));

    let hasChanges = false;
    for (const key of newDeploymentStatusKeys) {
      // Check if there's a new key in deploymentStatuses
      if (!prevDeploymentStatusKeys.has(key)) {
        let newItem = {
          type: 'deploymentStatus',
          key: key,
          value: newDeploymentStatuses[key],
        };
        displayItems = [...displayItems, newItem];
        hasChanges = true;
      }
      // Check if a deployment status has been updated
      else if (prevDeploymentStatuses[key] !== newDeploymentStatuses[key]) {
        displayItems = displayItems.map((item) => {
          if (item.type === 'deploymentStatus' && item.key === key) {
            return { ...item, value: newDeploymentStatuses[key] };
          }
          return item;
        });
        hasChanges = true;
      }
    }

    // Update the previous state only when there are changes
    if (hasChanges) {
      prevDeploymentStatusKeys = newDeploymentStatusKeys;
      prevDeploymentStatuses = newDeploymentStatuses;
    }
  }
</script>

<div class="terminal-container my-4">
  <div
    class="terminal-content flex-col items-center justify-end mx-6"
    class:matrix={matrixTheme}
  >
    {#each displayItems as item, i}
      {#if item.type === 'message'}
        <DisplayDataInput
          data={item.data.message}
          showIdleDots={item.data.showIdleDots && i === lastMessageIndex}
          bind:dotText
        />
      {:else}
        <LiveDeploymentStatus
          key={item.key}
          status={item.value.status}
          percentage={item.value.percentage}
          bind:matrixTheme
        />
      {/if}
    {/each}
  </div>
</div>

<div class="flex flex-row items-center justify-between">
  <div>
    {#if matrixTheme}
      <button
        class="bg-transparent hover:bg-green-700 text-green-900 dark:text-green-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-green-800 hover:border-transparent rounded-lg shadow-lg"
        on:click={toggleTheme}>Retro Theme: -ON-</button
      >
    {:else}
      <button
        class="bg-transparent hover:bg-purple-700 text-purple-900 dark:text-purple-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-purple-800 hover:border-transparent rounded-lg shadow-lg"
        on:click={toggleTheme}>Retro Theme: -OFF-</button
      >
    {/if}
  </div>
  <div>
    {#if matrixTheme}
      <button
        class="bg-transparent hover:bg-green-700 text-green-900 dark:text-green-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-green-800 hover:border-transparent rounded-lg shadow-lg"
        on:click={downloadResultsAsJSONFile}>Download Results JSON</button
      >
    {:else}
      <button
        class="bg-transparent hover:bg-purple-700 text-purple-900 dark:text-purple-500 font-semibold hover:text-white dark:hover:text-white py-2 px-4 border border-purple-800 hover:border-transparent rounded-lg shadow-lg"
        on:click={downloadResultsAsJSONFile}>Download Results JSON</button
      >
    {/if}
  </div>
</div>

<style lang="scss">
  .terminal-container {
    background-color: black;
    padding-block: 30px;
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
