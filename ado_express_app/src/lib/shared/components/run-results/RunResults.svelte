<script lang="ts">
  import { onDestroy, onMount, tick } from 'svelte';
  import { writable } from 'svelte/store';

  import type { IDisplayedRunResultData } from '../../../models/interfaces/idisplayed-run-result-data';
  import type { IDeploymentStatuses } from '../../../models/interfaces/ilive-deployment-details.interface';

  import { displayedRunResultData } from '../../../utils/stores/stores';
  import { deploymentStatusStore } from '../../../utils/websocketStores/deployment-status-store';
  import { genericMessageStore } from '../../../utils/websocketStores/generic-message-store';

  import DisplayDataInput from './DisplayDataInput.svelte';
  import LiveDeploymentStatus from './LiveDeploymentStatus.svelte';
  import ResultDownloadButton from './ResultDownloadButton.svelte';
  import ThemeChangeButton from './ThemeChangeButton.svelte';

  export let displayIdleDots = false;

  let container;
  let deploymentStatuses: IDeploymentStatuses = {};
  let displayDataInputs: string[] = [];
  let displayItems = [];
  let dotText = '';
  let genericMessageDataLength;
  let lastMessageIndex = -1;
  let loadingResultsDisplay = false;
  let localResultData: IDisplayedRunResultData[] = [];
  let localResultDataLength;
  let matrixTheme = true;
  let messageCount = 0;
  let newDeploymentStatuses;
  let newDeploymentStatusKeys;
  let newGenericMessageItems = [];
  let newLocalResultItems = [];
  let percentage = 0;
  let prevDeploymentStatusKeys = new Set(Object.keys(deploymentStatuses));
  let prevDeploymentStatuses: IDeploymentStatuses = {};
  let prevGenericMessageDataLength = 0;
  let prevLocalResultDataLength = localResultData.length;
  let shouldAutoScroll = true;
  let unsubscribeDeploymentStatus;
  let unsubscribeDisplayedRunResultData;

  const displayDataInputsStore = writable([]);

  onMount(() => {
    localResultData = $displayedRunResultData;
    displayDataInputs = new Array(localResultData.length + $genericMessageStore.length).fill('');

    setupAutoScroll();
    setupKeyboardAccessibility();
    setupSubscriptions();

    setInterval(updateDots, 400);
  });

  onDestroy(() => {
    unsubscribeDeploymentStatus();
    unsubscribeDisplayedRunResultData();
  });

  function setupAutoScroll() {
    container.addEventListener('scroll', (e) => {
      const manualScrollThreshold = container.scrollHeight * 0.87;

      if (!loadingResultsDisplay){
        if (container.scrollTop + container.clientHeight < manualScrollThreshold) {
        shouldAutoScroll = false;
        } else if (container.scrollTop + container.clientHeight >= manualScrollThreshold) {
          shouldAutoScroll = true;
        }
      }
    });
  }

  function setupKeyboardAccessibility() {
    container.setAttribute('tabindex', '0');

    container.addEventListener('keydown', (e) => {
      switch (e.key) {
        case 'ArrowUp':
          container.scrollBy({ top: -100, behavior: 'smooth' });
          break;
        case 'ArrowDown':
          container.scrollBy({ top: 100, behavior: 'smooth' });
          break;
      }
    });
  }

  function setupSubscriptions() {
    unsubscribeDeploymentStatus = deploymentStatusStore.subscribe((value) => {
      deploymentStatuses = {
        ...deploymentStatuses,
        ...value,
      };
    });

    unsubscribeDisplayedRunResultData = displayedRunResultData.subscribe(($displayedRunResultData) => {
      if (localResultData.length !== $displayedRunResultData.length) {
        localResultData = $displayedRunResultData;
        displayIdleDots = false;
        displayDataInputs = [...displayDataInputs, ''];
      }
    });
  }

  async function scrollToBottom() {
    if (!shouldAutoScroll || !container) return;

    await tick();
    container.scroll({ top: container.scrollHeight, behavior: 'smooth' });
  }

  function updateDots() {
    if (dotText.length < 3) {
      dotText += '.';
      percentage = percentage + 5;
    } else {
      dotText = '';
    }
  }

  // Reactive updates for in-project message updates, and websocket messages
  $: {
    genericMessageDataLength = $genericMessageStore.length;
    localResultDataLength = localResultData.length;

    if (genericMessageDataLength !== prevGenericMessageDataLength) processGenericMessageUpdates();

    if (localResultDataLength !== prevLocalResultDataLength) processInProjectMessageUpdates();

    if (newLocalResultItems.length > 0 || newGenericMessageItems.length > 0) mergeNewItems();

    newDeploymentStatuses = { ...deploymentStatuses };
    newDeploymentStatusKeys = new Set(Object.keys(newDeploymentStatuses));

    if (newDeploymentStatusKeys.size) processDeploymentStatusUpdates();
  }

  function processInProjectMessageUpdates() {
    for (let i = prevLocalResultDataLength; i < localResultDataLength; i++) {
      let newItem = {
        type: 'message',
        data: localResultData[i],
      };
      newLocalResultItems.push(newItem);
      displayDataInputsStore.update((inputs) => {
        inputs[messageCount] = (inputs[messageCount] || '') + localResultData[i].message;
        return inputs;
      });
      messageCount++;
    }
    prevLocalResultDataLength = localResultDataLength;
  }

  function processGenericMessageUpdates() {
    for (let i = prevGenericMessageDataLength; i < genericMessageDataLength; i++) {
      let newItem = {
        type: 'message',
        data: $genericMessageStore[i],
      };
      newGenericMessageItems.push(newItem);
      displayDataInputsStore.update((inputs) => {
        inputs[messageCount] = (inputs[messageCount] || '') + $genericMessageStore[i].message;
        return inputs;
      });
      messageCount++;
    }
    prevGenericMessageDataLength = genericMessageDataLength;
  }

  function mergeNewItems() {
    displayItems = displayItems.concat(newLocalResultItems, newGenericMessageItems);
    lastMessageIndex = displayItems.length - 1;

    newLocalResultItems = [];
    newGenericMessageItems = [];
  }

  function processDeploymentStatusUpdates() {
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

      scrollToBottom();
    }
  }
