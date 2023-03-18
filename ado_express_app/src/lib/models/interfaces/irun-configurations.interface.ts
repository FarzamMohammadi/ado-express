import type { IDeploymentDetails } from "./ideployment-details.interface";

export interface IRunConfigurations {
	explicit_release_values?: {};
	crucial_release_definitions?: [string];
	organization_url: string;
    personal_access_token: string;
    queries?: [string];
    release_name_format: string;
	release_target_env?: string;
	search_only?: boolean;
    via_env?: boolean;
    via_env_latest_release?: boolean;
    via_env_source_name?: string;
	deployment_details?: [IDeploymentDetails];
}