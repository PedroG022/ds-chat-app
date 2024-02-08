import flet as ft


class MessageBubble(ft.UserControl):
    def __init__(self, message: str, sender: str):
        super().__init__()

        self.__message = message
        self.__sender = sender

    def build(self):
        bubble = ft.Container(
            bgcolor=ft.colors.BLUE_700,
            border_radius=10,
            padding=8,
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Text(f'~{self.__sender}', size=12, weight=ft.FontWeight.W_600),
                    ft.Container(
                        ft.Text(self.__message),
                        margin=ft.margin.only(0, 8, 0, 0)
                    )
                ]
            )
        )

        return bubble
