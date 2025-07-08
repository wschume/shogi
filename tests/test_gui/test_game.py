import flet as ft

from shogi.gui.game import Game, GameControl


def test_simple(ft_app):
    def main(page: ft.Page):
        game = Game.from_animal_shogi()
        game_control = GameControl(game)

        page.add(game_control)

    ft_app(main, visible=True, window_size=(200, 200))
