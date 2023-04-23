<script lang="ts">
  import { ADOExpressApi } from '../../core/services/api';
  import { RunConfiguration } from '../../models/classes/run-configuration.model';
  import {
      DeploymentRunMethod,
      RunType,
      SearchRunMethod,
      ToastType,
  } from '../../models/enums/enums';
  import type { IExplicitExclusion } from '../../models/interfaces/iexplicit-exclusion.interface';
  import type { IExplicitInclusion } from '../../models/interfaces/iexplicit-inclusion.interface';
  import type { IInputSettings } from '../../models/interfaces/input-settings.interface';
  import { ResultHandler } from '../../utils/result-handler';
  import { deploymentDetails, runResultData } from '../../utils/stores';
  import ExplicitReleaseValuesInput from './custom-form-components/ExplicitReleaseValuesInput.svelte';
  import DeploymentDetailsSelector from './custom-form-components/deployment-details/DeploymentDetailsSelector.svelte';
  import CustomPasswordInput from './custom-form-components/inputs/CustomPasswordInput.svelte';
  import CustomTextInput from './custom-form-components/inputs/CustomTextInput.svelte';
  import CustomUrlInput from './custom-form-components/inputs/CustomUrlInput.svelte';
  import Toast from './utils/Toast.svelte';

  const defaultFormInputRequirements = {
    dd: {
      required: true,
      show: true,
    } as IInputSettings,
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

  let deploymentSelectorHeaders = [
    '',
    'Project Name',
    'Release Name',
    'Release #',
    'Rollback #',
    'Crucial',
  ];
  let formInputRequirements = structuredClone(defaultFormInputRequirements);
  export let runMethod: string = null;
  export let runType: string = null;
  export let running;
  let submitButtonLabel = 'Run ADO Express';
  let isSubmitting = false;
  // RunConfiguration
  let crucialReleaseDefinitions: '';
  let explicitReleaseValuesReleases = '';
  let explicitReleaseValuesType = '';
  let hasExplicitReleaseValues = false;
  let organizationUrl = '';
  let personalAccessToken = '';
  let queries: string = null;
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

  async function handleSubmit() {
    running = true;
    isSubmitting = true;

    ResultHandler.sendMessage(`\nRunning ${runType.toLowerCase()}`, true);

    if (isNullOrUndefined(runType) || isNullOrUndefined(runMethod)) {
      return showToast(
        ToastType.Warning,
        'Please complete the run type selection at the top'
      );
    }

    //TODO: within this or run method validator set a variable to be levered for finding out whether we need deployment details or not
    setupRunConfigurationRunTypeVariables();

    const runConfigurations = new RunConfiguration(
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
      $deploymentDetails
    );

    const adoExpressApi = new ADOExpressApi();
    console.log(runConfigurations);

    showToast(ToastType.Success, 'Successfully submitted run request');

    $runResultData = await adoExpressApi.runADOExpress(runConfigurations);

    ResultHandler.sendRunResults(runConfigurations);

    isSubmitting = false;
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
    } else if (runType && runType === 'Deployment') {
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
        queries = null;

        formInputRequirements.queries.required = false;
        formInputRequirements.queries.show = false;
      } else if (runMethod == SearchRunMethod.ViaNumber) {
        viaEnv = false;
        viaEnvLatestRelease = false;
        queries = null;

        formInputRequirements.queries.required = false;
        formInputRequirements.queries.show = false;

        formInputRequirements.rse.required = false;
        formInputRequirements.rse.show = false;

        formInputRequirements.rte.required = false;
        formInputRequirements.rte.show = false;
      } else if (runMethod == SearchRunMethod.ViaQuery) {
        viaEnv = true;
        viaEnvLatestRelease = false;

        formInputRequirements.dd.required = false;
        formInputRequirements.dd.show = false;
      }
    } else if (runType === RunType.Deployment) {
      if (runMethod == SearchRunMethod.ViaLatestInEnvironment) {
        viaEnv = true;
        viaEnvLatestRelease = true;
        queries = null;

        formInputRequirements.queries.required = false;
        formInputRequirements.queries.show = false;
      } else if (runMethod == SearchRunMethod.ViaNumber) {
        viaEnv = false;
        viaEnvLatestRelease = false;
        queries = null;
        formInputRequirements.queries.required = false;
        formInputRequirements.queries.show = false;

        formInputRequirements.rse.required = false;
        formInputRequirements.rse.show = false;
      }
    }
  }

  function onRunTypeSelection(runType): void {
    if (runType === RunType.Search) {
      submitButtonLabel = 'Run New Search';
    } else if (runType === RunType.Deployment) {
      submitButtonLabel = 'Run New Deployment';
    }
  }

  function setupRunConfigurationRunTypeVariables(): void {
    if (runType === RunType.Search) {
      if (runMethod == SearchRunMethod.ViaEnvironment) {
        viaEnv = true;
        viaEnvLatestRelease = false;
        queries = null;
      } else if (runMethod == SearchRunMethod.ViaLatestInEnvironment) {
        viaEnv = true;
        viaEnvLatestRelease = true;
        queries = null;
      } else if (runMethod == SearchRunMethod.ViaNumber) {
        viaEnv = false;
        viaEnvLatestRelease = false;
        queries = null;
      } else if (runMethod == SearchRunMethod.ViaQuery) {
        viaEnv = true;
        viaEnvLatestRelease = false;
      }
    } else if (
      runType === RunType.Deployment &&
      runMethod == DeploymentRunMethod.ViaNumber
    ) {
      viaEnv = false;
      viaEnvLatestRelease = false;
      queries = null;
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
</script>

<svelte:head>
  <link
    rel="stylesheet"
    href="https://unpkg.com/mono-icons@1.0.5/iconfont/icons.css"
  />
</svelte:head>

<div class="flex flex-col max-w-3xl items-center justify-center">
  <DeploymentDetailsSelector
    {deploymentSelectorHeaders}
    bind:showInput={formInputRequirements.dd.show}
  />

  <form class="w-96" on:submit|preventDefault={handleSubmit}>
    <div class="relative flex flex-col text-gray-900 dark:text-white">
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

    <div class="flex justify-center pt-4">
      <button
        disabled={isSubmitting}
        type="submit"
        class="bg-transparent hover:bg-blue-700 text-blue-900 dark:text-blue-500 font-semibold hover:text-white dark:hover:text-white border border-blue-800 hover:border-transparent rounded-lg shadow-lg"
      >
        {submitButtonLabel}
      </button>
    </div>
  </form>
</div>
