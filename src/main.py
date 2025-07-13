import flet as ft

from shogi.gui.game import Game, GameControl


def before_main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 640
    page.window.height = 480


def flet_main(page: ft.Page) -> None:
    game = Game.from_animal_shogi()
    game_control = GameControl(game)

    page.add(ft.SafeArea(game_control))


def main() -> None:
    ft.run(flet_main, before_main)


if __name__ == "__main__":
    main()
