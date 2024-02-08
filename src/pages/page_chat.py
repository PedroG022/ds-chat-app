from threading import Thread
from typing import Optional

import flet as ft
from fletrt import Route

from src.controls import MessageBubble
from src.infra import Client
from src.shared import configure_window


class PageChat(Route):
    def __init__(self):
        super().__init__()

        self.client: Client

        self.send_button: Optional[ft.IconButton] = None
        self.message_field: Optional[ft.TextField] = None

        self.page: Optional[ft.Page] = None

        self.chat_content: Optional[ft.Column] = None

    def on_message(self, message: str):
        bubble = MessageBubble(message, 'server')

        self.chat_content.controls.append(bubble)
        self.page.update()

    def __send_message(self):
        message: str = self.message_field.value
        self.client.send_message(message)

        self.message_field.value = ''
        self.page.update()

    def body(self):
        port: int = self.page.session.get('port')

        configure_window(self.page)

        self.message_field: ft.TextField = ft.TextField(hint_text='Mensagem')
        self.send_button: ft.IconButton = ft.IconButton(ft.icons.SEND, width=50, height=50,
                                                        on_click=lambda _: self.__send_message())

        self.chat_content: ft.Column = ft.Column()

        root = ft.Stack(
            expand=True,
        )

        col = ft.Column(
            top=0,
            controls=[
                self.chat_content
            ]
        )

        row = ft.Row(
            bottom=0,
            controls=[
                self.message_field,
                self.send_button
            ]
        )

        root.controls.append(col)
        root.controls.append(row)

        client_thread: Thread = Thread(target=self.__start_client, args=(port,))
        client_thread.start()

        return root

    def __start_client(self, port: int):
        self.client: Client = Client('127.0.0.1', port)
        self.client.connect()