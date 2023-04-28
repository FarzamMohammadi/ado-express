import { writable } from 'svelte/store';
import type { DeploymentDetail } from '../../models/classes/deployment-detail.model';
import type { IRunResultData } from '../../models/interfaces/irun-result-data';

export const deploymentDetails = writable<DeploymentDetail[]>([]);

export const runResultData = writable<IRunResultData[]>([]);

export const running = writable(false);

