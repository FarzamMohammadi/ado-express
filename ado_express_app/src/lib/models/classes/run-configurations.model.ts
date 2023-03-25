import { camelCaseToSnakeCase } from '../../utils/camel-to-snakecase';
import type { IDeploymentDetails } from '../interfaces/ideployment-details.interface';
import type { IDeserializable } from '../interfaces/ideserializable.interface';
import type { IExplicitExclusion } from '../interfaces/iexplicit-exclusion.interface';
import type { IExplicitInclusion } from '../interfaces/iexplicit-inclusion.interface';
import type { IRunConfigurations } from '../interfaces/irun-configurations.interface';
import type { IToSnakeCase } from '../interfaces/ito-snake-case.interface';

export class RunConfigurations
  implements
    IDeserializable<IRunConfigurations>,
    IToSnakeCase,
    IRunConfigurations
{
  public explicitReleaseValues: IExplicitExclusion | IExplicitInclusion;

  public crucialReleaseDefinitions: string[];

  public organizationUrl!: string;

  public personalAccessToken!: string;

  public queries: string[];

  public releaseNameFormat!: string;

  public releaseTargetEnv: string;

  public searchOnly: boolean;

  public viaEnv: boolean;

  public viaEnvLatestRelease: boolean;

  public viaEnvSourceName: string;

  public deploymentDetails: IDeploymentDetails[];

  constructor(
    explicitReleaseValues: IExplicitExclusion | IExplicitInclusion,
    crucialReleaseDefinitions: string[],
    organizationUrl: string,
    personalAccessToken: string,
    queries: string[],
    releaseNameFormat: string,
    releaseTargetEnv: string,
    searchOnly: boolean,
    viaEnv: boolean,
    viaEnvLatestRelease: boolean,
    viaEnvSourceName: string,
    deploymentDetails: IDeploymentDetails[]
  ) {
    this.explicitReleaseValues = explicitReleaseValues;
    this.crucialReleaseDefinitions = crucialReleaseDefinitions;
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

  deserialize(input: IRunConfigurations): this {
    Object.assign(this, input);
    return this;
  }

  toSnakeCase(): Object {
    return Object.fromEntries(
      Object.entries(this).map(([key, value]) => [camelCaseToSnakeCase(key), value])
    );
  }
}
