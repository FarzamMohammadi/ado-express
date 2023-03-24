<script lang="ts">
  import { RunConfigurations } from "../../models/classes/run-configurations.model";
  import type { IDeploymentDetails } from "../../models/interfaces/ideployment-details.interface";
  import type { IExplicitExclusion } from "../../models/interfaces/iexplicit-exclusion.interface";
  import type { IExplicitInclusion } from "../../models/interfaces/iexplicit-inclusion.interface";

  let hasExplicitReleaseValues = false;
  let explicitReleaseValuesType = "";
  let explicitReleaseValuesReleases = "";
  let crucialReleaseDefinitions: string[] = [];
  let organization_url = "";
  let personal_access_token = "";
  let queries: string[] = [];
  let release_name_format = "";
  let release_target_env = "";
  let search_only = false;
  let via_env = false;
  let via_env_latest_release = false;
  let via_env_source_name = "";
  let deployment_details: IDeploymentDetails[] = [];

  function getExplicitReleaseValues() {
    if (!hasExplicitReleaseValues) return null;

    const selectedRelease: string[] = explicitReleaseValuesReleases.split(",");
    if (selectedRelease.length === 0) return null;

    let explicitReleaseValues: any = null;

    if (explicitReleaseValuesType === "include") {
      explicitReleaseValues = {
        inclusion: selectedRelease,
      } as IExplicitInclusion;
    } else if (explicitReleaseValuesType === "exclude") {
      explicitReleaseValues = {
        exclusion: selectedRelease,
      } as IExplicitExclusion;
    }

    return explicitReleaseValues;
  }

  function handleSubmit() {
    const runConfigurations = new RunConfigurations(
      getExplicitReleaseValues(),
      crucialReleaseDefinitions,
      organization_url,
      personal_access_token,
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
        <label for="name" class="font-bold"> Explicit Release Values </label>

        <input type="checkbox" bind:checked={hasExplicitReleaseValues} />
      </div>

      {#if hasExplicitReleaseValues}
        <div class="flex justify-center mb-2">
          <label class="pr-3">
            <input
              type="radio"
              name="options"
              value="include"
              bind:group={explicitReleaseValuesType}
            />
            Explicitly Include
          </label>

          <label>
            <input
              type="radio"
              name="options"
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

    <div class="mb-4">
      <div />
      <label for="crucial_release_definitions" class="font-bold mb-2"
        >Crucial Release Definitions</label
      >
      <input
        type="text"
        id="crucial_release_definitions"
        class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
        bind:value={crucialReleaseDefinitions}
      />
    </div>

    <div class="mb-4">
      <label for="email" class="block font-bold mb-2">organization_url</label>
      <input
        type="email"
        id="email"
        class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
        bind:value={organization_url}
      />
    </div>

    <div class="mb-4">
      <label for="message" class="block font-bold mb-2"
        >personal_access_token</label
      >
      <textarea
        id="message"
        class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
        rows="5"
        bind:value={personal_access_token}
      />
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
