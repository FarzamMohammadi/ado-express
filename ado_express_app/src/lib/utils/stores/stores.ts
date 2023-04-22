import { writable } from 'svelte/store';
import type { DeploymentDetail } from '../../models/classes/deployment-detail.model';
import type { IdisplayedRunResultData } from '../../models/interfaces/irun-result-data';

export const deploymentDetails = writable<DeploymentDetail[]>([]);

export const displayedRunResultData = writable<IdisplayedRunResultData[]>([]);

export const running = writable(false);

