from dataclasses import dataclass, field as dataclass_field
from typing import cast

import flet as ft
from blinker import Signal
from flet import canvas as cv

from src.shogi.gui.field import Field, FieldControl


@dataclass
class Board:
    width: int = 3
    height: int = 4

    fields: list[Field] = dataclass_field(init=False, default_factory=list)

    on_field_click: Signal = dataclass_field(init=False, default_factory=Signal)

    def __post_init__(self):
        self.fields = [Field() for _ in range(self.width * self.height)]

        for field in self.fields:
            field.on_click.connect(self._on_click)

    def iter_fields(self):
        for i in range(self.width):
            for j in range(self.height):
                yield (i, j), self[i, j]

    def __getitem__(self, key: tuple[int, int]) -> Field:
        x, y = key
        return self.fields[y * self.width + x]

    def _on_click(self, field: Field):
        self.on_field_click.send(field)


class BoardControl(ft.Container):
    def __init__(self, board: Board):
        super().__init__(ft.ControlBuilder(board, self._build))

        self._board = board

    @property
    def board_width(self) -> int:
        return Field.field_size * self._board.width

    @property
    def board_height(self):
        return Field.field_size * self._board.height

    @property
    def inner_control(self) -> ft.Container:
        return cast(ft.Container, cast(ft.ControlBuilder, self.content).content)

    @staticmethod
    def _build(board: Board) -> ft.Container:
        stroke_paint = ft.Paint(
            ft.Colors.WHITE, stroke_width=2, style=ft.PaintingStyle.STROKE
        )
        board_width = Field.field_size * board.width
        board_height = Field.field_size * board.height
        canvas = cv.Canvas(
            [
                cv.Rect(
                    0,
                    0,
                    board_width,
                    board_height,
                    paint=stroke_paint,
                )
            ]
        )

        stack = ft.Stack([canvas])
        for i in range(board.width):
            for j in range(board.height):
                stack.controls.append(
                    ft.Container(
                        FieldControl(board[i, j]),
                        bottom=j * Field.field_size,
                        left=i * Field.field_size,
                    )
                )

        return ft.Container(
            content=stack,
            width=board_width,
            height=board_height,
        )
