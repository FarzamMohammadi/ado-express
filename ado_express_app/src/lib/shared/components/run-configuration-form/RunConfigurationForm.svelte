<script lang="ts">
  import { ADOExpressApi } from '../../../core/services/api';
  import { ToastType } from '../../../models/enums/enums';
  import { ResultHandler } from '../../../utils/result-handler';
  import { deploymentDetails, runResultData } from '../../../utils/stores';
  import DeploymentDetailsSelector from '../custom-form-components/deployment-detail-selector/DeploymentDetailSelector.svelte';
  import CustomPasswordInput from '../custom-form-components/inputs/CustomPasswordInput.svelte';
  import CustomTextInput from '../custom-form-components/inputs/CustomTextInput.svelte';
  import CustomUrlInput from '../custom-form-components/inputs/CustomUrlInput.svelte';

  import SubmitButton from './SubmitButton.svelte';
  import { defaultFormInputs } from './default-form-inputs';
  import {
    generateRunConfiguration,
    getFormValuesForDeployment,
    isFormValid,
    isNullOrUndefined,
    isRunResultDataValid,
    onRunMethodSelection,
    onRunTypeSelection,
    runMethodSelectionIsIncomplete,
    setupRunTypeVariables,
    showToast,
  } from './form-helpers';

  // API
  const adoExpressApi = new ADOExpressApi();

  // Form Inputs
  let formInputs = structuredClone(defaultFormInputs);

  // Headers
  let deploymentSelectorHeaders = ['', 'Project Name', 'Release Name', 'Release #', 'Rollback #', 'Crucial'];

  // Run Configuration
  let viaEnv = false;
  let viaEnvLatestRelease = false;

  // Run Results
  let runResultDataIsValid = false;

  // Run Settings
  export let isSubmitting = false;
  export let runMethod: string = null;
  export let runType: string = null;
  export let running;

  // Submit Button
  let disableSubmitButton = false;
  let showSubmitButton = true;
  let submitButtonLabel = 'Run ADO Express';

  async function handleSubmit() {
    isSubmitting = true;

    if (runMethodSelectionIsIncomplete(runType, runMethod)) {
      showToast(ToastType.Warning, 'Please complete the run method selection at the top');
      return;
    }

    if (!isFormValid(formInputs, $deploymentDetails)) {
      showToast(ToastType.Warning, 'Please complete all required fields before submitting');
      return;
    }

    disableSubmitButton = true;
    showSubmitButton = false;
    running = true;

    ResultHandler.sendMessage(running ? `\n\nRunning ${runType}` : `\nRunning ${runType}`, true);

    if (isNullOrUndefined(runType) || isNullOrUndefined(runMethod)) {
      return showToast(ToastType.Warning, 'Please complete the run type selection at the top');
    }

    [viaEnv, viaEnvLatestRelease, formInputs] = setupRunTypeVariables(runType, runMethod, viaEnv, viaEnvLatestRelease, formInputs);
    const runConfigurations = generateRunConfiguration(formInputs, viaEnv, viaEnvLatestRelease, runType);

    showToast(ToastType.Success, 'Successfully submitted run request');

    $runResultData = await adoExpressApi.runADOExpress(runConfigurations);
    ResultHandler.sendRunResults(runConfigurations);

    isSubmitting = false;
    disableSubmitButton = false;
  }

  function setupSearchResultsForDeployment() {
    [runType, runMethod] = getFormValuesForDeployment(deploymentDetails, runResultData);
  }

  $: if (runType) submitButtonLabel = onRunTypeSelection(runType);
  $: if (runMethod)
    [formInputs, showSubmitButton, viaEnv, viaEnvLatestRelease] = onRunMethodSelection(
      runType,
      runMethod,
      running,
      formInputs,
      showSubmitButton,
      viaEnv,
      viaEnvLatestRelease,
    );
  $: if ($runResultData) runResultDataIsValid = isRunResultDataValid($runResultData);
</script>

<svelte:head>
  <link rel="stylesheet" href="https://unpkg.com/mono-icons@1.0.5/iconfont/icons.css" />
</svelte:head>

<div class="flex flex-col max-w-3xl items-center justify-center">
  <DeploymentDetailsSelector deploymentSelectorHeaders={deploymentSelectorHeaders} bind:showInput={formInputs.dd.show} bind:isSubmitting={isSubmitting} />

  <form class="w-96">
    <div class="relative flex flex-col text-gray-900 dark:text-white">
      <CustomUrlInput
        label="Organization Url"
        id="organizationUrl"
        bind:required={formInputs.org_url.required}
        bind:showInput={formInputs.org_url.show}
        bind:bindValue={formInputs.org_url.bindValue}
        bind:isSubmitting={isSubmitting}
      />
      <CustomPasswordInput
        label="Personal Access Token"
        id="personalAccessToken"
        bind:required={formInputs.pat.required}
        bind:showInput={formInputs.pat.show}
        bind:bindValue={formInputs.pat.bindValue}
        bind:isSubmitting={isSubmitting}
      />
      <CustomTextInput
        label="Queries"
        id="queries"
        bind:required={formInputs.queries.required}
        bind:showInput={formInputs.queries.show}
        bind:bindValue={formInputs.queries.bindValue}
        bind:isSubmitting={isSubmitting}
      />
      <CustomTextInput
        label="Release Name Format"
        id="releaseNameFormat"
        bind:required={formInputs.rnf.required}
        bind:showInput={formInputs.rnf.show}
        bind:bindValue={formInputs.rnf.bindValue}
        bind:isSubmitting={isSubmitting}
      />
      <CustomTextInput
        label="Release Source Environment"
        id="viaEnvSourceName"
        bind:required={formInputs.rse.required}
        bind:showInput={formInputs.rse.show}
        bind:bindValue={formInputs.rse.bindValue}
        bind:isSubmitting={isSubmitting}
      />
      <CustomTextInput
        label="Release Target Environment"
        id="releaseTargetEnv"
        bind:required={formInputs.rte.required}
        bind:showInput={formInputs.rte.show}
        bind:bindValue={formInputs.rte.bindValue}
        bind:isSubmitting={isSubmitting}
      />
      
      <SubmitButton
        bind:disableSubmitButton={disableSubmitButton}
        handleSubmit={handleSubmit}
        bind:runType={runType}
        bind:runMethod={runMethod}
        bind:showSubmitButton={showSubmitButton}
        bind:submitButtonLabel={submitButtonLabel}
        bind:runResultDataIsValid={runResultDataIsValid}
        setupSearchResultsForDeployment={setupSearchResultsForDeployment}
      />
    </div>
  </form>
</div>
