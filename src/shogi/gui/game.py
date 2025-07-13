from dataclasses import dataclass, field as dataclass_field
from typing import Literal, cast

import flet as ft
import flet.canvas as cv

from .board import Board, BoardControl
from .field import Field, Piece


@dataclass
class Game:
    board: Board
    current_player: Literal["P1", "P2"] = dataclass_field(init=False, default="P1")

    @classmethod
    def from_animal_shogi(cls) -> "Game":
        board = Board()

        board[1, 0].piece = Piece("L", "P1")
        board[1, 3].piece = Piece("L", "P2")
        board[0, 0].piece = Piece("E", "P1")
        board[0, 3].piece = Piece("G", "P2")
        board[2, 0].piece = Piece("G", "P1")
        board[2, 3].piece = Piece("E", "P2")
        board[1, 1].piece = Piece("C", "P1")
        board[1, 2].piece = Piece("C", "P2")

        return cls(board)

    def __post_init__(self):
        self.board.on_field_click.connect(self._on_field_click)

        self.setup_next_turn(self.current_player)

    def _on_field_click(self, field: Field):
        if field.selected:
            field.selected = False
            return

        for f in self.board.fields:
            if f.selected:
                field.piece = f.piece
                f.piece = None
                f.selected = False

                self.setup_next_turn()
                return

        field.selected = True
        for f in self.board.fields:
            f.selectable = True

    def setup_next_turn(self, next_player: Literal["P1", "P2"] | None = None):
        if next_player is None:
            next_player = "P1" if self.current_player == "P2" else "P2"

        for field in self.board.fields:
            field.selected = False
            if field.piece is None or field.piece.possession != next_player:
                field.selectable = False

        self.current_player = cast(Literal["P1", "P2"], next_player)


class GameControl(ft.Container):
    def __init__(self, game: Game):
        super().__init__(ft.ControlBuilder(game, self._build))

    @staticmethod
    def _build(game: Game) -> ft.Stack:
        board_control = BoardControl(game.board)

        p1_dot = cv.Canvas(
            [
                cv.Circle(
                    0,
                    0,
                    5,
                    paint=ft.Paint(
                        ft.Colors.GREEN
                        if game.current_player == "P1"
                        else ft.Colors.GREY_500
                    ),
                )
            ],
            left=board_control.board_width + 20,
            bottom=10,
        )

        p2_dot = cv.Canvas(
            [
                cv.Circle(
                    0,
                    0,
                    5,
                    paint=ft.Paint(
                        ft.Colors.GREEN
                        if game.current_player == "P2"
                        else ft.Colors.GREY_500
                    ),
                )
            ],
            left=board_control.board_width + 20,
            top=10,
        )

        return ft.Stack(
            [board_control, p1_dot, p2_dot], width=board_control.board_width + 25
        )
