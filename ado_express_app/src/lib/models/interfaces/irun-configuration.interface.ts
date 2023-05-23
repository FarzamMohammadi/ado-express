import type { IDeploymentDetail } from './ideployment-detail.interface';

export interface IRunConfiguration {
  organizationUrl: string;
  personalAccessToken: string;
  queries?: string[];
  releaseNameFormat: string;
  releaseTargetEnv?: string;
  searchOnly?: boolean;
  viaEnv?: boolean;
  viaEnvLatestRelease?: boolean;
  viaEnvSourceName?: string;
  deploymentDetails?: IDeploymentDetail[];
}
