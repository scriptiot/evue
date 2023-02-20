# -*- coding: utf-8 -*-
import os
from flet import (
    Draggable,
    WindowDragArea,
    Stack,
    alignment
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer
from loguru import logger
from ..globalthis import globalThis


class WindowtitlebarElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._stack_ = Stack([])
        self._controls_ = self._stack_.controls
        self._windowDragArea_ = WindowDragArea(content=BaseContainer(self._stack_))
        self._obj_ = BaseContainer(
                self._windowDragArea_,
                alignment = alignment.center
            )

    @property
    def isContainer(self):
        return True

    @property
    def isLayout(self):
        return False

    @property
    def attributes(self):
        attributes = super().attributes
        return attributes

    def set_attributes(self, node):
        super().set_attributes(node)
        # attr
        attributes = node['attributes']

    @classmethod
    def defaut_style(cls):
        style = FletBaseElement.defaut_style()
        style.update({
            "background-color": "transparent"
        })
        return style

    @classmethod
    def defaut_attributes(cls):
        return {
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "windowtitlebar", left, top)
