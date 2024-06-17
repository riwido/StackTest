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
from starlette.websockets import WebSocketDisconnect
from uvicorn import Server

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
static = pathlib.Path(__file__).parent / "static"


"""
https://stackoverflow.com/questions/58133694/graceful-shutdown-of-uvicorn-starlette-app-with-websockets
"""
handle_exit = Server.handle_exit
_app_has_exited = False


def patched_handle_exit(*args, **kwargs):
    global _app_has_exited
    _app_has_exited = True
    handle_exit(*args, **kwargs)


Server.handle_exit = patched_handle_exit


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except HTTPException as ex:
            if ex.status_code == 404:
                logger.critical(f"404: {path=}")
                return await super().get_response("404.html", scope)
            else:
                raise ex


app = FastAPI()


@app.get("/data")
async def data():
    return dict(data=f"Server Uptime: {time.time() - then:.02f} seconds")


@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            if _app_has_exited:
                logger.info("Cancelling websocket loop")
                break
            await websocket.send_text(
                "".join(random.choice(string.ascii_uppercase) for _ in range(10))
            )
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        logger.info("Websocket has been disconnected")


# this appears to need be last
app.mount("/", SPAStaticFiles(directory=static, html=True), name="server root")
