<script lang="ts">
    import CustomTextInput from './inputs/CustomTextInput.svelte';

  export let hasExplicitReleaseValues;
  export let explicitReleaseValuesType;
  export let explicitReleaseValuesReleases;
  export let showInput;
</script>

{#if showInput}
  <div
    class="items-center border-2 border-gray-600 rounded dark:border-gray-500 mb-2"
    id="hasExplicitReleaseValues"
  >
    <div
      class="flex justify-between items-center px-1"
      on:click={() => (hasExplicitReleaseValues = !hasExplicitReleaseValues)}
      on:keypress={() => (hasExplicitReleaseValues = !hasExplicitReleaseValues)}
    >
      <label for="hasExplicitReleaseValues" class="py-2 m-2 font-bold"
        >Explicit Release Values</label
      >
      <input
        bind:checked={hasExplicitReleaseValues}
        id="hasExplicitReleaseValues"
        type="checkbox"
        name="hasExplicitReleaseValues"
        class="w-4 h-4 m-2 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
      />
    </div>

    {#if hasExplicitReleaseValues}
      <div class="flex justify-center">
        <label class="pr-3">
          <input
            type="radio"
            name="explicitReleaseValuesOptions"
            value="include"
            bind:group={explicitReleaseValuesType}
          />
          Include
        </label>

        <label>
          <input
            type="radio"
            name="explicitReleaseValuesOptions"
            value="exclude"
            bind:group={explicitReleaseValuesType}
          />
          Exclude
        </label>
      </div>
      <div class="w-full flex justify-center items-center">
        <div class="w-full pr-4 pl-4">
          <CustomTextInput
            label="Releases"
            id="explicitReleaseValuesReleases"
            required={hasExplicitReleaseValues}
            showInput={hasExplicitReleaseValues}
            bind:bindValue={explicitReleaseValuesReleases}
          />
        </div>
      </div>
    {/if}
  </div>
{/if}
