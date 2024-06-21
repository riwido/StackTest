import asyncio
import logging
import os
import pathlib
import random
import string
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

then = time.time()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DEV_MODE = bool(os.getenv("STACKTEST_DEBUG"))

logger.info(f"{DEV_MODE=}")

if DEV_MODE:
    static = pathlib.Path(__file__).parent / "static-dev"
else:
    static = pathlib.Path(__file__).parent / "static"


async def sleep_n_log():
    try:
        while True:
            logger.info("Sleeping process doing something")
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        logger.warning("Parallel sleeping task has been cancelled")


@asynccontextmanager
async def my_app(app: FastAPI):
    logger.info(f"beginning of lifetime for {app=}")
    task = asyncio.create_task(sleep_n_log())
    yield
    task.cancel()
    logger.info("end of lifetime")


app = FastAPI(lifespan=my_app)


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
    except WebSocketDisconnect:  # pragma: no cover
        logger.info("Websocket has been disconnected")


# todo: find out what name means
app.mount("/", StaticFiles(directory=static, html=True), name="server root")
