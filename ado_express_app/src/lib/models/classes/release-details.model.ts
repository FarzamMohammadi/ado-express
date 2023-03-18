import type { IDeserializable } from "../interfaces/ideserializable.interface";
import type { IReleaseDetails } from "../interfaces/irelease-details.interface";

export class ReleaseDetails implements IDeserializable<IReleaseDetails>, IReleaseDetails {
	public release_project_name!: string;

	public release_definition!: string;

	public release_name!: string;

    public release_env!: string;

    public is_deployed!: boolean;

    public modified_on!: string;

	deserialize(input: IReleaseDetails): this {
		Object.assign(this, input);
		return this;
	}
}