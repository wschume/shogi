import math
from dataclasses import dataclass, field as dataclass_field
from typing import ClassVar, Literal

import flet as ft
from blinker import Signal


@dataclass
class Piece:
    piece_type: Literal["L", "G", "E", "C", "H"]
    possession: Literal["P1", "P2"]


@dataclass
class Field:
    piece: Piece | None = None
    selectable: bool = True
    selected: bool =False

    field_size: ClassVar[int] = 40

    on_click: Signal = dataclass_field(init=False, default_factory=Signal)

    def click(self):
        self.on_click.send(self)


class FieldControl(ft.Container):
    def __init__(self, field: Field):
        super().__init__(ft.ControlBuilder(field, self._build))

        self._field = field

    @staticmethod
    def _build(field: Field) -> ft.Container:
        container = ft.Container(
            width=Field.field_size,
            height=Field.field_size,
            alignment=ft.Alignment.CENTER,
        )

        if field.selectable:
            container.on_click = field.click

        if field.selected:
            container.border = ft.border.all(2, ft.Colors.BLUE)

        if field.piece is not None:
            container.content = ft.Container(
                ft.Text(
                    field.piece.piece_type,
                    color=ft.Colors.WHITE if field.selectable else ft.Colors.GREY_500,
                ),
                rotate=0 if field.piece.possession == "P1" else math.pi,
            )

        return container
