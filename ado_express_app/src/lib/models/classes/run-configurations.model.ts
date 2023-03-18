import type { IDeploymentDetails } from "../interfaces/ideployment-details.interface";
import type { IDeserializable } from "../interfaces/ideserializable.interface";
import type { IRunConfigurations } from "../interfaces/irun-configurations.interface";

export class RunConfigurations implements IDeserializable<IRunConfigurations>, IRunConfigurations {
	public explicit_release_values: string;

	public crucial_release_definitions: [string];

	public organization_url!: string;

    public personal_access_token!: string;

    public queries: [string];

    public release_name_format!: string;

	public release_target_env: string;

	public search_only: boolean;

	public via_env: boolean;

    public via_env_latest_release: boolean;

    public via_env_source_name: string;

    public deployment_details: [IDeploymentDetails];

	deserialize(input: IRunConfigurations): this {
		Object.assign(this, input);
		return this;
	}
}