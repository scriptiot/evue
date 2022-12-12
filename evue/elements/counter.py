# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from flet import (
    Draggable,
    alignment
)
from .widgets import Counter
from .widgets import BaseContainer


class CounterElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._counter_ = Counter()
        self._text_ = self._counter_.text_number
        self.minusIconButton = self._counter_.minusIconButton
        self.addIconButton = self._counter_.addIconButton
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._counter_),
                alignment=alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = self._counter_
        
        def on_change(value):
            self.value = int(value)

        self._counter_.on_change = on_change

    def set_width(self, value):
        self._counter_.set_width(value) 

    def set_border_width(self, value):
        self._counter_.set_border_width(value)

    def set_border_radius(self, value):
        self._counter_.set_border_radius(value)

    def set_border_color(self, value):
        self._counter_.set_border_color(value)

    def set_font_size(self, value):
        self._counter_.set_font_size(value)

    def set_color(self, value):
        self._counter_.set_color(value)

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

    def set_value(self, value):
        self._counter_.set_value(int(value))
    
    def set_onValueChanged(self, func):
        def on_change(value):
            self.value = value
            func(self)
        self._counter_.on_change = on_change

    @classmethod
    def default_events(cls, id):
        ret = FletBaseElement.default_events(id)
        ret['onValueChanged'] = {
            "code": "pass",
            "name": "on_%s_valueChanged" % id
        }
        return ret

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "value": self.value
        })
        return attributes

    @property
    def style(self):
        style = super().style
        style.update({
            "color": self.color,
            "font-size": self.font_size,
            "text-align": self.text_align
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
            "width": 190,
            "height": 40,
            "border-width": 1,
            "border-radius": 0,
            "border-color": "white",
            "background-color": "transparent",
            "color": "white",
            "font-size": 14,
            "text-align": "center"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "value": 0,
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "counter", left, top)
