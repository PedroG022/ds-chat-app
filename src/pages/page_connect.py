import flet as ft
from flet_core import View
from fletrt import Route

from src.shared import configure_window


class PageConnect(Route):
    def __confirm_user(self, username: str):
        self.page.session.set('username', username)
        self.go('/chat')

    def body(self):
        configure_window(self.page)
        column = ft.Column()

        button_style = ft.ButtonStyle(
            shape={
                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=8),
            },
        )

        username_field = ft.TextField(label='Username', on_submit=lambda _: self.__confirm_user(username_field.value))
        confirm_button = ft.ElevatedButton('Connect', expand=True, height=50, style=button_style,
                                           on_click=lambda _: self.__confirm_user(username_field.value))

        wrapper_row = ft.Row()
        wrapper_row.controls.append(confirm_button)

        column.controls = [username_field, wrapper_row]

        return column

    def view(self) -> View:
        base = super().view()

        base.vertical_alignment = ft.MainAxisAlignment.CENTER
        base.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        base.padding = 16

        return base
