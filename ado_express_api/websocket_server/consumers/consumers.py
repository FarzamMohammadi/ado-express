import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer

connected_clients = set()


class WebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        connected_clients.add(self)
        await self.accept()

    async def disconnect(self, close_code):
        connected_clients.discard(self)

    async def receive(self, text_data):
        print('Received Data!', text_data)

    async def broadcast(self, message):
        if connected_clients:
            await asyncio.gather(*(client.send(message) for client in connected_clients))

    # Can be called from anywhere
    @staticmethod
    def send_message(message):
        if connected_clients:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            async def broadcast_static():
                nonlocal message
                if connected_clients:
                    await asyncio.gather(*(client.send(message) for client in connected_clients))

            coroutine = broadcast_static()
            loop.run_until_complete(coroutine)