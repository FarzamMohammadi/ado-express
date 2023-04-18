import { camelCase, mapKeys } from 'lodash';
import type { RunConfigurations } from '../../../models/classes/run-configurations.model';
import type { IDeploymentDetails } from '../../../models/interfaces/ideployment-details.interface';
import type { IReleaseDetails } from '../../../models/interfaces/irelease-details.interface';
import { JSONHttp } from '../https';
import { Endpoints } from './endpoints';

export class ADOExpressApi {

  public async runADOExpress(runConfigurations: RunConfigurations): Promise<IReleaseDetails[] | IReleaseDetails | IDeploymentDetails[] | IDeploymentDetails> {
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
      console.log(res.internationalapp);
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
      console.log(res.internationalapp);
      console.log(res);
      return res;
    });
  }

  private async searchViaNumber(runConfigurations: RunConfigurations) {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<IReleaseDetails>(
      Endpoints.searchViaNumber,
      parsedRunConfigurations
    ).then((res) => {
      console.log(res.internationalapp);
      console.log(res);
      return res;
    });
  }

  private async searchViaQuery(runConfigurations: RunConfigurations) {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<[IReleaseDetails]>(
      Endpoints.searchViaQuery,
      parsedRunConfigurations
    ).then((res) => {
      return res;
    });
  }

  private async deploy(runConfigurations: RunConfigurations) {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<[IDeploymentDetails]>(
      Endpoints.deploy,
      parsedRunConfigurations
    ).then((res) => {
      return res;
    });
  }

  private toCamelCase(obj: any): any {
    if (Array.isArray(obj)) {
      return obj.map((item) => this.toCamelCase(item));
    } else if (obj !== null && typeof obj === 'object') {
      return mapKeys(
        Object.fromEntries(
          Object.entries(obj).map(([key, value]) => [camelCase(key), this.toCamelCase(value)])
        ),
        (_, key) => camelCase(key)
      );
    } else {
      return obj;
    }
  }
}
