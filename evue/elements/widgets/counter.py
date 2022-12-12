# -*- coding: utf-8 -*-
from asyncio.log import logger
from math import pi
from typing import Optional

from flet import IconButton, Container, TextField, Text, Row, border, alignment, border_radius, icons, padding
from flet.control import Control
from .basecontainer import BaseContainer

class Counter(BaseContainer):
    def __init__(self):
        super().__init__()
        bgcolor = "transparent"

        self.minusIconButton = IconButton(icons.REMOVE, bgcolor=bgcolor, on_click=self.minus_click, icon_size=14)
        self.addIconButton = IconButton(icons.ADD, bgcolor=bgcolor, on_click=self.plus_click, icon_size=14)
        self.text_number = TextField(value="0", filled=True, bgcolor=bgcolor, text_align="center")
        self.text_number.border_width = 0

        self.content = Row([
            self.minusIconButton,
            self.text_number,
            self.addIconButton
        ], alignment="center", spacing=0, run_spacing=0)

        self.alignment = alignment.center
        
        self._on_change = None
        
        def on_change(e):
            self._on_change(int(e.control.value))
        
        def on_submit(e):
            logger.warning(e.control.value)
            self._on_change(int(e.control.value))

        self.text_number.on_change = on_change
        self.text_number.on_submit = on_submit

    @property
    def on_change(self):
        return self._on_change

    @on_change.setter
    def on_change(self, value):
        self._on_change = value

    def minus_click(self, e):
        self._on_change(int(self.text_number.value) - 1)
        self.update()
    
    def plus_click(self, e):
        self._on_change(int(self.text_number.value) + 1)
        self.update()

    def _build(self):
        pass
    
    def set_width(self, value):
        self.width = value
        self.text_number.width = value - 80

    def set_font_size(self, value):
        self.addIconButton.icon_size = value
        self.minusIconButton.icon_size = value
        self.text_number.text_size = value
        self.text_number.height = value + 6

    def set_color(self, value):
        self.addIconButton.icon_color = value
        self.minusIconButton.icon_color = value
        self.text_number.color = value

    def set_value(self, value):
        self.text_number.value = value
