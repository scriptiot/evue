# -*- coding: utf-8 -*-
from flet import (
    Draggable,
    alignment,
    IconButton
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer


class IconButtonElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._button_ = IconButton()
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._button_), 
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(
                self._button_,
                alignment = alignment.center
            )

    def set_width(self, value):
        self._obj_.width = value

    def set_height(self, value):
        self._obj_.height = value

    def set_icon(self, value):
        from flet import icons
        if value.startswith("icons."):
            name = value[6:]
            if hasattr(icons, name):
                self._button_.icon = getattr(icons, name)
        else:
            self._button_.icon = value
    
    def set_name(self, value):
        self.set_icon(value)

    def set_size(self, value):
        self._button_.icon_size = value

    def set_color(self, value):
        self._button_.icon_color = value
    
    def set_tooltip(self, value):
        self._button_.tooltip = value

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "icon": self.icon,
            "size": self._button_.icon_size,
            "tooltip": self._button_.tooltip,
            "color": self._button_.icon_color
        })
        return attributes
    
    def set_attributes(self, node):
        super().set_attributes(node)
        # attr
        attributes = node['attributes']
        self.icon = attributes["icon"]
        self.size = attributes["size"]
        self.tooltip = attributes["tooltip"]
        self.color = attributes["color"]


    @classmethod
    def defaut_style(cls):
        return {
            "left": 0,
            "top": 0,
            "width": 64,
            "height": 64,
            "border-width": 0,
            "border-color": "transparent",
            "background-color": "transparent"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "icon": "icons.INSERT_EMOTICON_SHARP",
            "tooltip": "smile",
            "size": 48,
            "color": "white",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "iconbutton", left, top)
