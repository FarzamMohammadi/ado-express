<script lang="ts">
  import { ADOExpressApi } from '../../core/services/api';
  import { RunConfigurations } from '../../models/classes/run-configurations.model';
  import { RunType, ToastType } from '../../models/enums/enums';
  import type { IDeploymentDetails } from '../../models/interfaces/ideployment-details.interface';
  import type { IExplicitExclusion } from '../../models/interfaces/iexplicit-exclusion.interface';
  import type { IExplicitInclusion } from '../../models/interfaces/iexplicit-inclusion.interface';
  import CustomCheckboxInput from './custom-form-components/CustomCheckboxInput.svelte';
  import CustomPasswordInput from './custom-form-components/CustomPasswordInput.svelte';
  import CustomRunSpecifierDropdown from './custom-form-components/CustomRunSpecifierDropdown.svelte';
  import CustomTextInput from './custom-form-components/CustomTextInput.svelte';
  import CustomUrlInput from './custom-form-components/CustomUrlInput.svelte';
  import Toast from './utils/Toast.svelte';

  let runType = null;
  let runMethod = null;
  let showSubmitButton = true;
  let submitButtonLabel = 'Run ADO Express';
  // RunConfigurations
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

  function isNullOrUndefined(variable: any): Boolean {
    if (variable === null || variable === undefined) {
      return true;
    }
    return false;
  }

  function handleSubmit() {
    if (isNullOrUndefined(runType) || isNullOrUndefined(runMethod)) {
      new Toast({
        target: document.body,
        props: {
          type: ToastType.Warning,
          message: 'Please complete the run type selection at the top'
        },
      });
      return;
    }

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

    const adoExpressApi = new ADOExpressApi();
    console.log(adoExpressApi.runADOExpress(runConfigurations));
  }

  function isSearchOnly() {
    if (runType && runType === 'Search') {
      return true;
    } else if (runType && runType === 'Deploy') {
      return false;
    }
  }

  function onRunTypeSelection(runType) {
    if (runType === RunType.Search) {
      submitButtonLabel = 'Run the Search';
    } else if (runType === RunType.Deploy) {
      submitButtonLabel = 'Run the Deployment';
    }
  }

  $: onRunTypeSelection(runType);
</script>

<svelte:head>
  <link
    rel="stylesheet"
    href="https://unpkg.com/mono-icons@1.0.5/iconfont/icons.css"
  />
</svelte:head>

<div class="mb-16 relative z-10">
  <CustomRunSpecifierDropdown
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
      required={true}
      bind:bindValue={organizationUrl}
    />
    <CustomPasswordInput
      label="Personal Access Token"
      id="personalAccessToken"
      required={true}
      bind:bindValue={personalAccessToken}
    />
    <CustomTextInput label="Queries" id="queries" bind:bindValue={queries} />
    <CustomTextInput
      label="Release Name Format"
      id="releaseNameFormat"
      required={true}
      bind:bindValue={releaseNameFormat}
    />
    <CustomTextInput
      label="Release Target Environment"
      id="releaseTargetEnv"
      required={true}
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

    <div
      class="w-full items-center border-2 border-gray-200 rounded dark:border-gray-700 mt-2 mb-2"
      id="hasExplicitReleaseValues"
    >
      <div
        class="flex justify-between items-center"
        on:click={() => (hasExplicitReleaseValues = !hasExplicitReleaseValues)}
        on:keypress={() =>
          (hasExplicitReleaseValues = !hasExplicitReleaseValues)}
      >
        <label for="hasExplicitReleaseValues" class="py-2 m-2 font-bold"
          >Explicit Release Values</label
        >
        <input
          bind:checked={hasExplicitReleaseValues}
          id="bordered-checkbox-1"
          type="checkbox"
          name="hasExplicitReleaseValues"
          class="w-4 h-4 m-2 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
        />
      </div>

      {#if hasExplicitReleaseValues}
        <div class="flex justify-center pb-2 pt-2">
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
              bind:bindValue={explicitReleaseValuesReleases}
            />
          </div>
        </div>
      {/if}
    </div>

    {#if showSubmitButton}
      <div class="flex justify-center">
        <button
          type="submit"
          class="bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        >
          {submitButtonLabel}
        </button>
      </div>
    {/if}
  </div>
</form>
