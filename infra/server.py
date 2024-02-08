import logging
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Event

logger = logging.getLogger(__name__)


class Server:

    # Server's parameters initialization
    def __init__(self, port: int):
        self.socket: socket = socket(AF_INET, SOCK_STREAM)

        self.host = '127.0.0.1'
        self.port = port

        self.__server_shutdown: Event = Event()
        self.__client_sockets: list[socket] = []

    # Method to start the server
    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        listen_for_clients = Thread(target=self.__wait_for_clients)
        listen_for_clients.start()

        logger.info('Server started successfully, waiting for connections...')

    # Method to start the server
    def stop(self):
        self.__server_shutdown.set()
        self.socket.close()

    def on_new_client(self, client_socket: socket, address: tuple):
        self.__client_sockets.append(client_socket)
        logger.info(f'New client {client_socket.getsockname()}')

    # Method to handle new client connections
    def __wait_for_clients(self):
        while not self.__server_shutdown.is_set():
            try:
                c, addr = self.socket.accept()

                handle_client_thread: Thread = Thread(target=self.on_new_client, args=(c, addr))
                handle_client_thread.start()
            except Exception as exception:
                if isinstance(exception, OSError) and exception.errno == 10038:
                    logger.warning('Tried to listen to a non socket object!')

        logger.info('Stopped listening for new connections.')

    def on_message(self, message):
        pass
