import argparse
import logging
import pathlib
import subprocess
import sys
from contextlib import contextmanager

import uvicorn
from uvicorn.supervisors import ChangeReload

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CONFIG = dict(
    app="stacktest.main:app",
    log_level="warning",
    port=5000,
)

CONFIG_DEV = dict(
    log_level="debug",
    env_file=".devenv",
    reload=True,
    reload_dirs=[str(pathlib.Path(__file__).parent)],
)


@contextmanager
def npm_run_dev():
    watcher = subprocess.Popen(
        ["npm", "run", "dev"], stdout=sys.stdout, stderr=subprocess.STDOUT
    )
    # todo: error handling when npm doesn't exist or fails
    yield
    watcher.kill()


def run_dev():
    config = uvicorn.Config(**(CONFIG | CONFIG_DEV))  # type: ignore
    logger.warning("Watching Enabled!!")
    server = uvicorn.Server(config)

    # https://github.com/encode/uvicorn/issues/1868
    # code from gh encode/uvicorn uvicorn/main.py
    sock = config.bind_socket()
    with npm_run_dev():
        ChangeReload(config, target=server.run, sockets=[sock]).run()


def run():
    config = uvicorn.Config(**CONFIG)  # type: ignore
    server = uvicorn.Server(config)
    server.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", action="store_true", help="Run in dev mode")
    args = parser.parse_args()

    if args.dev:
        run_dev()
    else:
        run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("KeyboardInterrupt while running main()")
