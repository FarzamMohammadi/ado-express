import type { RunConfigurations } from '../../../models/classes/run-configurations.model';
import type { IDeploymentDetails } from '../../../models/interfaces/ideployment-details.interface';
import type { IReleaseDetails } from '../../../models/interfaces/irelease-details.interface';
import { JSONHttp } from '../https';
import { Endpoints } from './endpoints';

export class ADOExpressApi {

  public async runADOExpress(runConfigurations: RunConfigurations): Promise<IReleaseDetails | IDeploymentDetails> {
    if (runConfigurations.searchOnly) {
      if (runConfigurations.queries) {
        return await this.searchViaQuery(runConfigurations);
      }
      else if (!runConfigurations.viaEnv && !runConfigurations.viaEnvLatestRelease) {
        return await this.searchViaNumber(runConfigurations);
      }
      else if (runConfigurations.viaEnv && !runConfigurations.viaEnvLatestRelease) {
        return await this.searchViaEnvironment(runConfigurations);
      }
      else if (runConfigurations.viaEnv && runConfigurations.viaEnvLatestRelease) {
        return await this.searchViaLatest(runConfigurations);
      }
    }
    else {
      return await this.deploy(runConfigurations);
    }
  }

  private async searchViaEnvironment(runConfigurations: RunConfigurations): Promise<IReleaseDetails> {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<IReleaseDetails>(
      Endpoints.searchViaEnvironment,
      parsedRunConfigurations
    ).then((res) => {
      console.log(res);
      return res;
    });
  }


  private async searchViaLatest(runConfigurations: RunConfigurations): Promise<IDeploymentDetails> {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<IDeploymentDetails>(
      Endpoints.searchViaLatest,
      parsedRunConfigurations
    ).then((res) => {
      console.log(res);
      return res;
    });
  }

  private async searchViaNumber(runConfigurations: RunConfigurations): Promise<IReleaseDetails> {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<IReleaseDetails>(
      Endpoints.searchViaNumber,
      parsedRunConfigurations
    ).then((res) => {
      console.log(res);
      return res;
    });
  }

  private async searchViaQuery(runConfigurations: RunConfigurations): Promise<IDeploymentDetails> {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<IDeploymentDetails>(
      Endpoints.searchViaQuery,
      parsedRunConfigurations
    ).then((res) => {
      console.log(res);
      return res;
    });
  }

  private async deploy(runConfigurations: RunConfigurations): Promise<IDeploymentDetails> {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<IDeploymentDetails>(
      Endpoints.deploy,
      parsedRunConfigurations
    ).then((res) => {
      console.log(res);
      return res;
    });
  }
}
