# -*- coding: utf-8 -*-
from flet import (
    Draggable,
    Text,
    alignment
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer
from loguru import logger


class TextElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)
        self._font = None

    def create(self, parent, draggable=False):
        self._text_ = Text()
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._text_),
                alignment=alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(self._text_, alignment=alignment.center)
        

        def onclick(e):
            pass
        self.onclick = onclick
    
    def updateSize(self):
        width, height = self.measureText(self.value, self.size)
        if width is not None and width > self.width:
            self.width = width
        if height is not None and height > self.height:
            self.height = height

    def set_value(self, value):
        self._text_.value = value
        if self._text_.expand == True:
            self.updateSize()

    def set_font_size(self, value):
        if value == "None":
            self._text_.size = 20
        else:
            self._text_.size = value
    
    def set_font_weight(self, value):
        self._text_.weight = value
    
    def set_weight(self, value):
        self._text_.weight = value
    
    def set_italic(self, value):
        self._text_.italic = FletBaseElement.bool(value)
    
    def set_overflow(self, value):
        if value in ["clip", "ellipsis", "fade", "visible"]:
            self._text_.overflow = value
        else:
            self._text_.overflow = None
    
    def set_selectable(self, value):
        self._text_.selectable = FletBaseElement.bool(value)
    
    def set_no_wrap(self, value):
        self._text_.no_wrap = FletBaseElement.bool(value)

    def set_color(self, value):
        self._text_.color = value

    def set_text_align(self, value):
        if value == "left":
            self._obj_.alignment = alignment.center_left
        elif value == "center":
            self._obj_.alignment = alignment.center
        elif value == "right":
            self._obj_.alignment = alignment.center_right
        else:
            self._obj_.alignment = alignment.center

        if value == "None":
            self._text_.text_align = "center"
        else:
            self._text_.text_align = value

    def set_height(self, value):
        self.obj.height = value
        self.padding_top = self.height / 2 -  self.font_size / 2

    def set_padding_left(self, value):
        self.obj.set_padding_left(value)

    def set_padding_top(self, value):
        self.obj.set_padding_top(0)

    def set_padding_right(self, value):
        self.obj.set_padding_right(value)

    def set_padding_bottom(self, value):
        self.obj.set_padding_bottom(value)

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "value": self._text_.value
        })
        return attributes

    @property
    def style(self):
        if self._text_.text_align is None:
            self._text_.text_align = "center"
        style = super().style
        style.update({
            "color": self._text_.color,
            "font-size": self._text_.size,
            "text-align": self._text_.text_align
        })
        return style

    def set_attributes(self, node):
        super().set_attributes(node)
        style = node["attributes"]['style']
        self.font_size = style['font-size']
        self.color = style['color']
        self.text_align = style['text-align']
        # attr
        attributes = node['attributes']
        self.value = attributes["value"]

    def set_tiny_attributes(self, data):
        style = data['style']
        self.font_size = style['font-size']
        self.color = style['color']
        self.text_align = style['text-align']
        # attr
        self.value = data["value"]

    @classmethod
    def defaut_style(cls):
        return {
            "width": 120,
            "height": 40,
            "border-width": 0,
            "border-color": "transparent",
            "background-color": "transparent",
            "color": "white",
            "font-size": 20,
            "text-align": "center",
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "value": "evue",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "text", left, top)
