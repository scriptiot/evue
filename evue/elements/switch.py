# -*- coding: utf-8 -*-
from flet import (
    Draggable,
    Switch,
    Row,
    Text,
    alignment,
)
from .fletbaseelement import FletBaseElement
from .text import TextElement
from .widgets import BaseContainer


class SwitchElement(TextElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)

    def create(self, parent, draggable=False):
        self._switch_ = Switch()
        self._text_ = Text(expand=True)
        self._row_ = Row([self._switch_, self._text_], expand=True)
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._row_),
                alignment=alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(self._row_, alignment=alignment.center)

    def set_width(self, value):
        self._obj_.width = value

    def set_height(self, value):
        self._obj_.height = value

    def set_text(self, value):
        width, height = self.measureText(value, self._text_.size)
        if width is not None and width > self.width:
            self.width = width + 72
        if height is not None and height > self.height:
            self.height = height
        self._text_.value = value

    def set_value(self, value):
        self._switch_.value = FletBaseElement.bool(value)

    def set_disabled(self, value):
        self._switch_.disabled = FletBaseElement.bool(value)

    def set_switch_indic_color(self, value):
        self._switch_.track_color = value

    def set_switch_knob_color(self, value):
        self._switch_.thumb_color = value

    def set_onValueChanged(self, func):
        def on_change(e):
            self.value = e.control.value
            func(self)
        self._switch_.on_change = on_change

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
            "text": self._text_.value,
            "value": self._switch_.value
        })
        return attributes

    @property
    def style(self):
        ret = super().style
        ret.update({
            "switch-indic-color": self._switch_.track_color,
            "switch-knob-color": self._switch_.thumb_color
        })
        return ret

    def set_attributes(self, node):
        super().set_attributes(node)
        style = node['attributes']['style']
        if 'switch-indic-color' in style:
            self.switch_indic_color = style['switch-indic-color']
        if 'switch-knob-color' in style:
            self.switch_knob_color = style['switch-knob-color']
        # attr
        attributes = node['attributes']
        if "text" in attributes:
            self.text = attributes["text"]
        if "value" in attributes:
            self.value = attributes["value"]

    def set_tiny_attributes(self, attributes):
        style = attributes['style']
        self.font_size = style['font-size']
        self.color = style['color']
        self.text_align = style['text-align']
        if 'checkbox-checked-color' in style:
            self.switch_indic_color = style['switch-indic-color']
        if 'switch-knob-color' in style:
            self.switch_knob_color = style['switch-knob-color']
        # attr
        if "text" in attributes:
            self.text = attributes["text"]
        if "value" in attributes:
            self.value = attributes["value"]

    @classmethod
    def defaut_style(cls):
        return {
            "width": 64,
            "height": 32,
            "border-width": 0,
            "border-color": "transparent",
            "background-color": "#282828",
            "color": "white",
            "font-size": 20,
            "text-align": "left",
            "switch-indic-color": "green",
            "switch-knob-color": "red"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "text": "switch",
            "value": True,
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "switch", left, top)
