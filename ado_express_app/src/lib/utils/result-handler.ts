import type { RunConfiguration } from '../models/classes/run-configuration.model';
import type { IDeploymentDetails } from '../models/interfaces/ideployment-details.interface';
import type { IReleaseDetail } from '../models/interfaces/irelease-detail.interface';
import type { IReleaseDetails } from '../models/interfaces/irelease-details.interface';
import { displayedRunResultData } from './stores';

export class ResultHandler {

    static formatDateTime(dateString: string): string {
        const date = new Date(dateString);

        const formattedDate = `${date.getFullYear()}-${(date.getMonth() + 1)
            .toString()
            .padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")}`;

        let hours = date.getHours();
        const ampm = hours >= 12 ? "PM" : "AM";
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'

        const formattedTime = `${hours.toString().padStart(2, "0")}:${date.getMinutes().toString().padStart(2, "0")}:${date.getSeconds().toString().padStart(2, "0")} ${ampm}`;

        return `${formattedDate} ${formattedTime}`;
    }

    static sendMessage(text: string, showIdleDots: boolean = false) {
        displayedRunResultData.update((data) => [
            ...data,
            {
                text,
                showIdleDots,
            },
        ]);
    }

    static showReleaseDetailsToUser(runResults: IReleaseDetails) {
        if (runResults === undefined || runResults === null) {
            this.sendMessage('\nNo results found');
            return;
        }

        this.sendMessage('\n\nGathered Results:');

        for (let key in runResults) {
            const releaseDetails: IReleaseDetail[] = runResults[key];

            this.sendMessage(`\n\nRelease Definition: ${releaseDetails[0].releaseDefinition}\nProject: ${releaseDetails[0].releaseProjectName}\n`);

            for (let releaseDetail of releaseDetails) {
                this.sendMessage(`\nRelease: ${releaseDetail.releaseName}\nEnv: ${releaseDetail.releaseEnv}\nDeployed: ${releaseDetail.isDeployed}\nModified On: ${this.formatDateTime(releaseDetail.modifiedOn)}\n`);
            }
        }
    }

    static showDeploymentDetailsToUser(runResults: IDeploymentDetails) {
        if (runResults === undefined || runResults === null) {
            this.sendMessage('\nNo results found');
            return;
        }

        this.sendMessage('\n\nGathered Results:');

        for (let key in runResults) {
            const deploymentDetail = runResults[key];

            this.sendMessage(`\n\nRelease Definition: ${deploymentDetail.releaseName}\nProject: ${deploymentDetail.releaseProjectName}\nRelease: ${deploymentDetail.releaseNumber}\nRollback: ${deploymentDetail.releaseRollback}`);
        }
    }

    static sendRunResults(runConfiguration: RunConfiguration, runResults: IReleaseDetails | IDeploymentDetails) {
        if (runConfiguration.searchOnly
            && !runConfiguration.queries
            && (!runConfiguration.viaEnv && !runConfiguration.viaEnvLatestRelease
                || runConfiguration.viaEnv && !runConfiguration.viaEnvLatestRelease)) {
            this.showReleaseDetailsToUser(runResults as IReleaseDetails);
        }
        else {
            this.showDeploymentDetailsToUser(runResults as IDeploymentDetails);
        }
    }
}