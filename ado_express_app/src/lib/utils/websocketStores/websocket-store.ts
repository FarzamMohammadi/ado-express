import { WebsocketMessageType } from '../../models/enums/enums';
import type { GenericWebsocketMessage } from '../../models/interfaces/generic-websocket-message';
import type { IDeploymentStatuses } from '../../models/interfaces/ilive-deployment-details.interface';
import { deploymentStatusStore } from './deployment-status-store';
import { errorStore } from './error-store';
import { genericMessageStore } from './generic-message-store';

const createWebsocketStore = () => {
  const connect = () => {
    const websocketUrl = 'ws://localhost:8000/ws/';
    const ws = new WebSocket(websocketUrl);

    ws.addEventListener('open', (event) => {
      console.log('WebSocket connection opened:', event);
    });

    ws.addEventListener('message', (event) => {
      const parsedData = JSON.parse(event.data);
      console.log('WebSocket message received:', parsedData);

      if (parsedData.message_type === WebsocketMessageType.Generic) {
        const genericMessage: GenericWebsocketMessage = JSON.parse(parsedData.message);
        genericMessageStore.addMessage(genericMessage);
      } else if (parsedData.message_type === WebsocketMessageType.Error) {
        errorStore.addError(parsedData.message);
      } else if (parsedData.message_type === WebsocketMessageType.DeploymentStatus) {
        const status: IDeploymentStatuses = JSON.parse(parsedData.message);
        deploymentStatusStore.updateStatus(status);
      }
      //   } else if (parsedData.message_type === WebsocketMessageType.SearchStatus) {
      //     const status: ISearchStatuses = JSON.parse(parsedData.message);
      //     searchStatusStore.updateStatus(status);
      //   }
    });

    ws.addEventListener('close', (event) => {
      console.log('WebSocket connection closed:', event);
      // Try to reconnect in 5 seconds
      setTimeout(() => connect(), 5000);
    });

    ws.addEventListener('error', (event) => {
      console.log('WebSocket error:', event);
      // The connection will be closed after an error, so we don't need to do anything here
    });
  };

  return {
    connect
  };
};

export const websocketStore = createWebsocketStore();
