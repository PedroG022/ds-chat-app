import logging
import pickle
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Event

from src.entities import ClientIdentifier, Message

logger = logging.getLogger(__name__)


class Server:

    # Server's parameters initialization
    def __init__(self, port: int):
        self.socket: socket = socket(AF_INET, SOCK_STREAM)

        self.host = '127.0.0.1'
        self.port = port

        self.__server_shutdown: Event = Event()
        self.__client_sockets: dict[ClientIdentifier: socket] = {}

        self.server_identifier: ClientIdentifier = ClientIdentifier('SERVER')
        self.server_identifier.client_id = 'SERVER'

    # Method to start the server
    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        listen_for_clients = Thread(target=self.__wait_for_clients)
        listen_for_clients.start()

        logger.info(f'Server started successfully at :{self.port}, waiting for connections...')

    # Method to stop the server
    def stop(self):
        logger.info('Stopping server...')

        self.__disconnect_all_clients()
        self.__server_shutdown.set()
        self.socket.close()

    # Method that runs once a new client is connected
    def on_new_client(self, client_socket: socket, address: tuple):
        identifier: ClientIdentifier = pickle.loads(client_socket.recv(1024))
        logger.info(f'New client {address}: "{identifier.name}"')

        join_message: Message = Message(body=f'{identifier.name} JOINED THE CHAT', identifier=self.server_identifier)
        self.__broadcast(join_message)

        self.__client_sockets[identifier] = client_socket
        self.__handle_client_messages(client_socket, identifier)

    def __disconnect_all_clients(self):
        for client_socket in self.__client_sockets.values():
            client_socket: socket
            client_socket.close()

    # Handles the messages that will be received from the clients
    def __handle_client_messages(self, client_socket: socket, client_identifier: ClientIdentifier):
        while not self.__server_shutdown.is_set():
            try:
                data = client_socket.recv(1024)
                message: Message = pickle.loads(data)

                # Sets the message identifier for the sender
                message.identifier = client_identifier
                self.on_message(message)

            # Catches clients disconnections and other errors
            except Exception as exception:
                if isinstance(exception, ConnectionResetError):
                    del self.__client_sockets[client_identifier]
                    logger.info(f'Client "{client_identifier.name}" disconnected')

                    left_message: Message = Message(body=f'{client_identifier.name} LEFT THE CHAT',
                                                    identifier=self.server_identifier)
                    self.__broadcast(left_message)
                elif not isinstance(exception, ConnectionAbortedError):
                    logger.error(f'Error while handling client message: {exception}')
                break

    # Broadcasts a message to all clients
    def __broadcast(self, message: Message):
        for identifier in self.__client_sockets.keys():
            identifier: ClientIdentifier

            # Verifies if the message sender is the target, if it is, then it's ignored
            if not message.identifier == identifier:
                client_socket: socket = self.__client_sockets[identifier]
                message_dump = pickle.dumps(message)
                client_socket.sendall(message_dump)

    # Method to handle new client connections
    def __wait_for_clients(self):
        while not self.__server_shutdown.is_set():
            try:
                client_socket, address = self.socket.accept()

                handle_client_thread: Thread = Thread(target=self.on_new_client, args=(client_socket, address))
                handle_client_thread.start()
            except Exception as exception:
                # Accept method was aborted by socket's disconnection,
                # so we can ignore this
                if not (isinstance(exception, OSError) and exception.errno == 10038):
                    logger.warning(f'Error while waiting for clients {exception}')

        logger.info('Server stopped.')

    def on_message(self, message: Message):
        self.__broadcast(message)
