from threading import Thread

from src.infra import Server


class ServerApp:
    def __init__(self, port: int):
        self.server: Server = Server(port)

    def start(self):
        server_thread = Thread(target=self.__start_server)
        server_thread.start()

    def __start_server(self):
        self.server.start()
