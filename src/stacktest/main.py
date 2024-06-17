import asyncio
import pathlib
import logging
import random
import string
import time

then = time.time()

from fastapi import FastAPI
from fastapi import WebSocket

from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException

logger = logging.getLogger(__name__)
static = pathlib.Path(__file__).parent / "static"

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except HTTPException as ex:
            if ex.status_code==404:
                logger.critical(f"404: {path=}")
                return await super().get_response("404.html", scope)
            else:
                raise ex

app = FastAPI()

@app.get("/data")
async def data():
    return dict(data=f"Server Uptime: {time.time() - then:.02f} seconds")


@app.websocket('/ws')
async def ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(5);
        await websocket.send_text(''.join(random.choice(string.ascii_uppercase) for _ in range(10)))

# this appears to need be last
app.mount('/', SPAStaticFiles(directory=static, html=True), name='server root')
