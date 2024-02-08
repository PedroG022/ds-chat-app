from threading import Thread

import flet as ft

from infra import Client


def main(page: ft.Page):
    pass


def start(port: int, headless: bool = False):
    ui_thread: Thread = Thread(target=lambda: ft.app(target=main))
    ui_thread.start()

    client_thread: Thread = Thread(target=__start_client, args=(port,))
    client_thread.start()


def __start_client(port: int):
    client: Client = Client('127.0.0.1', port)
    client.connect()
