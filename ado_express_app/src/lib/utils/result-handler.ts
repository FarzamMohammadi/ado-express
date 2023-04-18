import type { ISearchViaReleaseEnvironment } from '../models/interfaces/dtos';
import { runResultData } from './stores';

function isISearchViaReleaseEnvironmentArray(obj: any): obj is ISearchViaReleaseEnvironment[] {
    if (!Array.isArray(obj)) {
        return false;
    }

    return obj.every(item => {
        return (
            typeof item === 'object' &&
            'releaseDefinition' in item &&
            typeof item.releaseDefinition === 'string' &&
            'releaseDetails' in item &&
            Array.isArray(item.releaseDetails)
        );
    });
}

export class ResultHandler {

    static sendMessage(text: string, showIdleDots: boolean = false) {
        runResultData.update((data) => [
            ...data,
            {
                text,
                showIdleDots,
            },
        ]);
    }

    static sendRunResults(runResults: any) {
        // Search via environment
        if (isISearchViaReleaseEnvironmentArray(runResults)) {
            for (let i = 0; i < runResults.length; i++) {
                this.sendMessage(`\nRelease definition: ${runResults[i].releaseDefinition}`);
                for (let releaseDetails of runResults[i].releaseDetails) {
                    this.sendMessage(`\nRelease: ${releaseDetails.releaseName} - ${releaseDetails.releaseEnv} - ${releaseDetails.isDeployed ? 'Deployed' : 'Not deployed'} - ${releaseDetails.modifiedOn}`);
                }
                this.sendMessage(`\n\n`);
            }
        }
    }
}