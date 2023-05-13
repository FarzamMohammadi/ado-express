<script lang="ts">
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

  let displayItems = [];
  let dotText = '';
  let matrixTheme = true;
  let localResultData: IDisplayedRunResultData[] = [];
  export let displayIdleDots = false;
  let displayDataInputs: string[] = [];
  let deploymentStatuses: IDeploymentStatuses = {};
  let prevGenericMessageDataLength = 0;
  let genericMessageData: IDisplayedRunResultData[] = [];

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

  function typeEffect(
    dataInput: string,
    i: number,
    dataIndex: number,
    delay = 15
  ) {
    if (i < dataInput.length) {
      displayDataInputs[dataIndex] =
        (displayDataInputs[dataIndex] || '') + dataInput[i];
      setTimeout(() => typeEffect(dataInput, i + 1, dataIndex, 10), delay);
    }
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
      localResultData.length + genericMessageData.length
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

  const unsubscribeGenericMessage = genericMessageStore.subscribe((value) => {
    genericMessageData = [...value];
    displayDataInputs = [
      ...displayDataInputs,
      ...new Array(value.length).fill(''),
    ];
  });

  onDestroy(() => {
    unsubscribeGenericMessage();
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
    const localResultDataChanged =
      localResultData.length !== prevLocalResultDataLength;
    const genericMessageDataChanged =
      genericMessageData.length !== prevGenericMessageDataLength;

    if (localResultDataChanged) {
      const prevLength = prevLocalResultDataLength;
      prevLocalResultDataLength = localResultData.length;

      for (let i = prevLength; i < localResultData.length; i++) {
        let newItem = {
          type: 'message',
          data: localResultData[i],
        };
        newLocalResultItems = [...newLocalResultItems, newItem];
        typeEffect(localResultData[i].message || '', 0, messageCount++);
      }
    }

    if (genericMessageDataChanged) {
      const prevLength = prevGenericMessageDataLength;
      prevGenericMessageDataLength = genericMessageData.length;

      for (let i = prevLength; i < genericMessageData.length; i++) {
        let newItem = {
          type: 'message',
          data: genericMessageData[i],
        };
        newGenericMessageItems = [...newGenericMessageItems, newItem];
        typeEffect(genericMessageData[i].message || '', 0, messageCount++);
      }
    }

    // Merge new items into displayItems separately
    displayItems = [
      ...displayItems,
      ...newLocalResultItems,
      ...newGenericMessageItems,
    ];

    // Update lastMessageIndex after merging the new items
    lastMessageIndex = displayItems.reduce((prev, current, index) => {
      return current.type === 'message' ? index : prev;
    }, lastMessageIndex);

    newLocalResultItems = [];
    newGenericMessageItems = [];

    const deploymentStatusKeys = new Set(Object.keys(deploymentStatuses));
    const isNewKeyInDeploymentStatus = !Array.from(deploymentStatusKeys).every(
      (key) => prevDeploymentStatusKeys.has(key)
    );
    const isDeploymentStatusUpdated = Array.from(deploymentStatusKeys).some(
      (key) =>
        prevDeploymentStatusKeys.has(key) &&
        deploymentStatuses[key] !== prevDeploymentStatuses[key]
    );

    if (isNewKeyInDeploymentStatus) {
      let newKey = Array.from(deploymentStatusKeys).find(
        (key) => !prevDeploymentStatusKeys.has(key)
      );
      let newItem = {
        type: 'deploymentStatus',
        key: newKey,
        value: deploymentStatuses[newKey],
      };
      displayItems = [...displayItems, newItem];
    }

    if (isDeploymentStatusUpdated) {
      displayItems = displayItems.map((item) => {
        if (
          item.type === 'deploymentStatus' &&
          deploymentStatuses[item.key] !== item.value
        ) {
          return { ...item, value: deploymentStatuses[item.key] };
        }
        return item;
      });
    }

    // Update the previous state
    prevLocalResultDataLength = localResultData.length;
    prevDeploymentStatusKeys = deploymentStatusKeys;
    prevDeploymentStatuses = { ...deploymentStatuses };
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
          data={displayDataInputs[i]}
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
