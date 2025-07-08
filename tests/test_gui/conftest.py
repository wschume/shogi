from typing import Callable

import flet as ft

import pytest


@pytest.fixture
def ft_app():
    def run_inside_flet(
        test_main: Callable[[ft.Page], None],
        *,
        visible: bool = False,
        theme_mode: ft.ThemeMode = ft.ThemeMode.DARK,
        window_size: tuple[int, int] = (800, 600),
    ):
        def main(page: ft.Page):
            page.window.width = window_size[0]
            page.window.height = window_size[1]
            page.theme_mode = theme_mode
            test_main(page)

            if not visible:
                page.window.destroy()

        ft.run(
            main=main,
            view=ft.AppView.FLET_APP_HIDDEN if not visible else ft.AppView.FLET_APP,
        )

    return run_inside_flet
