<script lang="ts">
  import { ADOExpressApi } from '../../core/services/api';
  import { RunConfigurations } from '../../models/classes/run-configurations.model';
  import {
      RunType,
      SearchRunMethod,
      ToastType
  } from '../../models/enums/enums';
  import type { IDeploymentDetails } from '../../models/interfaces/ideployment-details.interface';
  import type { IExplicitExclusion } from '../../models/interfaces/iexplicit-exclusion.interface';
  import type { IExplicitInclusion } from '../../models/interfaces/iexplicit-inclusion.interface';
  import type { IInputSettings } from '../../models/interfaces/input-settings.interface';
  import CustomPasswordInput from './custom-form-components/CustomPasswordInput.svelte';
  import CustomRunSpecifierDropdown from './custom-form-components/CustomRunSpecifierDropdown.svelte';
  import CustomTextInput from './custom-form-components/CustomTextInput.svelte';
  import CustomUrlInput from './custom-form-components/CustomUrlInput.svelte';
  import ExcelFileInput from './custom-form-components/ExcelFileInput.svelte';
  import ExcelPatternSelector from './custom-form-components/ExcelPatternSelector.svelte';
  import ExplicitReleaseValuesInput from './custom-form-components/ExplicitReleaseValuesInput.svelte';
  import Toast from './utils/Toast.svelte';

  const defaultFormInputRequirements = {
    crd: {
      required: true,
      show: true,
    } as IInputSettings,
    org_url: {
      required: true,
      show: true,
    } as IInputSettings,
    pat: {
      required: true,
      show: true,
    } as IInputSettings,
    queries: {
      required: true,
      show: true,
    } as IInputSettings,
    rnf: {
      required: true,
      show: true,
    } as IInputSettings,
    rte: {
      required: true,
      show: true,
    } as IInputSettings,
    rse: {
      required: true,
      show: true,
    } as IInputSettings,
    erv: {
      required: true,
      show: true,
    } as IInputSettings,
  };

  let deploymentDetailsType = '';
  let deploymentSelectorHeaders = [
    'Project Name',
    'Release Name',
    'Release Number',
    'Rollback Number',
    'Is Crucial',
  ];
  let formInputRequirements = structuredClone(defaultFormInputRequirements);
  let runMethod = null;
  let runType = null;
  let showSubmitButton = true;
  let submitButtonLabel = 'Run ADO Express';

  // RunConfigurations
  let crucialReleaseDefinitions: '';
  let deployment_details: IDeploymentDetails[] = [];
  let explicitReleaseValuesReleases = '';
  let explicitReleaseValuesType = '';
  let hasExplicitReleaseValues = false;
  let organizationUrl = '';
  let personalAccessToken = '';
  let queries: '';
  let releaseNameFormat = 'Release-$(rev:r)';
  let releaseTargetEnv = '';
  let viaEnv = false;
  let viaEnvLatestRelease = false;
  let viaEnvSourceName = '';

  function getExplicitReleaseValues(): IExplicitInclusion | IExplicitExclusion {
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

  function handleSubmit(): void {
    if (isNullOrUndefined(runType) || isNullOrUndefined(runMethod)) {
      return showToast(
        ToastType.Warning,
        'Please complete the run type selection at the top'
      );
    }

    setupRunConfigurationRunTypeVariables();

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
    showToast(ToastType.Success, 'Successfully submitted run request');
  }

  function isNullOrUndefined(variable: any): Boolean {
    if (variable === null || variable === undefined) {
      return true;
    }
    return false;
  }

  function isSearchOnly(): boolean {
    if (runType && runType === 'Search') {
      return true;
    } else if (runType && runType === 'Deploy') {
      return false;
    }
  }

  function onRunMethodSelection(runMethod) {
    formInputRequirements = structuredClone(defaultFormInputRequirements);

    if (runType === RunType.Search) {
      formInputRequirements.crd.required = false;
      formInputRequirements.crd.show = false;

      // Currently works on deployment only
      formInputRequirements.erv.required = false;
      formInputRequirements.erv.show = false;
      if (runMethod == SearchRunMethod.ViaEnvironment) {
        formInputRequirements.queries.required = false;
        formInputRequirements.queries.show = false;

        formInputRequirements.rse.required = false;
        formInputRequirements.rse.show = false;
      } else if (runMethod == SearchRunMethod.ViaLatestInEnvironment) {
        viaEnv = true;
        viaEnvLatestRelease = true;
        queries = '';

        formInputRequirements.queries.required = false;
        formInputRequirements.queries.show = false;
      } else if (runMethod == SearchRunMethod.ViaNumber) {
        viaEnv = false;
        viaEnvLatestRelease = false;
        queries = '';

        formInputRequirements.queries.required = false;
        formInputRequirements.queries.show = false;

        formInputRequirements.rse.required = false;
        formInputRequirements.rse.show = false;
      } else if (runMethod == SearchRunMethod.ViaQuery) {
        viaEnv = true;
        viaEnvLatestRelease = false;
      }
    } else if (runType === RunType.Deploy) {
      if (runMethod == SearchRunMethod.ViaLatestInEnvironment) {
        viaEnv = true;
        viaEnvLatestRelease = true;
        queries = '';

        formInputRequirements.queries.required = false;
        formInputRequirements.queries.show = false;
      } else if (runMethod == SearchRunMethod.ViaNumber) {
        viaEnv = false;
        viaEnvLatestRelease = false;
        queries = '';
        formInputRequirements.queries.required = false;
        formInputRequirements.queries.show = false;

        formInputRequirements.rse.required = false;
        formInputRequirements.rse.show = false;
      }
    }
  }

  function onRunTypeSelection(runType): void {
    if (runType === RunType.Search) {
      submitButtonLabel = 'Run the Search';
    } else if (runType === RunType.Deploy) {
      submitButtonLabel = 'Run the Deployment';
    }
  }

  function setupRunConfigurationRunTypeVariables(): void {
    if (runType === RunType.Search) {
      if (runMethod == SearchRunMethod.ViaEnvironment) {
        viaEnv = true;
        viaEnvLatestRelease = false;
        queries = '';
      } else if (runMethod == SearchRunMethod.ViaLatestInEnvironment) {
        viaEnv = true;
        viaEnvLatestRelease = true;
        queries = '';
      } else if (runMethod == SearchRunMethod.ViaNumber) {
        viaEnv = false;
        viaEnvLatestRelease = false;
        queries = '';
      } else if (runMethod == SearchRunMethod.ViaQuery) {
        viaEnv = true;
        viaEnvLatestRelease = false;
      }
    } else if (runType === RunType.Deploy) {
      if (runMethod == SearchRunMethod.ViaLatestInEnvironment) {
        viaEnv = true;
        viaEnvLatestRelease = true;
        queries = '';
      } else if (runMethod == SearchRunMethod.ViaNumber) {
        viaEnv = false;
        viaEnvLatestRelease = false;
        queries = '';
      }
    }
  }

  function showToast(
    type: ToastType,
    message: string,
    duration?: number
  ): void {
    new Toast({
      target: document.body,
      props: {
        type,
        message,
        duration,
      },
    });
  }

  $: onRunTypeSelection(runType);
  $: onRunMethodSelection(runMethod);

  function handleDataExport(event) {
    console.log('Exported data:', event.detail);
  }
</script>

<svelte:head>
  <link
    rel="stylesheet"
    href="https://unpkg.com/mono-icons@1.0.5/iconfont/icons.css"
  />
</svelte:head>

<div class="relative mb-16 z-10">
  <CustomRunSpecifierDropdown
    bind:selectedCategoryName={runType}
    bind:selectedTask={runMethod}
  />
</div>

<div class="w-auto items-center border-2 border-gray-200 rounded dark:border-gray-700 mt-2 mb-2 p-2 mx-4" id="deploymentDetails">
  <label for="deploymentDetails" class="font-bold">Deployment Details</label>

  <div class="flex justify-center pb-2 pt-2">
    <label class="pr-3">
      <input
        type="radio"
        name="deploymentDetailsType"
        value="file"
        bind:group={deploymentDetailsType}
      />
      Excel File
    </label>

    <label>
      <input
        type="radio"
        name="deploymentDetailsType"
        value="custom"
        bind:group={deploymentDetailsType}
      />
      Manual Input
    </label>
  </div>

  {#if deploymentDetailsType === 'custom'}
    <div class="flex items-center justify-center p-2">
      <ExcelPatternSelector
        columns={5}
        rows={4}
        headers={deploymentSelectorHeaders}
        on:dataExport={handleDataExport}
      />
    </div>
  {:else if deploymentDetailsType === 'file'}
    <div class="flex items-center justify-center p-2">
      <ExcelFileInput />
    </div>
  {/if}
</div>

<form on:submit|preventDefault={handleSubmit}>

  <div class="relative flex flex-col text-gray-900">
    <CustomTextInput
      label="Crucial Release Definitions"
      id="crucialReleaseDefinitions"
      bind:required={formInputRequirements.crd.required}
      bind:showInput={formInputRequirements.crd.show}
      bind:bindValue={crucialReleaseDefinitions}
    />
    <CustomUrlInput
      label="Organization Url"
      id="organizationUrl"
      bind:required={formInputRequirements.org_url.required}
      bind:showInput={formInputRequirements.org_url.show}
      bind:bindValue={organizationUrl}
    />
    <CustomPasswordInput
      label="Personal Access Token"
      id="personalAccessToken"
      bind:required={formInputRequirements.pat.required}
      bind:showInput={formInputRequirements.pat.show}
      bind:bindValue={personalAccessToken}
    />
    <CustomTextInput
      label="Queries"
      id="queries"
      bind:required={formInputRequirements.queries.required}
      bind:showInput={formInputRequirements.queries.show}
      bind:bindValue={queries}
    />
    <CustomTextInput
      label="Release Name Format"
      id="releaseNameFormat"
      bind:required={formInputRequirements.rnf.required}
      bind:showInput={formInputRequirements.rnf.show}
      bind:bindValue={releaseNameFormat}
    />
    <CustomTextInput
      label="Release Target Environment"
      id="releaseTargetEnv"
      bind:required={formInputRequirements.rte.required}
      bind:showInput={formInputRequirements.rte.show}
      bind:bindValue={releaseTargetEnv}
    />
    <CustomTextInput
      label="Release Source Environment"
      id="viaEnvSourceName"
      bind:required={formInputRequirements.rse.required}
      bind:showInput={formInputRequirements.rse.show}
      bind:bindValue={viaEnvSourceName}
    />

    <ExplicitReleaseValuesInput
      bind:hasExplicitReleaseValues
      bind:explicitReleaseValuesType
      bind:explicitReleaseValuesReleases
      bind:showInput={formInputRequirements.erv.show}
    />
  </div>

  {#if showSubmitButton}
    <div class="flex justify-center pt-4">
      <button
        type="submit"
        class="bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        {submitButtonLabel}
      </button>
    </div>
  {/if}
</form>
