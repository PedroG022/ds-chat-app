import logging
import threading
from socket import socket, AF_INET, SOCK_STREAM

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, host: str, port: int):
        self.socket: socket = socket(AF_INET, SOCK_STREAM)

        self.host: str = host
        self.port: int = port

    def __handle_io(self):
        pass

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            logging.info('Connection established!')

            io_thread = threading.Thread(target=self.__handle_io)
            io_thread.start()
        except ConnectionRefusedError:
            logging.error('Connection refused!')
        except ConnectionError:
            logging.error('Connection error!')

    def disconnect(self):
        pass

    def on_message(self, message):
        pass
