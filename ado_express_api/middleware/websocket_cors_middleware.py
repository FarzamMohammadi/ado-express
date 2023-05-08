from django.conf import settings


class WebSocketCorsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket" and settings.DEBUG:
            scope["allowed_hosts"] = ["*"]
            scope["client"] = ["*"]
            scope["headers"] = [(b"origin", b"*")]

        return await self.app(scope, receive, send)
