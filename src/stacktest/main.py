import asyncio
import pathlib
import logging
import random
import string
import time
from contextlib import asynccontextmanager
then = time.time()

from fastapi import FastAPI
from fastapi import WebSocket

from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.websockets import WebSocketDisconnect

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

static = pathlib.Path(__file__).parent / "static"

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except HTTPException as exc:
            if ex.status_code == 404:
                logger.critical(f"404: {path=}")
                return await super().get_response("404.html", scope)
            else:
                raise exc

async def sleep_n_log():
    try:
        while True:
            logger.info("Sleeping process doing something")
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        logger.warning("Parallel sleeping task has been cancelled")


@asynccontextmanager
async def lifetime(app: FastAPI):
    logger.info(f"beginning of lifetime for {app=}")
    task = asyncio.create_task(sleep_n_log())
    yield
    task.cancel()
    logger.info("end of lifetime")

app = FastAPI(lifespan=lifetime)

@app.get("/data")
async def data():
    return dict(data=f"Server Uptime: {time.time() - then:.02f} seconds")

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_text(
                "".join(random.choice(string.ascii_uppercase) for _ in range(10))
            )
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        logger.info("Websocket has been disconnected")


# this appears to need be last
app.mount("/", SPAStaticFiles(directory=static, html=True), name="server root")
