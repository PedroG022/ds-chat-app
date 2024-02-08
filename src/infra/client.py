import logging
import threading
from socket import socket, AF_INET, SOCK_STREAM
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, host: str, port: int):
        self.connection: socket = socket(AF_INET, SOCK_STREAM)

        self.host: str = host
        self.port: int = port

        self.on_message: Optional[Callable[[str], None]] = None

    def __handle_io(self):
        while self.connection:
            data = self.connection.recv(1024)

            if self.on_message:
                self.on_message(data.decode('utf-8'))

    def set_on_message_handler(self, handler: Callable[[str], None]):
        self.on_message = handler

    def send_message(self, message: str):
        if self.connection:
            self.connection.send(message.encode('utf-8'))

    def connect(self):
        try:
            self.connection.connect((self.host, self.port))
            logging.info('Connection established!')

            io_thread = threading.Thread(target=self.__handle_io)
            io_thread.start()
        except ConnectionRefusedError:
            logging.error('Connection refused!')
        except ConnectionError:
            logging.error('Connection error!')

    def disconnect(self):
        self.connection.close()
