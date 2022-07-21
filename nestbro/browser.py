from websockets import connect
from httpx import AsyncClient

import subprocess


class Browser:
    def __init__(self, headless: bool = True):
        self.headless = headless
