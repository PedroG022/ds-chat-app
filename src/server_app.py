from threading import Thread

from src.infra import Server, Identifier, Message


class ServerApp:
    def __init__(self, port: int):
        self.server: Server = Server(port)

        self.server.on_new_client = self.on_new_client
        self.server.on_message_received = self.on_message_received
        self.server.on_client_disconnect = self.on_client_disconnect

        self.identifier: Identifier = Identifier('SERVER')
        self.identifier.id = 'SERVER'

    def on_new_client(self, identifier: Identifier):
        join_message: Message = Message(body=f'{identifier.name} JOINED THE CHAT', identifier=self.identifier)
        self.server.broadcast(join_message)

    def on_message_received(self, message: Message):
        self.server.broadcast(message)

    def on_client_disconnect(self, identifier: Identifier):
        left_message: Message = Message(body=f'{identifier.name} LEFT THE CHAT',
                                        identifier=self.identifier)
        self.server.broadcast(left_message)

    def start(self):
        server_thread = Thread(target=self.__start_server)
        server_thread.start()

    def __start_server(self):
        self.server.start()
