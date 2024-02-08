import logging
import pickle
import threading
from socket import socket, AF_INET, SOCK_STREAM
from typing import Callable, Optional

from src.entities import ClientIdentifier, Message

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, host: str, port: int, identifier: str):
        self.connection: socket = socket(AF_INET, SOCK_STREAM)

        self.host: str = host
        self.port: int = port

        self.identifier: str = identifier

        self.on_message: Optional[Callable[[Message], None]] = None

    def __handle_io(self):
        while self.connection:
            data = self.connection.recv(1024)
            message: Message = pickle.loads(data)

            if self.on_message:
                self.on_message(message)

    # Method to set the handler for the messages received from the server
    def set_on_message_handler(self, handler: Callable[[Message], None]):
        self.on_message = handler

    # Method to send messages to the server
    def send_message(self, message: Message):
        if self.connection:
            message_dump = pickle.dumps(message)
            self.connection.send(message_dump)

    # Method used to establish a connection to the server
    def connect(self):
        try:
            self.connection.connect((self.host, self.port))
            logging.info('Connection established!')

            # Handle identification
            identifier = ClientIdentifier(self.identifier)
            identifier_dump = pickle.dumps(identifier)

            self.connection.sendall(identifier_dump)

            io_thread = threading.Thread(target=self.__handle_io)
            io_thread.start()
        except ConnectionRefusedError:
            logging.error('Connection refused!')
        except ConnectionError:
            logging.error('Connection error!')

    # Disconnects from the server
    def disconnect(self):
        self.connection.close()
