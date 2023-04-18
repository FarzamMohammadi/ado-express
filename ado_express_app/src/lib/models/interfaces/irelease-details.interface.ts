import type { IReleaseDetail } from './irelease-detail.interface';

export interface IReleaseDetails {
    [releaseDefinition: string]: IReleaseDetail[];
}