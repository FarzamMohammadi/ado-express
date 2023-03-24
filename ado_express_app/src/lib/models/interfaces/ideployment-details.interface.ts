export interface IDeploymentDetails {
	releaseProjectName: string;
	releaseName: string;
	releaseNumber?: number;
    releaseRollback?: number;
    isCrucial?: boolean;
}