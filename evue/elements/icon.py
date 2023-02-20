# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from flet import (
    Draggable,
    alignment,
    Icon,
    icons
)
from .widgets import BaseContainer


class IconElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._icon_ = Icon()
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._icon_), 
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(
                self._icon_,
                alignment = alignment.center
            )
        
        def onclick(e):
            pass
        self.onclick = onclick

    def set_width(self, value):
        self._obj_.width = value
        self._icon_.width = value

    def set_height(self, value):
        self._obj_.height = value
        self._icon_.height = value

    def set_name(self, value):
        if value.startswith("icons."):
            name = value[6:]
            if hasattr(icons, name):
                self._icon_.name = getattr(icons, name)
        else:
            self._icon_.name = value

    def set_size(self, value):
        self._icon_.size = int(value)
    
    def set_color(self, value):
        self._icon_.color = value

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "name": self._icon_.name
        })
        return attributes
    
    def set_attributes(self, node):
        super().set_attributes(node)
        # attr
        attributes = node['attributes']
        self.name = attributes["name"]


    @classmethod
    def defaut_style(cls):
        return {
            "left": 0,
            "top": 0,
            "border-width": 0,
            "border-color": "#282828",
            "background-color": "#282828"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "name": "/image/logo.png",
            "size": 32,
            "style": cls.defaut_style()
        }
    
    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "image", left, top)
