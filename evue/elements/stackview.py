# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from flet import (
    Column,
    Draggable,
    alignment
)
from .widgets import BaseContainer
from .column import ColumnElement
from .div import DivElement
from loguru import logger

class StackViewElement(DivElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self._currentElement_ = None

    def childAdded(self, element):
        currentIndex = self['currentIndex']
        for i, el in enumerate(self.listElements):
            if currentIndex == i:
                self._currentElement_ = el
                self._currentElement_.show()
            else:
                el.visible = False

    def set_currentIndex(self, value):
        lastElement = self._currentElement_
        if lastElement:
            lastElement.hide()
        for i, el in enumerate(self.listElements):
            if value == i:
                self._currentElement_ = el
                self._currentElement_.show()

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        self.currentIndex = attributes["currentIndex"]

    def set_tiny_attributes(self, data):
        super().set_tiny_attributes(data)

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "currentIndex": self.currentIndex
        })
        return attributes

    @classmethod
    def defaut_attributes(cls):
        ret =  ColumnElement.defaut_attributes()
        ret.update({
            "currentIndex": 0
        })
        return ret

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "stackview", left, top)
