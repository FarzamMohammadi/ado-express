import json

from channels.generic.websocket import AsyncWebsocketConsumer

connected_clients = set()

class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        connected_clients.add(self)
        await self.accept()

    async def disconnect(self, close_code):
        connected_clients.remove(self)

    async def receive(self, text_data):
        await self.broadcast(text_data)

    async def broadcast(self, message):
        if connected_clients:
            await self.channel_layer.group_send(
                'broadcast',
                {
                    'type': 'send_message',
                    'message': message
                }
            )

    async def send_message(self, event):
        message = event['message']

        for client in connected_clients:
            await client.send(text_data=json.dumps({'message': message}))
