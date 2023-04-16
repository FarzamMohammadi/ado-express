import { writable } from 'svelte/store';
import type { IRunResultData } from '../../models/interfaces/irun-result-data';

export const running = writable(false);

export const runResultData = writable<IRunResultData[]>([]);