import { camelCaseToSnakeCase } from '../../utils/camel-to-snakecase';
import type { IDeploymentDetail } from '../interfaces/ideployment-detail.interface';
import type { IDeserializable } from '../interfaces/ideserializable.interface';
import type { IRunConfiguration } from '../interfaces/irun-configuration.interface';
import type { IToSnakeCase } from '../interfaces/ito-snake-case.interface';

export class RunConfiguration
  implements
    IDeserializable<IRunConfiguration>,
    IToSnakeCase,
    IRunConfiguration
{
  public organizationUrl!: string;

  public personalAccessToken!: string;

  public queries: string[];

  public releaseNameFormat!: string;

  public releaseTargetEnv: string;

  public searchOnly: boolean;

  public viaEnv: boolean;

  public viaEnvLatestRelease: boolean;

  public viaEnvSourceName: string;

  public deploymentDetails: IDeploymentDetail[];

  constructor(
    organizationUrl: string,
    personalAccessToken: string,
    queries: string[],
    releaseNameFormat: string,
    releaseTargetEnv: string,
    searchOnly: boolean,
    viaEnv: boolean,
    viaEnvLatestRelease: boolean,
    viaEnvSourceName: string,
    deploymentDetails: IDeploymentDetail[]
  ) {
    this.personalAccessToken = personalAccessToken;
    this.organizationUrl = organizationUrl;
    this.queries = queries;
    this.releaseNameFormat = releaseNameFormat;
    this.releaseTargetEnv = releaseTargetEnv;
    this.searchOnly = searchOnly;
    this.viaEnv = viaEnv;
    this.viaEnvLatestRelease = viaEnvLatestRelease;
    this.viaEnvSourceName = viaEnvSourceName;
    this.deploymentDetails = deploymentDetails;
  }

  deserialize(input: IRunConfiguration): this {
    Object.assign(this, input);
    return this;
  }

  private static toSnakeCaseDeep(obj: any): any {
    if (Array.isArray(obj)) {
      return obj.map(RunConfiguration.toSnakeCaseDeep);
    } else if (obj && typeof obj === 'object') {
      return Object.fromEntries(
        Object.entries(obj).map(([key, value]) => [camelCaseToSnakeCase(key), RunConfiguration.toSnakeCaseDeep(value)])
      );
    } else {
      return obj;
    }
  }
  
  toSnakeCase(): Object {
    return RunConfiguration.toSnakeCaseDeep(this);
  }
}
