import pathlib
import logging
from fastapi import FastAPI
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
    return dict(data="ABC123")

# this appears to need be last
app.mount('/', SPAStaticFiles(directory=static, html=True), name='server root')
