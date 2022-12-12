# -*- coding: utf-8 -*-
from itertools import cycle
from flet import (
    Stack,
    Draggable,
    alignment,
    border,
    border_radius,
    Tab,
    Text
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer


class TabElement(FletBaseElement):
    
    colors = cycle(
            ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4', '#fed9a6', '#ffffcc', '#e5d8bd', '#fddaec', '#f2f2f2',
             '#b3e2cd', '#fdcdac', '#cbd5e8', '#f4cae4', '#e6f5c9', '#fff2ae', '#f1e2cc', '#cccccc', '#8dd3c7',
             '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd',
             '#ccebc5', '#ffed6f'])

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._stack_ = Stack([])
        self._container_ = BaseContainer(self._stack_, expand=True, bgcolor="red", alignment=alignment.center)
        self._text_ = Text(color="white", bgcolor="transparent")
        self._tab_ = Tab(tab_content=self._text_, content=self._container_)
        self._controls_ = self._stack_.controls
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._tab_), 
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(self._tab_)
    
    def setParent(self, parent):
        if parent and parent.isContainer:
            self['parent'] = parent
            self['index'] = len(parent._controls_)
            parent._controls_.append(self._tab_)
            parent.elements[self.eid] = self
            parent.currentIndex = self['index']
    
    def delete_control(self):
        parent = self['parent']
        parent._controls_.remove(self._tab_)
        try:
            parent.obj.update()
        except:
            pass

    @property
    def isContainer(self):
        return True
    
    def set_left(self, value):
        self._obj_.left = value
    
    def set_top(self, value):
        self._obj_.top = value

    def set_width(self, value):
        self._obj_.width = value
        self._container_.width = value
    
    def set_height(self, value):
        self._obj_.height = value
        self._container_.height = value

    def set_background_color(self, value):
        self._obj_.bgcolor = value
        self._container_.bgcolor = value
    
    def set_border_width(self, value):
        self._obj_.bgcolor = border.all(value, self.border_color)
        self._container_.border = border.all(value, self.border_color)

    def set_border_radius(self, value):
        self._obj_.border_radius = border_radius.all(value)
        self._container_.border_radius = border_radius.all(value)

    def set_border_color(self, value):
        self._obj_.border = border.all(self.border_width, value)
        self._container_.border = border.all(self.border_width, value)

    def set_expand(self, value):
        self._obj_.expend = FletBaseElement.bool(value)
        self._tab_.expend = FletBaseElement.bool(value)

    def set_name(self, value):
        self._text_.value = value

    def set_font_size(self, value):
        if value == "None":
            self._text_.size = 20
        else:
            self._text_.size = value

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

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        style = node["attributes"]['style']
        self.font_size = style['font-size']
        self.color = style['color']
        self.text_align = style['text-align']
        # attr
        self.expand = attributes["expand"]
        self.name = attributes["name"]

    def set_tiny_attributes(self, attributes):
        self.font_size = attributes['font-size']
        self.color = attributes['color']
        self.text_align = attributes['text-align']
        # attr
        self.expand = attributes["expand"]
        self.name = attributes["name"]

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "expand": self._tab_.expand,
            "name": self._tab_.text,
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

    @classmethod
    def defaut_style(cls):
        color = next(cls.colors)
        return {
            "left": 0,
            "top": 0,
            "width": 400,
            "height": 400,
            "border-width": 0,
            "border-radius": 0,
            "border-color": "transparent",
            "background-color": color,
            "color": color,
            "font-size": 20,
            "text-align": "center"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "expand": True,
            "name": "tab",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "tab", left, top)
