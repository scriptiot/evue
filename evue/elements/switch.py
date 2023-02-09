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
from loguru import logger
from ..debounce import debounce


class SwitchElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self['value'] = False
        self['switch-indic-color'] = "#01a2b1"
        self['switch-knob-color'] = '#ffffff'
        self.create(parent, draggable)
        self.setParent(parent)
        self.events = self.default_events(self.id)

    def create(self, parent, draggable=False):
        self._switch_ = BaseContainer()
        self._switch_.border_radius = 1000
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._row_),
                alignment=alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(self._switch_, alignment=alignment.center_left)

        def onValueChanged(value):
            pass
        
        self.onValueChanged = onValueChanged

    def set_width(self, value):
        self._obj_.width = value

    def set_height(self, value):
        self._obj_.height = value
        self.border_radius = value
        self._switch_.width = value
        self._switch_.height = value

    def set_border_radius(self, value):
        self._obj_.border_radius = value

    def set_value(self, value):
        flag = FletBaseElement.bool(value)
        if flag:
            self._obj_.alignment = alignment.center_right
            self._obj_.bgcolor = self['switch-indic-color']
        else:
            self._obj_.alignment = alignment.center_left
            self._obj_.bgcolor = self.background_color

    def set_disabled(self, value):
        self._obj_.disabled = FletBaseElement.bool(value)

    def set_switch_indic_color(self, value):
        if self['value']:
            self._obj_.bgcolor = value
        self['switch-indic-color']  = value

    def set_switch_knob_color(self, value):
        self._switch_.bgcolor = value
        self['switch_knob_color']  = value

    @debounce(0.01)
    def handle_callback(self, func):
        self.value = not self['value']
        func(self)

    def set_onValueChanged(self, func):
        def on_click(e):
            self.handle_callback(func)
        self._obj_.on_click = on_click

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
        ret = super().style
        ret.update({
            "switch-indic-color": self['switch-indic-color'],
            "switch-knob-color": self['switch-knob-color']
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
        if "value" in attributes:
            self.value = attributes["value"]

    def set_tiny_attributes(self, attributes):
        style = attributes['style']
        if 'switch-indic-color' in style:
            self.switch_indic_color = style['switch-indic-color']
        if 'switch-knob-color' in style:
            self.switch_knob_color = style['switch-knob-color']
        # attr
        if "value" in attributes:
            self.value = attributes["value"]

    @classmethod
    def defaut_style(cls):
        return {
            "width": 64,
            "height": 32,
            "border-width": 0,
            "border-radius": 32,
            "border-color": "transparent",
            "background-color": "#808080",
            "switch-indic-color": "#01a2b1",
            "switch-knob-color": "#ffffff"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "value": False,
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "switch", left, top)
