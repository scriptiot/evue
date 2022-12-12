# -*- coding: utf-8 -*-
from flet import Text, ElevatedButton, alignment, Draggable, icons
from loguru import logger
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer
from .text import TextElement


class ButtonElement(TextElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)

    def create(self, parent, draggable=False):
        self._text_ = Text(expand=True)
        self._button_ = ElevatedButton(content=self._text_, expand=True)
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._button_),
                alignment=alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(self._button_, alignment=alignment.center)

    def set_width(self, value):
        self._obj_.width = value
        self._button_.width = value

    def set_height(self, value):
        self._obj_.height = value
        self._button_.height = value

    def set_icon(self, value):
        self._button_.icon = getattr(icons, value)

    def set_background_color(self, value):
        self._button_.bgcolor = value
    
    def set_value(self, value):
        super().set_value(value)

    @classmethod
    def defaut_style(cls):
        return {
            "border-width": 0,
            "border-color": "transparent",
            "background-color": "#282828",
            "color": "white",
            "font-size": 20,
            "text-align": "center"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "value": "button",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "button", left, top)
