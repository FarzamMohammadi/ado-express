<script lang="ts">
  import { RunConfigurations } from '../../models/classes/run-configurations.model';
  import { ToastType } from '../../models/enums/enums';
  import type { IDeploymentDetails } from '../../models/interfaces/ideployment-details.interface';
  import type { IExplicitExclusion } from '../../models/interfaces/iexplicit-exclusion.interface';
  import type { IExplicitInclusion } from '../../models/interfaces/iexplicit-inclusion.interface';
  import CustomCheckboxInput from './custom-form-components/CustomCheckboxInput.svelte';
  import CustomPasswordInput from './custom-form-components/CustomPasswordInput.svelte';
  import CustomTextInput from './custom-form-components/CustomTextInput.svelte';
  import CustomUrlInput from './custom-form-components/CustomUrlInput.svelte';
  import RunSpecifierDropdown from './RunSpecifierDropdown.svelte';
  import Toast from './Toast.svelte';

  let runType = null;
  let runMethod = null;

  let hasExplicitReleaseValues = false;
  let explicitReleaseValuesType = '';
  let explicitReleaseValuesReleases = '';
  let crucialReleaseDefinitions: '';
  let organizationUrl = '';
  let personalAccessToken = '';
  let queries: '';
  let releaseNameFormat = 'Release-$(rev:r)';
  let releaseTargetEnv = '';
  let viaEnv = false;
  let viaEnvLatestRelease = false;
  let viaEnvSourceName = '';
  let deployment_details: IDeploymentDetails[] = [];

  function getExplicitReleaseValues() {
    if (!hasExplicitReleaseValues) return null;

    const selectedRelease: string[] = explicitReleaseValuesReleases
      .split(',')
      .map((s) => s.trim());

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
    validateForm();

    const runConfigurations = new RunConfigurations(
      getExplicitReleaseValues(),
      crucialReleaseDefinitions?.split(',').map((s) => s.trim()) ?? null,
      organizationUrl.trim(),
      personalAccessToken.trim(),
      queries?.split(',').map((s) => s.trim()) ?? null,
      releaseNameFormat.trim(),
      releaseTargetEnv.trim(),
      isSearchOnly(),
      viaEnv,
      viaEnvLatestRelease,
      viaEnvSourceName.trim(),
      deployment_details
    );

    console.log(runConfigurations);
  }

  function isSearchOnly() {
    if (runType && runType === 'Search') {
      return true;
    } else if (runType && runType === 'Deploy') {
      return false;
    }
  }

  function validateForm(): void {
    new Toast({
      target: document.body,
      props: {
        message: 'Invalid Form',
        type: ToastType.Error,
        duration: 1000,
      },
    });
  }
</script>

<div class="mb-4 relative z-10">
  <RunSpecifierDropdown
    bind:selectedCategoryName={runType}
    bind:selectedTask={runMethod}
  />
</div>

<form on:submit|preventDefault={handleSubmit}>
  <div class="flex flex-col">
    <CustomTextInput
      label="Crucial Release Definitions"
      id="crucialReleaseDefinitions"
      bind:bindValue={crucialReleaseDefinitions}
    />
    <CustomUrlInput
      label="Organization Url"
      id="organizationUrl"
      bind:bindValue={organizationUrl}
    />
    <CustomPasswordInput
      label="Personal Access Token"
      id="personalAccessToken"
      bind:bindValue={personalAccessToken}
    />
    <CustomTextInput label="Queries" id="queries" bind:bindValue={queries} />
    <CustomTextInput
      label="Release Name Format"
      id="releaseNameFormat"
      bind:bindValue={releaseNameFormat}
    />
    <CustomTextInput
      label="Release Target Environment"
      id="releaseTargetEnv"
      bind:bindValue={releaseTargetEnv}
    />
    <CustomTextInput
      label="Release Source Environment"
      id="viaEnvSourceName"
      bind:bindValue={viaEnvSourceName}
    />
    <CustomCheckboxInput
      label="Via Release Environment"
      id="viaEnv"
      bind:bindValue={viaEnv}
    />
    <CustomCheckboxInput
      label="Via Latest in Release Environment"
      id="viaEnvLatestRelease"
      bind:bindValue={viaEnvLatestRelease}
    />

    <div class="w-full items-center border-2 border-gray-200 rounded dark:border-gray-700 mt-2 mb-2" id="hasExplicitReleaseValues">
      <div class="flex justify-between items-center">
        <label for="hasExplicitReleaseValues" class="py-2 m-2 font-bold">Explicit Release Values</label>
        <input bind:checked={hasExplicitReleaseValues} id="bordered-checkbox-1" type="checkbox" name="hasExplicitReleaseValues" class="w-4 h-4 m-2 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
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
        <div class="grid justify-items-center w-full">
          <CustomTextInput
          label="Releases"
          id="explicitReleaseValuesReleases"
          bind:bindValue={explicitReleaseValuesReleases}
        />
        </div>
      {/if}
    </div>


    <div class="flex justify-center">
      <button
        type="submit"
        class="bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Run ADO Express
      </button>
    </div>
  </div>
</form>
