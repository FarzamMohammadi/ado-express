import { DEPLOY, SEARCH_VIA_ENVIRONMENT, SEARCH_VIA_LATEST, SEARCH_VIA_NUMBER, SEARCH_VIA_QUERY } from "../../../api";
import type { IReleaseDetails } from "../../../models/interfaces/irelease-details.interface";
import type { IRunConfigurations } from "../../../models/interfaces/irun-configurations.interface";
import { snakeToCamel } from "../../../utils/snake-to-camel";
import { JSONHttp } from "../https";


export class ADOExpressApi {

	public async searchViaEnvironment(runConfigurations: IRunConfigurations) {
		const parsedRunConfigurations = this.convertObjectToCamelCase(runConfigurations);

		return await JSONHttp.post<[IReleaseDetails]>(SEARCH_VIA_ENVIRONMENT, parsedRunConfigurations)
		.then(res => {
			console.log(res)
		});
	}

	public async searchViaLatest(runConfigurations: IRunConfigurations) {
		const parsedRunConfigurations = this.convertObjectToCamelCase(runConfigurations);

		return await JSONHttp.post<[IReleaseDetails]>(SEARCH_VIA_LATEST, parsedRunConfigurations)
		.then(res => {
			console.log(res)
		});
	}

	public async searchViaNumber(runConfigurations: IRunConfigurations) {
		const parsedRunConfigurations = this.convertObjectToCamelCase(runConfigurations);

		return await JSONHttp.post<[IReleaseDetails]>(SEARCH_VIA_NUMBER, parsedRunConfigurations)
		.then(res => {
			console.log(res)
		});
	}

	public async searchViaQuery(runConfigurations: IRunConfigurations) {
		const parsedRunConfigurations = this.convertObjectToCamelCase(runConfigurations);

		return await JSONHttp.post<[IReleaseDetails]>(SEARCH_VIA_QUERY, parsedRunConfigurations)
		.then(res => {
			console.log(res)
		});
	}

	public async deploy(runConfigurations: IRunConfigurations) {
		const parsedRunConfigurations = this.convertObjectToCamelCase(runConfigurations);

		return await JSONHttp.post<[IReleaseDetails]>(DEPLOY, parsedRunConfigurations)
		.then(res => {
			console.log(res)
		});
	}
	
	private convertObjectToCamelCase = (obj: any) => {
		return Object.fromEntries(Object.entries(obj).map(([key, value]) => [snakeToCamel(key), value]))
	}
}