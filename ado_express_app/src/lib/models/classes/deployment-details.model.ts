import { camelCaseToSnakeCase } from '../../utils/camel-to-snakecase';
import type { IDeploymentDetails } from '../interfaces/ideployment-details.interface';
import type { IDeserializable } from '../interfaces/ideserializable.interface';
import type { IToSnakeCase } from '../interfaces/ito-snake-case.interface';

export class DeploymentDetails
  implements
    IDeserializable<IDeploymentDetails>,
    IToSnakeCase,
    IDeploymentDetails
{
  public releaseProjectName!: string;

  public releaseName!: string;

  public releaseNumber: number;

  public releaseRollback: number;

  public isCrucial: boolean;

  constructor(
    releaseProjectName: string,
    releaseName: string,
    releaseNumber: number,
    releaseRollback: number,
    isCrucial: boolean
  ) {
    this.releaseProjectName = releaseProjectName;
    this.releaseName = releaseName;
    this.releaseNumber = releaseNumber;
    this.releaseRollback = releaseRollback;
    this.isCrucial = isCrucial;
  }

  deserialize(input: IDeploymentDetails): this {
    Object.assign(this, input);
    return this;
  }

  toSnakeCase(): Object {
    return Object.fromEntries(
      Object.entries(this).map(([key, value]) => [camelCaseToSnakeCase(key), value])
    );
  }
}
