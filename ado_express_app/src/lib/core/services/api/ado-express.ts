import type { RunConfiguration } from '../../../models/classes/run-configuration.model';
import type { IDeploymentDetails } from '../../../models/interfaces/ideployment-details.interface';
import type { IReleaseDetails } from '../../../models/interfaces/irelease-details.interface';
import { JSONHttp } from '../https';
import { Endpoints } from './endpoints';

export class ADOExpressApi {

  public async runADOExpress(runConfigurations: RunConfiguration): Promise<IReleaseDetails | IDeploymentDetails> {
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

  private async searchViaEnvironment(runConfigurations: RunConfiguration): Promise<IReleaseDetails> {
    return await JSONHttp.post<IReleaseDetails>(
      Endpoints.searchViaEnvironment,
      runConfigurations
    ).then((res) => {
      console.log(res);
      return res;
    });
  }


  private async searchViaLatest(runConfigurations: RunConfiguration): Promise<IDeploymentDetails> {
    return await JSONHttp.post<IDeploymentDetails>(
      Endpoints.searchViaLatest,
      runConfigurations
    ).then((res) => {
      console.log(res);
      return res;
    });
  }

  private async searchViaNumber(runConfigurations: RunConfiguration): Promise<IReleaseDetails> {
    return await JSONHttp.post<IReleaseDetails>(
      Endpoints.searchViaNumber,
      runConfigurations
    ).then((res) => {
      console.log(res);
      return res;
    });
  }

  private async searchViaQuery(runConfigurations: RunConfiguration): Promise<IDeploymentDetails> {
    return await JSONHttp.post<IDeploymentDetails>(
      Endpoints.searchViaQuery,
      runConfigurations
    ).then((res) => {
      console.log(res);
      return res;
    });
  }

  private async deploy(runConfigurations: RunConfiguration): Promise<void> {
    await JSONHttp.post<IDeploymentDetails>(
      Endpoints.deploy,
      runConfigurations
    ).then((res) => {
      console.log(res);
    });
  }  
}
