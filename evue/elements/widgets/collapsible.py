# -*- coding: utf-8 -*-
from loguru import logger
from math import pi
from typing import Optional

from flet import Column, Container, Icon, Row, Text, icons, padding
from flet.control import Control
from .basecontainer import BaseContainer

class Collapsible(Column):
    def __init__(
        self,
        title: Optional[str] = "",
        content: Optional[Control]= None,
        icon: Optional[Control] = None,
        spacing: float = 3,
    ):
        super().__init__()
        self.icon = icon
        self.title = title
        self._text_ = Text(self.title)
        self.shevron = Icon(
            icons.KEYBOARD_ARROW_DOWN_ROUNDED,
            animate_rotation=100,
            rotate=0,
            color="white"
        )
        self.spacingContainer = BaseContainer(height=spacing)
        self.content = Column(
            [self.spacingContainer],
            height=0,
            spacing=0,
            animate_size=100,
            opacity=0,
            animate_opacity=100
        )
        self.spacing = 0

        self._switch_ = False

    def header_click(self, e=None):
        self.content.height = None if self.content.height == 0 else 0
        self.content.opacity = 0 if self.content.height == 0 else 1
        self.shevron.rotate = pi if self.shevron.rotate == 0 else 0
        self.update()
    
    def set_open(self, value):
        if value:
            self.content.height = 0
            self.content.opacity = 0 
            self.shevron.rotate = 0
        else:
            self.content.height = 0 
            self.content.opacity = 1 
            self.shevron.rotate = 0
        self.header_click()

    def set_switch(self, value):
        self._switch_ = value

    def _build(self):
        title_row = Row()
        if self.icon != None:
            title_row.controls.append(self.icon)
        title_row.controls.append(self._text_)
        self.controls.extend(
            [
                BaseContainer(
                    Row([title_row, self.shevron], alignment="spaceBetween"),
                    padding=padding.only(left=8, right=8),
                    height=38,
                    border_radius=4,
                    ink=True,
                    on_click=self.header_click
                ),
                self.content,
            ]
        )
