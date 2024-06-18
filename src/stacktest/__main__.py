import argparse
import pathlib
import uvicorn
import logging
from uvicorn.supervisors import ChangeReload

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", action="store_true", help="Run in dev mode")
    args = parser.parse_args()
    logger.info(f"Args: {args}")
    if args.dev:
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
