import { writable } from 'svelte/store';
import type { GenericWebsocketMessage } from '../../models/interfaces/generic-websocket-message';

const createGenericMessageStore = () => {
  const { subscribe, set, update } = writable<GenericWebsocketMessage[]>([]);

  return {
    subscribe,
    addMessage: (messageData: GenericWebsocketMessage) => update(messages => [...messages, messageData])
  };
};

export const genericMessageStore = createGenericMessageStore();
