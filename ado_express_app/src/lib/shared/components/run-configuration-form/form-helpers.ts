import type { DeploymentDetail } from '../../../models/classes/deployment-detail.model';
import { RunConfiguration } from '../../../models/classes/run-configuration.model';
import { DeploymentRunMethod, RunType, SearchRunMethod, ToastType } from '../../../models/enums/enums';
import Toast from '../utils/Toast.svelte';
import { defaultFormInputs } from './default-form-inputs';

export function clonedDefaultFormInputsWithUserValues(formInputs) {
    let newFormInputs = JSON.parse(JSON.stringify(defaultFormInputs));

    for (const key in newFormInputs) {
        if (newFormInputs.hasOwnProperty(key)) {
            const element = newFormInputs[key];

            // Maintain user input values
            if (formInputs.hasOwnProperty(key)) {
                element.bindValue = formInputs[key].bindValue;
            }
        }
    }

    return newFormInputs;
}

function extractIdsFromQueries(queries: string): string[] {
    const guidRegExp = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i;

    const parts = queries.split(",");

    const ids = parts.map(part => {
        const match = part.trim().match(guidRegExp);

        return match ? match[0] : null;
    }).filter(id => id !== null);

    return ids;
}

export function generateRunConfiguration(formInputs, viaEnv, viaEnvLatestRelease, runType): RunConfiguration {
    return new RunConfiguration(
        formInputs.org_url.bindValue.trim(),
        formInputs.pat.bindValue.trim(),
        extractIdsFromQueries(formInputs.queries.bindValue),
        formInputs.rnf.bindValue.trim(),
        formInputs.rte.bindValue.trim().toLowerCase(),
        isSearchOnly(runType),
        viaEnv,
        viaEnvLatestRelease,
        formInputs.rse.bindValue.trim().toLowerCase(),
        formInputs.dd.bindValue,
    );
}

export function getFormValuesForDeployment(deploymentDetailsStore, runResultData): [RunType, DeploymentRunMethod] {
    const runType = RunType.Deploy;
    const runMethod = DeploymentRunMethod.ViaNumber;
    deploymentDetailsStore.set([]);

    runResultData.subscribe(($runResultData) => {
        for (let key in $runResultData) {
            deploymentDetailsStore.update((deploymentDetails) => [
                ...deploymentDetails,
                $runResultData[key] as DeploymentDetail,
            ]);
        }
    });

    return [runType, runMethod];
};

export function isFormValid(formInputs, deploymentDetails) {
    formInputs.dd.bindValue = deploymentDetails;

    const requiredInputs = [
        formInputs.dd,
        formInputs.org_url,
        formInputs.pat,
        formInputs.queries,
        formInputs.rnf,
        formInputs.rte,
        formInputs.rse,
    ];

    for (const input of requiredInputs) {
        if (input.required && input.show && (!input.bindValue || (Array.isArray(input.bindValue) && input.bindValue.length <= 0))) {
            return false;
        }
    }

    return true;
}

export function isNullOrUndefined(variable: any): Boolean {
    if (variable === null || variable === undefined) {
        return true;
    }
    return false;
}

export function isRunResultDataValid(runResultData): boolean {
    return runResultData !== null && runResultData !== undefined && Object.keys(runResultData).length > 0;
};

export function isSearchOnly(runType): boolean {
    if (runType === RunType.Search) {
        return true;
    } else if (runType === RunType.Deploy) {
        return false;
    }
}

export function onRunMethodSelection(runType, runMethod, running, formInputs, showSubmitButton, viaEnv, viaEnvLatestRelease): [typeof defaultFormInputs, boolean, boolean, boolean] {
    formInputs = clonedDefaultFormInputsWithUserValues(formInputs);

    if (runType === RunType.Search) {
        // Don't allow more than one search run
        if (running) {
            showSubmitButton = false;
        }

        if (runMethod == SearchRunMethod.ViaEnvironment) {
            formInputs.queries.required = false;
            formInputs.queries.show = false;

            formInputs.rse.required = false;
            formInputs.rse.show = false;
        } else if (runMethod == SearchRunMethod.ViaLatestInEnvironment) {
            viaEnv = true;
            viaEnvLatestRelease = true;

            formInputs.queries.required = false;
            formInputs.queries.show = false;
        } else if (runMethod == SearchRunMethod.ViaNumber) {
            viaEnv = false;
            viaEnvLatestRelease = false;

            formInputs.queries.required = false;
            formInputs.queries.show = false;

            formInputs.rse.required = false;
            formInputs.rse.show = false;

            formInputs.rte.required = false;
            formInputs.rte.show = false;
        } else if (runMethod == SearchRunMethod.ViaQuery) {
            viaEnv = true;
            viaEnvLatestRelease = false;

            formInputs.dd.required = false;
            formInputs.dd.show = false;
        }
    } else if (runType === RunType.Deploy && runMethod === DeploymentRunMethod.ViaNumber) {
        // Allow deployment after search
        if (running) {
            showSubmitButton = true;
        }
        formInputs.queries.required = false;
        formInputs.queries.show = false;

        formInputs.rse.required = false;
        formInputs.rse.show = false;
    }

    return [formInputs, showSubmitButton, viaEnv, viaEnvLatestRelease];
}

export function onRunTypeSelection(runType): string {
    if (runType === RunType.Search) {
        return 'Initiate Search';
    } else if (runType === RunType.Deploy) {
        return 'Execute Deployment';
    }
}

export function runMethodSelectionIsIncomplete(runType, runMethod) {
    return !runMethod || !runType;
}

export function setupRunTypeVariables(runType, runMethod, viaEnv, viaEnvLatestRelease, formInputs): [boolean, boolean, typeof defaultFormInputs] {
    if (runType === RunType.Search) {
        if (runMethod === SearchRunMethod.ViaEnvironment) {
            viaEnv = true;
            viaEnvLatestRelease = false;
            formInputs.queries.bindValue = null;
        } else if (runMethod === SearchRunMethod.ViaLatestInEnvironment) {
            viaEnv = true;
            viaEnvLatestRelease = true;
            formInputs.queries.bindValue = null;
        } else if (runMethod === SearchRunMethod.ViaNumber) {
            viaEnv = false;
            viaEnvLatestRelease = false;
            formInputs.queries.bindValue = null;
        } else if (runMethod === SearchRunMethod.ViaQuery) {
            viaEnv = true;
            viaEnvLatestRelease = false;
        }
    } else if (runType === RunType.Deploy && runMethod === DeploymentRunMethod.ViaNumber) {
        viaEnv = false;
        viaEnvLatestRelease = false;
        formInputs.queries.bindValue = null;
    }

    return [viaEnv, viaEnvLatestRelease, formInputs];
}

export function showToast(type: ToastType, message: string, duration?: number): void {
    new Toast({
        target: document.body,
        props: {
            type,
            message,
            duration,
        },
    });
}