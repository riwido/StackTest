import asyncio
import argparse
import pathlib
import uvicorn
import sys
import logging
import subprocess

from uvicorn.supervisors import ChangeReload

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

asyncio



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", action="store_true", help="Run in dev mode")
    args = parser.parse_args()
    logger.info(f"Args: {args}")
    if args.dev:
        watcher = subprocess.Popen(['npm', 'run', 'dev'], stdout=sys.stdout, stderr=subprocess.STDOUT)
        config = uvicorn.Config(
            "stacktest.main:app",
            port=5000,
            log_level="debug",
            reload=True,
            reload_dirs=[str(pathlib.Path(__file__).parent)],
        )
        logger.warning("Watching Enabled!!")
        server = uvicorn.Server(config)
        sock = config.bind_socket()
        ChangeReload(config, target=server.run, sockets=[sock]).run()
        watcher.kill()
    else:
        config = uvicorn.Config(
            "stacktest.main:app",
            port=5000,
            log_level="info",
        )
        server = uvicorn.Server(config)
        server.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Closing app")
