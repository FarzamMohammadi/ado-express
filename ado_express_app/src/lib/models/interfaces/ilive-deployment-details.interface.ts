import type { ILiveDeploymentDetail } from './ilive-deployment-detail.interface';

export interface ILiveDeploymentDetails {
  [releaseDefinition: string]: ILiveDeploymentDetail;
}
