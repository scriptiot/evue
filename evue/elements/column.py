# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from flet import (
    Column,
    Draggable,
    alignment
)
from .widgets import BaseContainer

class ColumnElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._column_ = Column([])
        self._column_.alignment = "start"
        self._column_.horizontal_alignment = "start"
        # self._column_.scroll = "always"
        # self._column_.auto_scroll = True
        self._controls_ = self._column_.controls
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._column_), 
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(
                self._column_,
                alignment = alignment.top_left
            )
    @property
    def isContainer(self):
        return True

    @property
    def isLayout(self):
        return True

    def set_width(self, value):
        self._obj_.width = value

    def set_height(self, value):
        self._obj_.height = value

    def set_scroll(self, value):
        self._column_.scroll = value
    
    def set_auto_scroll(self, value):
        self._column_.auto_scroll = value
    
    def set_alignment(self, value):
        self._column_.alignment = FletBaseElement.alignment(value)
    
    def set_horizontal_alignment(self, value):
        self._column_.horizontal_alignment = FletBaseElement.alignment(value)

    def set_wrap(self, value):
        self._column_.wrap = FletBaseElement.bool(value)

    def set_spacing(self, value):
        self._column_.spacing = value

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        style = attributes['style']
        # attr
        self.scroll = attributes["scroll"]
        self.auto_scroll = attributes["auto_scroll"]
        self.wrap = attributes["wrap"]
        self.spacing = attributes["spacing"]
        self.alignment = attributes["alignment"]
        self.horizontal_alignment = attributes["horizontal_alignment"]

    def set_tiny_attributes(self, data):
        # attr
        self.scroll = data["scroll"]
        self.auto_scroll = data["auto_scroll"]
        self.wrap = data["wrap"]
        self.spacing = data["spacing"]
        self.alignment = data["alignment"]
        self.horizontal_alignment = data["horizontal_alignment"]

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "scroll": self._column_.scroll,
            "auto_scroll": self._column_.auto_scroll,
            "wrap": self._column_.wrap,
            "spacing": self._column_.spacing,
            "alignment": self._column_.alignment,
            "horizontal_alignment": self._column_.horizontal_alignment
        })
        return attributes

    @classmethod
    def defaut_style(cls):
        return {
            "left": 0,
            "top": 0,
            "width": 40,
            "height": 200,
            "border-width": 0,
            "border-radius": 0,
            "border-color": "transparent",
            "background-color": "white"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "scroll": "auto",
            "auto_scroll": True,
            "wrap": True,
            "spacing": 5,
            "alignment": "start",
            "horizontal_alignment": "start",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "column", left, top)
