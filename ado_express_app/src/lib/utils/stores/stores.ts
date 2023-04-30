import { writable } from 'svelte/store';
import type { DeploymentDetail } from '../../models/classes/deployment-detail.model';
import type { IDeploymentDetails } from '../../models/interfaces/ideployment-details.interface';
import type { IReleaseDetails } from '../../models/interfaces/irelease-details.interface';
import type { IDisplayedRunResultData } from '../../models/interfaces/irun-result-data';

export const deploymentDetails = writable<DeploymentDetail[]>([]);

export const displayedRunResultData = writable<IDisplayedRunResultData[]>([]);

export const runResultData = writable<IReleaseDetails | IDeploymentDetails>();

export const running = writable(true);