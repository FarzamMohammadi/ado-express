import { DEPLOY, SEARCH_VIA_ENVIRONMENT, SEARCH_VIA_LATEST, SEARCH_VIA_NUMBER, SEARCH_VIA_QUERY } from "../../../api";
import type { IReleaseDetails } from "../../../models/interfaces/irelease-details.interface";
import type { IRunConfigurations } from "../../../models/interfaces/irun-configurations.interface";
import { JSONHttp } from "../https";


export class ADOExpressApi {

	public async searchViaEnvironment(runConfigurations: IRunConfigurations) {
		return await JSONHttp.post<[IReleaseDetails]>(SEARCH_VIA_ENVIRONMENT, runConfigurations)
		.then(res => {
			console.log(res)
		});
	}

	public async searchViaLatest(runConfigurations: IRunConfigurations) {
		return await JSONHttp.post<[IReleaseDetails]>(SEARCH_VIA_LATEST, runConfigurations)
		.then(res => {
			console.log(res)
		});
	}

	public async searchViaNumber(runConfigurations: IRunConfigurations) {
		return await JSONHttp.post<[IReleaseDetails]>(SEARCH_VIA_NUMBER, runConfigurations)
		.then(res => {
			console.log(res)
		});
	}

	public async searchViaQuery(runConfigurations: IRunConfigurations) {
		return await JSONHttp.post<[IReleaseDetails]>(SEARCH_VIA_QUERY, runConfigurations)
		.then(res => {
			console.log(res)
		});
	}

	public async deploy(runConfigurations: IRunConfigurations) {
		return await JSONHttp.post<[IReleaseDetails]>(DEPLOY, runConfigurations)
		.then(res => {
			console.log(res)
		});
	}
}