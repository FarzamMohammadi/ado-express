import { camelCase, mapKeys } from 'lodash';
import type { RunConfigurations } from '../../../models/classes/run-configurations.model';
import type { ISearchViaReleaseEnvironment } from '../../../models/interfaces/dtos/search_via_release_environment';
import type { IDeploymentDetails } from '../../../models/interfaces/ideployment-details.interface';
import type { IReleaseDetails } from '../../../models/interfaces/irelease-details.interface';
import { JSONHttp } from '../https';
import { Endpoints } from './endpoints';

export class ADOExpressApi {

  public async runADOExpress(runConfigurations: RunConfigurations): Promise<IReleaseDetails[] | IDeploymentDetails[] | ISearchViaReleaseEnvironment[]> {
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

  private async searchViaEnvironment(runConfigurations: RunConfigurations): Promise<ISearchViaReleaseEnvironment[]> {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<ISearchViaReleaseEnvironment[]>(
      Endpoints.searchViaEnvironment,
      parsedRunConfigurations
    ).then((res) => {
      const releaseDetails: ISearchViaReleaseEnvironment[] = this.toCamelCase(res);
      return releaseDetails;
    });
  }


  private async searchViaLatest(runConfigurations: RunConfigurations) {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<[IReleaseDetails]>(
      Endpoints.searchViaLatest,
      parsedRunConfigurations
    ).then((res) => {
      return res;
    });
  }

  private async searchViaNumber(runConfigurations: RunConfigurations) {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<[IReleaseDetails]>(
      Endpoints.searchViaNumber,
      parsedRunConfigurations
    ).then((res) => {
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
