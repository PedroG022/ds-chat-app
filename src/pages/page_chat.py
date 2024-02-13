from threading import Thread
from typing import Optional

import flet as ft
from fletrt import Route

from src.controls import MessageBubble
from src.infra import Client, Message


class PageChat(Route):
    def __init__(self):
        super().__init__()

        self.client: Client
        self.identifier: str

        self.send_button: Optional[ft.IconButton] = None
        self.message_field: Optional[ft.TextField] = None

        self.page: Optional[ft.Page] = None

        self.chat_content: Optional[ft.Column] = None

        self.username: Optional[str] = None
        self.port: Optional[int] = None

    def __on_message(self, message: Message):
        bubble = MessageBubble(message, self.identifier)

        self.chat_content.controls.append(bubble)
        self.page.update()

    def __send_message(self):
        body: str = self.message_field.value

        message: Message = Message(body, identifier=self.identifier)

        self.client.send_message(message)

        bubble = MessageBubble(message, self.identifier)
        self.chat_content.controls.append(bubble)

        self.message_field.value = ''
        self.page.update()

    def body(self):
        self.port = self.page.session.get('port')
        self.username = self.page.session.get('username')

        self.chat_content = ft.Column(scroll=ft.ScrollMode.HIDDEN)

        self.message_field = ft.TextField(label='Write your message', width=self.page.width - 70,
                                          on_submit=lambda _: self.__send_message())

        self.send_button = ft.IconButton(ft.icons.SEND_SHARP, bgcolor=ft.colors.TEAL_700,
                                         on_click=lambda _: self.__send_message())

        container_root = ft.Container(
            expand=True,
            content=ft.Stack(
                controls=[
                    ft.Container(
                        content=self.chat_content,
                        bottom=70,
                        top=0,
                        right=0,
                        left=0,
                    ),
                    ft.Container(
                        ft.Row([
                            self.message_field,
                            self.send_button
                        ]),
                        bottom=0
                    )
                ]
            )
        )

        thread_start_client = Thread(target=self.__start_client, args=(self.port,))
        thread_start_client.start()

        return container_root

    def __start_client(self, port: int):
        self.client: Client = Client('127.0.0.1', port, self.username)

        try:
            self.identifier = self.client.connect()
        except:
            self.go('/error')

        self.client.set_on_message_handler(self.__on_message)
