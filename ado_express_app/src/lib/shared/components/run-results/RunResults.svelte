<script lang="ts">
  import DisplayDataInput from './DisplayDataInput.svelte';
  import LiveDeploymentStatus from './LiveDeploymentStatus.svelte';

  import { onDestroy, onMount } from 'svelte';
  import { WebsocketMessageType } from '../../../models/enums/enums';
  import type { GenericWebsocketMessage } from '../../../models/interfaces/generic-websocket-message';
  import type { IDeploymentStatuses } from '../../../models/interfaces/ilive-deployment-details.interface';
  import type { IDisplayedRunResultData } from '../../../models/interfaces/irun-result-data';
  import {
      displayedRunResultData,
      runResultData,
  } from '../../../utils/stores/stores';

  export let runMethod: string = null;
  export let runType: string = null;
  let displayingDeploymentResults = false;
  let deploymentStatuses: IDeploymentStatuses = {};
  let displayItems = [];
  let dotText = '';
  let matrixTheme = true;
  let localResultData: IDisplayedRunResultData[] = [];
  export let displayIdleDots = false;
  let displayDataInputs: string[] = [];

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
    speed = 50,
    delay = 50
  ) {
    if (i < dataInput.length) {
      displayDataInputs[dataIndex] =
        (displayDataInputs[dataIndex] || '') + dataInput[i];
      setTimeout(() => typeEffect(dataInput, i + 1, dataIndex, speed), delay);
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

  let parentWidth = 600;
  let windowWidth = window.innerWidth;

  const updateWindowWidth = () => {
    windowWidth = window.innerWidth;
    parentWidth = Math.min((windowWidth / 2.5) * 0.8, 600); // Adjust the multiplier (0.8) as needed to match the parent div's width
  };

  let ws: WebSocket;

  onMount(() => {
    const websocketUrl = 'ws://localhost:8000/ws/';
    ws = new WebSocket(websocketUrl);

    ws.addEventListener('open', (event) => {
      console.log('WebSocket connection opened:', event);
    });

    ws.addEventListener('message', (event) => {
      const parsedData = JSON.parse(event.data);
      console.log('WebSocket message received:', parsedData);
      if (parsedData.message_type === WebsocketMessageType.Generic) {
        console.log('Got generic message');
        const messageData: GenericWebsocketMessage = JSON.parse(
          parsedData.message
        );
        displayDataInputs = [...displayDataInputs, messageData.message];
        localResultData = [
          ...localResultData,
          {
            text: messageData.message,
            showIdleDots: messageData.showIdleDots,
          },
        ];
      } else if (
        parsedData.message_type === WebsocketMessageType.DeploymentStatus
      ) {
        const messageData = JSON.parse(parsedData.message);
        const liveDeploymentDetails: IDeploymentStatuses = {};

        for (const key in messageData) {
          liveDeploymentDetails[key] = messageData[key];
        }

        deploymentStatuses = {
          ...deploymentStatuses,
          ...liveDeploymentDetails,
        };
      }
    });

    ws.addEventListener('close', (event) => {
      console.log('WebSocket connection closed:', event);
    });

    ws.addEventListener('error', (event) => {
      console.error('WebSocket error:', event);
    });

    localResultData = $displayedRunResultData;
    displayDataInputs = localResultData.map(() => '');

    localResultData.forEach((dataInput, index) => {
      typeEffect(dataInput.text || '', 0, index);
    });

    window.addEventListener('resize', updateWindowWidth);

    // Subscribe to displayedRunResultData store
    unsubscribeDisplayedRunResultData = displayedRunResultData.subscribe(
      ($displayedRunResultData) => {
        if (localResultData.length !== $displayedRunResultData.length) {
          const newIndex = $displayedRunResultData.length - 1;
          localResultData = $displayedRunResultData;

          displayIdleDots = false; // Might adjust later but for now, never show idling dots
          //displayIdleDots = !localResultData[newIndex].showIdleDots;

          displayDataInputs = [...displayDataInputs, ''];
          typeEffect(localResultData[newIndex].text || '', 0, newIndex);
        }
      }
    );

    return () => {
      window.removeEventListener('resize', updateWindowWidth);
    };
  });

  onDestroy(() => {
    unsubscribeDisplayedRunResultData();
  });

  setInterval(updateDots, 400);

  $: {
    updateWindowWidth();
  }

  let prevLocalResultDataLength = localResultData.length;
  let prevDeploymentStatusKeys = new Set(Object.keys(deploymentStatuses));

  $: {
    const isLocalResultDataChanged =
      localResultData.length !== prevLocalResultDataLength;
    const deploymentStatusKeys = new Set(Object.keys(deploymentStatuses));
    const isNewKeyInDeploymentStatus = !Array.from(deploymentStatusKeys).every(
      (key) => prevDeploymentStatusKeys.has(key)
    );

    if (isLocalResultDataChanged) {
      let newItem = {
        type: 'message',
        data: localResultData[localResultData.length - 1],
      };
      displayItems = [...displayItems, newItem];
    }

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

    // Update the previous state
    prevLocalResultDataLength = localResultData.length;
    prevDeploymentStatusKeys = deploymentStatusKeys;

    console.log('displayItems', displayItems);
  }
</script>

<div>
  <div>
    <div class="terminal-container my-4">
      <div
        class="terminal-content flex-col items-center justify-end ml-6 mr-6"
        class:matrix={matrixTheme}
      >
        {#each displayItems as item, i}
          {#if item.type === 'message'}
            <DisplayDataInput
              data={item.data.text}
              showIdleDots={item.data.showIdleDots &&
                i === localResultData.length - 1}
              bind:dotText
            />
          {:else}
            <LiveDeploymentStatus
              key={item.key}
              status={item.value.status}
              percentage={item.value.percentage}
              bind:parentWidth
              bind:matrixTheme
            />
          {/if}
        {/each}
      </div>
    </div>
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
