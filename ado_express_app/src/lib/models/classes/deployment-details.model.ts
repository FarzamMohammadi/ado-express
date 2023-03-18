import type { IDeserializable } from "../interfaces/ideserializable.interface";
import type { IDeploymentDetails } from "../interfaces/ideployment-details.interface";

export class DeploymentDetails implements IDeserializable<IDeploymentDetails>, IDeploymentDetails {
	public release_project_name!: string;

	public release_name!: string;

	public release_number: number;

    public release_rollback: number;

    public is_crucial: boolean;

	deserialize(input: IDeploymentDetails): this {
		Object.assign(this, input);
		return this;
	}
}