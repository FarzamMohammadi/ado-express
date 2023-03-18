export interface IDeploymentDetails {
	release_project_name: string;
	release_name: string;
	release_number?: number;
    release_rollback?: number;
    is_crucial?: boolean;
}