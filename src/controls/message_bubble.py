import flet as ft

from src.entities import Message


class MessageBubble(ft.UserControl):
    def __init__(self, message: Message, self_identifier: str):
        super().__init__()

        self.__message: Message = message
        self.__owner = self.__message.identifier == self_identifier

    def build(self):
        is_server = self.__message.identifier and self.__message.identifier.client_id == 'SERVER'
        bubble_color = ft.colors.BLUE_700

        if self.__owner:
            bubble_color = ft.colors.GREEN_500

        if is_server:
            bubble_color = ft.colors.GREY_800

        sender_title = None

        if self.__message.identifier:
            sender_title = ft.Text(f'{self.__message.identifier.name}', size=12, weight=ft.FontWeight.W_600)

        message_content = ft.Text(self.__message.body)

        margin_top = 8 if not (self.__owner or is_server) else 0

        holder_column = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        )

        if not self.__owner and self.__message.identifier and not is_server:
            holder_column.controls.append(sender_title)

        holder_column.controls.append(ft.Container(
            margin=ft.margin.only(0, margin_top, 0, 0),
            content=message_content
        ))

        bubble = ft.Container(
            bgcolor=bubble_color,
            border_radius=10,
            padding=8,
            content=holder_column
        )

        alignment = None

        if self.__owner:
            alignment = ft.MainAxisAlignment.END

        if is_server:
            alignment = ft.MainAxisAlignment.CENTER

        return ft.Row(
            [bubble],
            alignment=alignment,
        )
