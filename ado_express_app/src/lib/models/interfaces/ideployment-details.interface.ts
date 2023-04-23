import type { IDeploymentDetail } from './ideployment-detail.interface';

export interface IDeploymentDetails {
    [releaseDefinition: string]: IDeploymentDetail;
}