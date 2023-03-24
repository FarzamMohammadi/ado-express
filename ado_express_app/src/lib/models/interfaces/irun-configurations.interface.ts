import type { IDeploymentDetails } from "./ideployment-details.interface";
import type { IExplicitExclusion } from "./iexplicit-exclusion.interface";
import type { IExplicitInclusion } from "./iexplicit-inclusion.interface";

export interface IRunConfigurations {
    explicitReleaseValues?: IExplicitExclusion | IExplicitInclusion;
    crucialReleaseDefinitions?: string[];
    organizationUrl: string;
    personalAccessToken: string;
    queries?: string[];
    releaseNameFormat: string;
    releaseTargetEnv?: string;
    searchOnly?: boolean;
    viaEnv?: boolean;
    viaEnvLatestRelease?: boolean;
    viaEnvSourceName?: string;
    deploymentDetails?: IDeploymentDetails[];
}