</script>

<div class="terminal-container my-4 scroll {matrixTheme ? 'matrix-scrollbar' : 'standard-scrollbar'}" bind:this={container}>
  <div class="terminal-content flex-col items-center justify-end mx-6" class:matrix={matrixTheme}>
    {#each displayItems as item, i}
      {#if item.type === 'message'}
        <DisplayDataInput
          data={item.data.message}
          showIdleDots={item.data.showIdleDots && i === lastMessageIndex}
          bind:dotText={dotText}
          on:scrollDown={scrollToBottom}
          on:loadingResultsDisplay={() => {loadingResultsDisplay = true}}
          on:completedLoadingResultsDisplay={() => {loadingResultsDisplay = false}}
        />
      {:else}
        <LiveDeploymentStatus key={item.key} status={item.value.status} percentage={item.value.percentage} bind:matrixTheme={matrixTheme} />
      {/if}
    {/each}
  </div>
</div>

<div class="flex flex-row items-center justify-between m-2">
  <div>
    <ThemeChangeButton bind:matrixTheme={matrixTheme} />
  </div>

  <div>
    <ResultDownloadButton matrixTheme={matrixTheme} />
  </div>
</div>

<style lang="scss">
.terminal-container {
  background-color: black;
  padding-block: 30px;
  border-radius: 8px;
  overflow-y: auto;
  overflow-x: hidden;
  width: 100%;
  height: 80vh;
}

.terminal-container.scroll::-webkit-scrollbar {
  background: transparent;
	width: 8px;
}

.matrix-scrollbar::-webkit-scrollbar-thumb {
  background: lime;
  border-radius: 2px;
  height: 80px;
}

.matrix-scrollbar.scroll::-webkit-scrollbar-track {
  background: transparent;
  border: 2px solid lime;
}

.standard-scrollbar::-webkit-scrollbar-thumb {
  background: white;
  border-radius: 2px;
  height: 80px;
}

.standard-scrollbar.scroll::-webkit-scrollbar-track {
  background: transparent;
  border: 2px solid white;
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
</style>
