import { camelCaseToSnakeCase } from "../../utils/camel-to-snakecase";
import type { IDeserializable } from "../interfaces/ideserializable.interface";
import type { IReleaseDetails } from "../interfaces/irelease-details.interface";
import type { IToSnakeCase } from "../interfaces/ito-snake-case.interface";

export class ReleaseDetails implements IDeserializable<IReleaseDetails>, IToSnakeCase, IReleaseDetails {
	public releaseProjectName!: string;

	public releaseDefinition!: string;

	public releaseName!: string;

	public releaseEnv!: string;

	public isDeployed!: boolean;

	public modifiedOn!: string;

	constructor (
		releaseProjectName: string,
		releaseDefinition: string,
		releaseName: string,
		releaseEnv: string,
		isDeployed: boolean,
		modifiedOn: string,
	) {
		this.releaseProjectName = releaseProjectName;
		this.releaseDefinition = releaseDefinition;
		this.releaseName = releaseName;
		this.releaseEnv = releaseEnv;
		this.isDeployed = isDeployed;
		this.modifiedOn = modifiedOn;
	}

	deserialize(input: IReleaseDetails): this {
		Object.assign(this, input);
		return this;
	}

	toSnakeCase(str: string): string {
		return camelCaseToSnakeCase(str);
	}
}