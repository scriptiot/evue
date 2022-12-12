# -*- coding: utf-8 -*-
from flet import (
    Draggable,
    ResponsiveRow,
    alignment
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer
from loguru import logger


class ResponsiveRowElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._row_ = ResponsiveRow([], expand=True)
        self._controls_ = self._row_.controls
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._row_), 
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(
                self._row_,
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

    def set_alignment(self, value):
        self._row_.alignment = FletBaseElement.alignment(value)

    def set_spacing(self, value):
        self._row_.spacing = int(value)
        self._row_.run_spacing = int(value)
    
    def set_cols(self, value):
        if isinstance(value, str):
            col = {}
            items = value.split("-")
            for i in range(0, int(len(items)/2)):
                col[items[i * 2]] = int(items[i * 2+1])
            self['col'] = col
        else:
            self['col'] = col

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        style = attributes['style']
        # attr
        self.spacing = attributes["spacing"]
        self.alignment = attributes["alignment"]
        self.cols = attributes["cols"]

    def set_tiny_attributes(self, attributes):
        # attr
        self.spacing = attributes["spacing"]
        self.alignment = attributes["alignment"]
        self.cols = attributes["cols"]

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "spacing": self._row_.spacing,
            "alignment": self._row_.alignment,
            'cols': self.cols
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
            "spacing": 5,
            "alignment": "start",
            "cols": "sm-6-md-4-xl-3",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "responsiverow", left, top)
