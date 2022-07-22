from websockets import connect
from httpx import AsyncClient
from orjson import dumps

from .pages import Page

import subprocess


class Browser:
    DIVICE_URI: str | None = None
    def __init__(self, headless: bool = True, *, executor_path: str = "chromium-browser",
                 gpu: bool = False, sandbox: bool = False):
        self.headless = headless
        self.process: subprocess.Popen | None = None
        self.executor_path = executor_path
        self.gpu = gpu
        self.sandbox = sandbox
        self.client = AsyncClient()

    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self, *args):
        await self.close()

    async def start(self, port: int = 9222):
        args = [self.executor_path]
        if self.headless:
            args.append("--headless")
        if not self.gpu:
            args.append("--disable-gpu")
        if not self.sandbox:
            args.append("--no-sandbox")
        args.append(f"--remote-debugging-port={port}")
        self.process = subprocess.Popen(args)
        self.URI = "http://127.0.0.1:{}".format(port)

    async def close(self) -> None:
        await self.ws.close()
        self.process.close()
    
    async def new_page(self) -> Page:
        page = Page(await self.request("GET", "/json/new"))
        await page.connect()
        return page

    async def request(self, method: str, path: str, **kwargs) -> dict:
        r = await self.client.request(method, self.URI + path, **kwargs)
        return r.json()
