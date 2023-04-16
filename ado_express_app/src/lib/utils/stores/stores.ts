import { writable } from 'svelte/store';

export const running = writable(false);

export const runResultData = writable([])