# -*- coding: utf-8 -*-
from flet import (
    Draggable,
    Row,
    alignment
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer


class RowElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._row_ = Row([], expand=True)
        self._row_.scroll = "auto"
        self._controls_ = self._row_.controls
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._row_), 
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(
                self._row_
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
        self._row_.scroll = value

    def set_auto_scroll(self, value):
        if value == "None" or value is None:
            self._row_.auto_scroll = None
        else:
            self._row_.auto_scroll = FletBaseElement.bool(value)

    def set_alignment(self, value):
        self._row_.alignment = FletBaseElement.alignment(value)

    def set_wrap(self, value):
        self._row_.wrap = FletBaseElement.bool(value)

    def set_spacing(self, value):
        self._row_.spacing = int(value)
        self._row_.run_spacing = int(value)
    
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

    def set_tiny_attributes(self, data):
        # attr
        self.scroll = data["scroll"]
        self.auto_scroll = data["auto_scroll"]
        self.wrap = data["wrap"]
        self.spacing = data["spacing"]
        self.alignment = data["alignment"]

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "scroll": self._row_.scroll,
            "auto_scroll": self._row_.auto_scroll,
            "wrap": self._row_.wrap,
            "spacing": self._row_.spacing,
            "alignment": self._row_.alignment
        })
        return attributes

    @classmethod
    def defaut_style(cls):
        return {
            "left": 0,
            "top": 0,
            "width": 200,
            "height": 40,
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
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "row", left, top)
