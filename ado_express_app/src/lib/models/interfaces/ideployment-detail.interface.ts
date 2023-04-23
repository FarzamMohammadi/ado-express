export interface IDeploymentDetail {
  releaseProjectName: string;
  releaseName: string;
  releaseNumber?: number;
  releaseRollback?: number;
  isCrucial?: boolean;
}
