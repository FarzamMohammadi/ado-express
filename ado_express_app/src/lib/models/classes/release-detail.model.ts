import { camelCaseToSnakeCase } from '../../utils/camel-to-snakecase';
import type { IDeserializable } from '../interfaces/ideserializable.interface';
import type { IReleaseDetail } from '../interfaces/irelease-detail.interface';
import type { IToSnakeCase } from '../interfaces/ito-snake-case.interface';

export class ReleaseDetail
  implements IDeserializable<IReleaseDetail>, IToSnakeCase, IReleaseDetail
{
  public releaseProjectName!: string;

  public releaseDefinition!: string;

  public releaseName!: string;

  public releaseEnv!: string;

  public isDeployed!: boolean;

  public modifiedOn!: string;

  constructor(
    releaseProjectName: string,
    releaseDefinition: string,
    releaseName: string,
    releaseEnv: string,
    isDeployed: boolean,
    modifiedOn: string
  ) {
    this.releaseProjectName = releaseProjectName;
    this.releaseDefinition = releaseDefinition;
    this.releaseName = releaseName;
    this.releaseEnv = releaseEnv;
    this.isDeployed = isDeployed;
    this.modifiedOn = modifiedOn;
  }

  deserialize(input: IReleaseDetail): this {
    Object.assign(this, input);
    return this;
  }

  toSnakeCase(): Object {
    return Object.fromEntries(
      Object.entries(this).map(([key, value]) => [camelCaseToSnakeCase(key), value])
    );
  }
}
