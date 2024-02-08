import threading

import flet as ft

from infra import Server


def main(page: ft.Page):
    pass


def start(port: int, headless: bool = False):
    if not headless:
        ui_thread = threading.Thread(target=__start_ui)
        ui_thread.start()

    server_thread = threading.Thread(target=__start_server, args=(port,))
    server_thread.start()


def __start_ui():
    ft.app(target=main)


def __start_server(port: int):
    server: Server = Server(port)
    server.start()
