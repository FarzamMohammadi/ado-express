import asyncio

import websockets
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

connected_clients = set()

async def handler(websocket, path):
    print(f'Client connected: {websocket}')
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            await broadcast(message)
    finally:
        connected_clients.remove(websocket)
        print(f'Client disconnected: {websocket}')

async def broadcast(message):
    if connected_clients:
        print(f'Sending to {len(connected_clients)} clients: {message}')
        await asyncio.wait([client.send(message) for client in connected_clients])

def send_message(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'broadcast',
        {
            'type': 'send_message',
            'message': message
        }
    )

async def main():
    print('Starting Websocket server...')
    async with websockets.serve(handler, "localhost", 5678):
        await asyncio.Future()  # Run the server until it is manually stopped.

if __name__ == '__main__':
    asyncio.run(main())

