import type { RunConfigurations } from '../../../models/classes/run-configurations.model';
import type { IReleaseDetails } from '../../../models/interfaces/irelease-details.interface';
import { JSONHttp } from '../https';
import { Endpoints } from './endpoints';

export class ADOExpressApi {
  public async searchViaEnvironment(runConfigurations: RunConfigurations) {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<[IReleaseDetails]>(
      Endpoints.searchViaEnvironment,
      parsedRunConfigurations
    ).then((res) => {
      console.log(res);
    });
  }

  public async searchViaLatest(runConfigurations: RunConfigurations) {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<[IReleaseDetails]>(
      Endpoints.searchViaLatest,
      parsedRunConfigurations
    ).then((res) => {
      console.log(res);
    });
  }

  public async searchViaNumber(runConfigurations: RunConfigurations) {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<[IReleaseDetails]>(
      Endpoints.searchViaNumber,
      parsedRunConfigurations
    ).then((res) => {
      console.log(res);
    });
  }

  public async searchViaQuery(runConfigurations: RunConfigurations) {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<[IReleaseDetails]>(
      Endpoints.searchViaQuery,
      parsedRunConfigurations
    ).then((res) => {
      console.log(res);
    });
  }

  public async deploy(runConfigurations: RunConfigurations) {
    const parsedRunConfigurations = runConfigurations.toSnakeCase();

    return await JSONHttp.post<[IReleaseDetails]>(
      Endpoints.deploy,
      parsedRunConfigurations
    ).then((res) => {
      console.log(res);
    });
  }
}
