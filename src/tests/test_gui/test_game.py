import flet as ft
import pytest

from src.shogi.gui.game import Game, GameControl


@pytest.mark.flet
def test_simple(ft_app):
    def main(page: ft.Page):
        game = Game.from_animal_shogi()
        game_control = GameControl(game)

        page.add(game_control)

    ft_app(main, visible=True, window_size=(200, 200))


def test_click():
    game = Game.from_animal_shogi()

    assert game.current_player == "P1"
    assert game.board[1, 1].piece is not None
    assert game.board[1, 1].piece.piece_type == "C"
    assert game.board[1, 1].piece.possession == "P1"

    assert game.board[1, 2].piece is not None
    assert game.board[1, 2].piece.piece_type == "C"
    assert game.board[1, 2].piece.possession == "P2"

    game.board[1, 1].click()
    game.board[1, 2].click()

    assert game.current_player == "P2"
    assert game.board[1, 1].piece is None

    assert game.board[1, 2].piece is not None
    assert game.board[1, 2].piece.piece_type == "C"
    assert game.board[1, 2].piece.possession == "P1"
