import type { IDeploymentStatus } from './ilive-deployment-detail.interface';

export interface IDeploymentStatuses {
  [releaseDefinition: string]: IDeploymentStatus;
}
