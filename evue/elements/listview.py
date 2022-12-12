# -*- coding: utf-8 -*-
import os
from flet import (
    Draggable,
    alignment,
    ListView
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer
from loguru import logger


class ListViewElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._listview_ = ListView(expand=True)
        self._controls_ = self._listview_.controls
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._listview_), 
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(
                self._listview_
            )
    @property
    def isContainer(self):
        return True

    @property
    def isLayout(self):
        return True

    def set_expand(self, value):
        self.obj.expend = FletBaseElement.bool(value)
        self._listview_.expend = FletBaseElement.bool(value)

    def set_horizontal(self, value):
        self._listview_.horizontal = FletBaseElement.bool(value)

    def set_spacing(self, value):
        self._listview_.spacing = value

    def set_divider(self, value):
        self._listview_.divider_thickness = value

    def set_padding(self, value):
        self._listview_.padding = value
    
    def set_onCurrentIndexChanged(self, value):
        self._listview_.currentIndex = value

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        style = attributes['style']
        # attr
        self.expand = attributes["expand"]
        self.horizontal = attributes["horizontal"]
        self.spacing = attributes["spacing"]
        self.divider = attributes["divider"]
        self.padding = attributes["padding"]

    def set_tiny_attributes(self, attributes):
        # attr
        self.expand = attributes["expand"]
        self.horizontal = attributes["horizontal"]
        self.spacing = attributes["spacing"]
        self.divider = attributes["divider"]
        self.padding = attributes["padding"]

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "expand": self._listview_.expand,
            "horizontal": self._listview_.horizontal,
            "spacing": self._listview_.spacing,
            "divider": self._listview_.divider_thickness,
            "padding": self._listview_.padding
        })
        return attributes

    @classmethod
    def defaut_style(cls):
        return {
            "left": 0,
            "top": 0,
            "width": 150,
            "height": 400,
            "border-width": 0,
            "border-radius": 0,
            "border-color": "transparent",
            "background-color": "white"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "expand": True,
            "horizontal": False,
            "spacing": 5,
            "divider": 0,
            "padding": 5,
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "listview", left, top)
