<script lang="ts">
  import { ADOExpressApi } from '../../core/services/api';
  import type { DeploymentDetail } from '../../models/classes/deployment-detail.model';
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

  // RunConfiguration
  let explicitReleaseValuesReleases = '';
  let explicitReleaseValuesType = '';
  let hasExplicitReleaseValues = false;
  let viaEnv = false;
  let viaEnvLatestRelease = false;

  let runResultDataIsValid = false;

  const defaultFormInputRequirements = {
    dd: {
      bindValue: null,
      required: true,
      show: true,
    } as IInputSettings,
    crd: {
      bindValue: '',
      required: false,
      show: true,
    } as IInputSettings,
    org_url: {
      bindValue: '',
      required: true,
      show: true,
    } as IInputSettings,
    pat: {
      bindValue: '',
      required: true,
      show: true,
    } as IInputSettings,
    queries: {
      bindValue: '',
      required: true,
      show: true,
    } as IInputSettings,
    rnf: {
      bindValue: 'Release-$(rev:r)',
      required: true,
      show: true,
    } as IInputSettings,
    rte: {
      bindValue: '',
      required: true,
      show: true,
    } as IInputSettings,
    rse: {
      bindValue: '',
      required: true,
      show: true,
    } as IInputSettings,
    erv: {
      bindValue: '',
      required: false,
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
  export let isSubmitting = false;
  let showSubmitButton = true;
  let disableSubmitButton = false;

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

  function isFormValid() {
    formInputRequirements.dd.bindValue = $deploymentDetails;

    const requiredInputs = [
      formInputRequirements.dd,
      formInputRequirements.org_url,
      formInputRequirements.pat,
      formInputRequirements.queries,
      formInputRequirements.rnf,
      formInputRequirements.rte,
      formInputRequirements.rse,
    ];

    for (const input of requiredInputs) {
      if (Array.isArray(input.bindValue)) {
        console.log(input.bindValue);
      }
      if (
        input.required &&
        input.show &&
        (!input.bindValue ||
          (Array.isArray(input.bindValue) && input.bindValue.length <= 0))
      ) {
        return false;
      }
    }

    return true;
  }

  function runMethodSelectionIsIncomplete() {
    return !runMethod || !runType;
  }

  async function handleSubmit() {
    isSubmitting = true;

    if (runMethodSelectionIsIncomplete()) {
      showToast(
        ToastType.Warning,
        'Please complete the run method selection at the top'
      );
      return;
    }

    if (!isFormValid()) {
      showToast(
        ToastType.Warning,
        'Please complete all required fields before submitting'
      );
      return;
    }

    disableSubmitButton = true;
    showSubmitButton = false;
    running = true;
    ResultHandler.sendMessage(
      running ? `\n\nRunning ${runType}` : `\nRunning ${runType}`,
      true
    );

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
      formInputRequirements.crd.bindValue
        .trim()
        .split(',')
        .map((s) => s.trim()) ?? null,
      formInputRequirements.org_url.bindValue.trim(),
      formInputRequirements.pat.bindValue.trim(),
      formInputRequirements.queries.bindValue
        .trim()
        .split(',')
        .map((s) => s.trim()) ?? null,
      formInputRequirements.rnf.bindValue.trim(),
      formInputRequirements.rte.bindValue.trim().toLowerCase(),
      isSearchOnly(),
      viaEnv,
      viaEnvLatestRelease,
      formInputRequirements.rse.bindValue.trim().toLowerCase(),
      formInputRequirements.dd.bindValue
    );

    const adoExpressApi = new ADOExpressApi();
    console.log(runConfigurations);

    showToast(ToastType.Success, 'Successfully submitted run request');

    $runResultData = await adoExpressApi.runADOExpress(runConfigurations);

    ResultHandler.sendRunResults(runConfigurations);

    isSubmitting = false;
    disableSubmitButton = false;
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

  function clonedDefaultFormInputsWithUserValues() {
    let newFormInputRequirements = JSON.parse(
      JSON.stringify(defaultFormInputRequirements)
    );

    for (const key in newFormInputRequirements) {
      if (newFormInputRequirements.hasOwnProperty(key)) {
        const element = newFormInputRequirements[key];

        // Maintain user input values
        if (formInputRequirements.hasOwnProperty(key)) {
          element.bindValue = formInputRequirements[key].bindValue;
        }
      }
    }

    return newFormInputRequirements;
  }

  function onRunMethodSelection(runMethod) {
    formInputRequirements = clonedDefaultFormInputsWithUserValues();

    if (runType === RunType.Search) {
      // Don't allow more than one run search
      if (running) {
        showSubmitButton = false;
      }

      formInputRequirements.crd.show = false;

      // Currently works on deployment only
      formInputRequirements.erv.show = false;
      if (runMethod == SearchRunMethod.ViaEnvironment) {
        formInputRequirements.queries.required = false;
        formInputRequirements.queries.show = false;

        formInputRequirements.rse.required = false;
        formInputRequirements.rse.show = false;
      } else if (runMethod == SearchRunMethod.ViaLatestInEnvironment) {
        viaEnv = true;
        viaEnvLatestRelease = true;

        formInputRequirements.queries.required = false;
        formInputRequirements.queries.show = false;
      } else if (runMethod == SearchRunMethod.ViaNumber) {
        viaEnv = false;
        viaEnvLatestRelease = false;

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
    } else if (
      runType === RunType.Deployment &&
      runMethod === DeploymentRunMethod.ViaNumber
    ) {
      // Allow deployment after search
      if (running) {
        showSubmitButton = true;
      }
      formInputRequirements.queries.required = false;
      formInputRequirements.queries.show = false;

      formInputRequirements.rse.required = false;
      formInputRequirements.rse.show = false;
    }
  }

  function onRunTypeSelection(runType): void {
    if (runType === RunType.Search) {
      submitButtonLabel = 'Initiate Search';
    } else if (runType === RunType.Deployment) {
      submitButtonLabel = 'Execute Deployment';
    }
  }

  function setupRunConfigurationRunTypeVariables(): void {
    if (runType === RunType.Search) {
      if (runMethod == SearchRunMethod.ViaEnvironment) {
        viaEnv = true;
        viaEnvLatestRelease = false;
        formInputRequirements.queries.bindValue = null;
      } else if (runMethod == SearchRunMethod.ViaLatestInEnvironment) {
        viaEnv = true;
        viaEnvLatestRelease = true;
        formInputRequirements.queries.bindValue = null;
      } else if (runMethod == SearchRunMethod.ViaNumber) {
        viaEnv = false;
        viaEnvLatestRelease = false;
        formInputRequirements.queries.bindValue = null;
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
      formInputRequirements.queries.bindValue = null;
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

  function deploySearchResults() {
    runType = RunType.Deployment;
    runMethod = DeploymentRunMethod.ViaNumber;

    deploymentDetails.set([]);

    for (let key in $runResultData) {
      deploymentDetails.update((deploymentDetails) => [
        ...deploymentDetails,
        $runResultData[key] as DeploymentDetail,
      ]);
    }
  }

  $: onRunTypeSelection(runType);
  $: onRunMethodSelection(runMethod);
  $: runResultDataIsValid =
    $runResultData !== null &&
    $runResultData !== undefined &&
    Object.keys($runResultData).length > 0;
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
    bind:isSubmitting
  />

  <form class="w-96">
    <div class="relative flex flex-col text-gray-900 dark:text-white">
      <CustomTextInput
        label="Crucial Release Definitions"
        id="crucialReleaseDefinitions"
        bind:required={formInputRequirements.crd.required}
        bind:showInput={formInputRequirements.crd.show}
        bind:bindValue={formInputRequirements.crd.bindValue}
        bind:isSubmitting
      />
      <CustomUrlInput
        label="Organization Url"
        id="organizationUrl"
        bind:required={formInputRequirements.org_url.required}
        bind:showInput={formInputRequirements.org_url.show}
        bind:bindValue={formInputRequirements.org_url.bindValue}
        bind:isSubmitting
      />
      <CustomPasswordInput
        label="Personal Access Token"
        id="personalAccessToken"
        bind:required={formInputRequirements.pat.required}
        bind:showInput={formInputRequirements.pat.show}
        bind:bindValue={formInputRequirements.pat.bindValue}
        bind:isSubmitting
      />
      <CustomTextInput
        label="Queries"
        id="queries"
        bind:required={formInputRequirements.queries.required}
        bind:showInput={formInputRequirements.queries.show}
        bind:bindValue={formInputRequirements.queries.bindValue}
        bind:isSubmitting
      />
      <CustomTextInput
        label="Release Name Format"
        id="releaseNameFormat"
        bind:required={formInputRequirements.rnf.required}
        bind:showInput={formInputRequirements.rnf.show}
        bind:bindValue={formInputRequirements.rnf.bindValue}
        bind:isSubmitting
      />
      <CustomTextInput
        label="Release Target Environment"
        id="releaseTargetEnv"
        bind:required={formInputRequirements.rte.required}
        bind:showInput={formInputRequirements.rte.show}
        bind:bindValue={formInputRequirements.rte.bindValue}
        bind:isSubmitting
      />
      <CustomTextInput
        label="Release Source Environment"
        id="viaEnvSourceName"
        bind:required={formInputRequirements.rse.required}
        bind:showInput={formInputRequirements.rse.show}
        bind:bindValue={formInputRequirements.rse.bindValue}
        bind:isSubmitting
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
          disabled={disableSubmitButton}
          type="button"
          on:click={handleSubmit}
          class="bg-transparent hover:bg-blue-700 text-blue-900 dark:text-blue-500 font-semibold hover:text-white dark:hover:text-white border border-blue-800 hover:border-transparent rounded-lg shadow-lg"
        >
          {submitButtonLabel}
        </button>
      </div>
    {/if}
    <div class="flex flex-row items-center justify-center">
      {#if !showSubmitButton && runResultDataIsValid && runType === RunType.Search && (runMethod === SearchRunMethod.ViaLatestInEnvironment || runMethod === SearchRunMethod.ViaQuery)}
        <button
          class="bg-transparent hover:bg-blue-700 text-blue-900 dark:text-blue-500 font-semibold hover:text-white dark:hover:text-white border border-blue-800 hover:border-transparent rounded-lg shadow-lg"
          on:click={deploySearchResults}>Deploy Search Results</button
        >
      {/if}
    </div>
  </form>
</div>
