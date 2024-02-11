import flet as ft
from flet_core import View
from fletrt import Route


class PageError(Route):
    def body(self):
        col = ft.Column(
            controls=[
                ft.Text('There was an error while connecting to the server'),
                ft.Row([ft.ElevatedButton('Try again', on_click=lambda _: self.pop(), expand=True)])
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return col

    def view(self) -> View:
        base = super().view()

        base.vertical_alignment = ft.MainAxisAlignment.CENTER
        base.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        return base
