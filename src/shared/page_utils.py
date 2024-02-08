import flet as ft


def configure_window(page: ft.Page):
    page.window_center()
    page.window_maximizable = False

    set_window_size(page, page.width / 3, page.height * 1.15)


def set_window_size(page: ft.Page, width: int, height: int):
    page.window_min_width = width
    page.window_min_height = height

    page.window_width = width
    page.window_height = height

    page.window_max_width = width
    page.window_max_height = height

    page.update()
