import pathlib
import uvicorn
from uvicorn.supervisors import ChangeReload
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def main():
    config = uvicorn.Config(
        "stacktest.main:app",
        port=5000,
        log_level="debug",
        reload=True,
        reload_dirs=[str(pathlib.Path(__file__).parent)],
    )
    server = uvicorn.Server(config)
    sock = config.bind_socket()
    ChangeReload(config, target=server.run, sockets=[sock]).run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Closing app")
