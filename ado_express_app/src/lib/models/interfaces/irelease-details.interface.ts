export interface IReleaseDetails {
	release_project_name: string;
	release_definition: string;
	release_name: string;
    release_env: string;
    is_deployed: boolean;
    modified_on: string;
}