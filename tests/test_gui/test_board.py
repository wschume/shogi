import flet as ft
import pytest

from src.shogi.gui.board import Board, BoardControl
from src.shogi.gui.field import Piece


@pytest.mark.flet
def test_simple(ft_app):
    def main(page: ft.Page):
        board = Board()
        board[1, 0].piece = Piece("L", "P1")
        board[1, 3].piece = Piece("L", "P2")

        board_control = BoardControl(board)

        page.add(board_control)

    ft_app(main, visible=True, window_size=(200, 200))
