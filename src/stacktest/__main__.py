import pathlib
import asyncio
from time import sleep
import uvicorn
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
async def sleep_n_log():
    try:
        while True:
            logger.info("Sleeping process doing something")
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        logger.info("Done sleeping")


async def main():
    config = uvicorn.Config("stacktest.main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    try:
        await asyncio.gather(server.serve(), sleep_n_log())
    except asyncio.CancelledError:
        logger.info("Done serving")

if __name__ == "__main__":
    asyncio.run(main())
