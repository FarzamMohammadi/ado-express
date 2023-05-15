import { writable } from "svelte/store";
import type { IDeploymentStatuses } from '../../models/interfaces/ilive-deployment-details.interface';

const createDeploymentStatusStore = () => {
  const { subscribe, set, update } = writable<IDeploymentStatuses>({});

  return {
    subscribe,
    updateStatus: (status: IDeploymentStatuses) => update(oldStatus => ({ ...oldStatus, ...status }))
  };
};

export const deploymentStatusStore = createDeploymentStatusStore();
