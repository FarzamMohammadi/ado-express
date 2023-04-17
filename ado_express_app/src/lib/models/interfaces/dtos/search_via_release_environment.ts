import type { IReleaseDetails } from '../irelease-details.interface';

export interface ISearchViaReleaseEnvironment {
    releaseDefinition: string;
    releaseDetails: IReleaseDetails[];
}