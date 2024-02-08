import argparse
import logging

from src import ClientApp, ServerApp

# Logging config
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | [%(name)s] %(message)s",
)

# Ignore INFO and DEBUG logs from the flet packages
logging.getLogger('flet_core').setLevel(logging.ERROR)
logging.getLogger('flet_runtime').setLevel(logging.ERROR)

# Default connection and hosting port
DEFAULT_PORT = 36000

# Args parsing
parser = argparse.ArgumentParser()

parser.add_argument('-s', '--server', action='store_true', help='Sets the chat to run in the server mode')
parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT, help='Overrides the default port')

args = parser.parse_args()

if __name__ == '__main__':
    if not args.server:
        ClientApp(args.port).start()
    else:
        ServerApp(args.port).start()
