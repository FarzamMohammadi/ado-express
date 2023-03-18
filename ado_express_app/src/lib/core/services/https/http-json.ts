import type { IRunConfigurations } from "../../../models/interfaces/irun-configurations.interface";

export class JSONHttp {
	public static async get<T>(url: string): Promise<T> {
		const res = await fetch(url)
		return res.json() as Promise<T>;
	}

	public static async post<T>(url: string, obj: IRunConfigurations): Promise<T> {
		const res = await fetch(url, {
			method: 'POST',
			body: JSON.stringify(obj),
			headers: {
				"Content-Type": "application/json"
			}
		})
		return res.json() as Promise<T>;
	}
}