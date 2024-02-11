import flet as ft
from fletrt import Router

from src.pages import PageChat, PageConnect, PageError


class ClientApp:
    def __init__(self, port: int, headless: bool = False):
        self.port = port
        self.headless = headless

    def __main(self, page: ft.Page):
        page.session.set('port', self.port)
        page.session.set('headless', self.headless)

        router: Router = Router(page, routes={
            '/': PageConnect(),
            '/chat': PageChat(),
            '/error': PageError()
        })

        router.install()

    def start(self):
        ft.app(target=self.__main)
