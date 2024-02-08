import argparse
import logging

from pages import client_page, server_page

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
parser.add_argument('-H', '--headless', action='store_true', help='Sets the chat server to run in headless mode')
parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT, help='Overrides the default port')

args = parser.parse_args()

if __name__ == '__main__':
    if not args.server:
        client_page.start(args.port, args.headless)
    else:
        server_page.start(args.port, args.headless)
