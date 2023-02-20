# -*- coding: utf-8 -*-
import os
from loguru import logger
from .fletbaseelement import FletBaseElement
from flet import (
    Stack,
    Draggable,
    alignment,
    types
)
from .widgets import EvueContainer, BaseContainer
from .image import getSize


class DivElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._stack_ = Stack([])
        self._div_ = EvueContainer(
            self._stack_
        )
        self._controls_ = self._stack_.controls
        if draggable:
            draggable = Draggable(content=self._div_)
            self._obj_ = EvueContainer(
                draggable, 
                alignment = alignment.center
            )
            self._div_.element = self
        else:
            self._obj_ = self._div_

    @property
    def isContainer(self):
        return True

    @property
    def isLayout(self):
        return False

    def set_width(self, value):
        self._obj_.width = value

    def set_height(self, value):
        self._obj_.height = value
    
    def set_src(self, value):
        if value in self.resources:
            self._obj_.image_src_base64 = self.resources[value]
            return

        from evue import globalThis
        if value.startswith("http"):
            self._obj_.image_src = f"%s" % value
        else:
            if globalThis.isWeb():
                value = "http://%s:%d/%s" % (globalThis.server_ip, globalThis.port, value)
            else:
                size = getSize(value)
                self.width = size[0]
                self.height = size[1]
            self._obj_.image_src = f"%s" % value

    def set_image_src_base64(self, value):
        self._obj_.image_src_base64 = value

    def set_image_repeat(self, value):
        self._obj_.image_repeat = value

    def set_image_fit(self, value):
        self._obj_.image_fit = value

    def set_image_opacity(self, value):
        self._obj_.image_opacity = value
    
    def set_shape(self, value):
        if value == "rectangle":
            self._obj_.shape = types.BoxShape.RECTANGLE
        else:
            self._obj_.shape = types.BoxShape.CIRCLE

    def set_attributes(self, node):
        super().set_attributes(node)
    
    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "div", left, top)
