from django.urls import path
from websocket_server.consumers import consumers

websocket_urlpatterns = [
    path('ws/', consumers.WebSocketConsumer.as_asgi()),
]