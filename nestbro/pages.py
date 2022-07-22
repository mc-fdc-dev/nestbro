from websockets import connect
from orjson import dumps

from typing import Any


class Page:
    def __init__(self, data: dict):
        self.data = data

    async def connect(self) -> None:
        self.ws = await connect(self.data["webSocketDebuggerUrl"])

    async def request(self, method: str, params: Any, *, type: int = 1) -> None:
        await self.ws.send(dumps({"type": type, "method": method, "params": params}))
