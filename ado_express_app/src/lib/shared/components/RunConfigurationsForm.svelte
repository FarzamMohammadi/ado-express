<script lang="ts">
  import { RunConfigurations } from '../../models/classes/run-configurations.model';
  import type { IDeploymentDetails } from '../../models/interfaces/ideployment-details.interface';
  import type { IExplicitExclusion } from '../../models/interfaces/iexplicit-exclusion.interface';
  import type { IExplicitInclusion } from '../../models/interfaces/iexplicit-inclusion.interface';

  let showPAT = false;

  let hasExplicitReleaseValues = false;
  let explicitReleaseValuesType = '';
  let explicitReleaseValuesReleases = '';
  let crucialReleaseDefinitions: '';
  let organizationUrl = '';
  let personalAccessToken = '';
  let queries: string[] = [];
  let release_name_format = '';
  let release_target_env = '';
  let search_only = false;
  let via_env = false;
  let via_env_latest_release = false;
  let via_env_source_name = '';
  let deployment_details: IDeploymentDetails[] = [];

  function getExplicitReleaseValues() {
    if (!hasExplicitReleaseValues) return null;

    const selectedRelease: string[] = explicitReleaseValuesReleases.split(',');
    if (selectedRelease.length === 0) return null;

    let explicitReleaseValues: any = null;

    if (explicitReleaseValuesType === 'include') {
      explicitReleaseValues = {
        inclusion: selectedRelease,
      } as IExplicitInclusion;
    } else if (explicitReleaseValuesType === 'exclude') {
      explicitReleaseValues = {
        exclusion: selectedRelease,
      } as IExplicitExclusion;
    }

    return explicitReleaseValues;
  }

  function handleSubmit() {
    const runConfigurations = new RunConfigurations(
      getExplicitReleaseValues(),
      crucialReleaseDefinitions?.split(',') ?? null,
      organizationUrl,
      personalAccessToken,
      queries,
      release_name_format,
      release_target_env,
      search_only,
      via_env,
      via_env_latest_release,
      via_env_source_name,
      deployment_details
    );

    console.log(runConfigurations);
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <div class="flex flex-col">

    <div class="explicit-release-values flex-row mb-4">
      <div class="flex justify-between mb-3">
        <!-- TODO: Keep together and then separate on select -->
        <label for="explicitReleaseValues" class="font-bold"
          >Explicit Release Values</label
        >

        <input type="checkbox" bind:checked={hasExplicitReleaseValues} />
      </div>

      {#if hasExplicitReleaseValues}
        <div class="flex justify-center mb-2">
          <label class="pr-3">
            <input
              type="radio"
              name="explicitReleaseValuesOptions"
              value="include"
              bind:group={explicitReleaseValuesType}
            />
            Explicitly Include
          </label>

          <label>
            <input
              type="radio"
              name="explicitReleaseValuesOptions"
              value="exclude"
              bind:group={explicitReleaseValuesType}
            />
            Explicitly Exclude
          </label>
        </div>

        <input
          type="text"
          id="explicitReleaseValuesReleases"
          class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
          bind:value={explicitReleaseValuesReleases}
        />
      {/if}
    </div>

    <div class="crucial-release-definitions mb-4">
      <label for="crucialReleaseDefinitions" class="font-bold mb-2"
        >Crucial Release Definitions</label
      >
      <input
        type="text"
        id="crucialReleaseDefinitions"
        class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
        bind:value={crucialReleaseDefinitions}
      />
    </div>

    <div class="organization-url mb-4">
      <label for="organizationUrl" class="block font-bold mb-2"
        >Organization Url</label
      >
      <input
        type="url"
        id="organizationUrl"
        class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
        bind:value={organizationUrl}
      />
    </div>

    <div class="perosnal-access-token mb-4">
      <label for="personalAccessToken" class="block font-bold mb-2">Personal Access Token</label>
      <div class="relative">
        {#if showPAT}
        <input
          type="text"
          id="personalAccessToken"
          class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
          autocomplete="off"
          bind:value={personalAccessToken}
        />
      {:else}
        <input
          type="password"
          id="personalAccessToken"
          class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
          autocomplete="off"
          bind:value={personalAccessToken}
        />
      {/if}
      <button
        class="absolute inset-y-0 right-0 flex items-center px-2 text-gray-700"
        on:click={() => (showPAT = !showPAT)}
      >
        {#if showPAT}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="feather feather-eye"
          >
            <path
              d="M23.928 11.036c-.182-.28-4.441-6.936-11.928-6.936s-11.746 6.656-11.928 6.936a.5.5 0 000 .928C1.184 12.964 5.439 19.5 12 19.5s10.816-6.536 11.928-7.536a.5.5 0 000-.928zM12 16.5a4.5 4.5 0 110-9 4.5 4.5 0 010 9z"
            />
          </svg>
        {:else}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="feather feather-eye-slash"
          >
            <path
              d="M23.928 11.036c-.182-.28-4.441-6.936-11.928-6.936s-11.746 6.656-11.928 6.936a.5.5 0 000 .928C1.184 12.964 5.439 19.5 12 19.5s10.816-6.536 11.928-7.536a.5.5 0 000-.928zM2.5 2.5l19 19M2.5 21.5l19-19"
            />
          </svg>
        {/if}
      </button>
      </div>
    </div>

    <div class="flex justify-center">
      <button
        type="submit"
        class="bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Send Message
      </button>
    </div>
  </div>
</form>
