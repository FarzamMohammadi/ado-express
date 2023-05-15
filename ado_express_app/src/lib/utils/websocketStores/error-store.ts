import { writable } from "svelte/store";

const createErrorStore = () => {
  const { subscribe, set, update } = writable<string[]>([]);

  return {
    subscribe,
    addError: (error: string) => update(errors => [...errors, error])
  };
};

export const errorStore = createErrorStore();
