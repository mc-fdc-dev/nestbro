from websockets import connect
from orjson import dumps

from typing import Any
from base64 import b64decode


class Page:
    def __init__(self, data: dict):
        self.data = data

    async def connect(self) -> None:
        self.ws = await connect(self.data["webSocketDebuggerUrl"])

    async def request(self, method: str, params: Any, *, type: int = 1) -> None:
        await self.ws.send(dumps({"type": type, "method": method, "params": params}))
        
    async def recv(self) -> dict:
        return dumps(await self.ws.recv())

    async def close(self, *, ignore_cache: bool = False,
                    script_to_evaluate_on_load: str | None = None) -> None:
        payload = {}
        if ignore_cache:
            payload["ignoreCache"] = True
        if script_to_evaluate_on_load is not None:
            payload["scriptToEvaluateOnLoad"] = script_to_evaluate_on_load
        await self.request(method="Page.reload", params=payload)
        
    async def screenshot(self) -> bytes:
        await self.request("Page.captureScreenshot")
        return b64decode((await self.recv()["data"]).encode())
