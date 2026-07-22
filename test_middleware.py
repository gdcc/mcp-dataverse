from starlette.types import ASGIApp, Scope, Receive, Send

class StripCharsetMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def send_wrapper(message: dict) -> None:
            if message["type"] == "http.response.start":
                headers = message.get("headers", [])
                for i, (key, value) in enumerate(headers):
                    if key.lower() == b"content-type" and b"text/event-stream" in value:
                        headers[i] = (key, b"text/event-stream")
            await send(message)

        await self.app(scope, receive, send_wrapper)
