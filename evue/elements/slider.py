# -*- coding: utf-8 -*-
from flet import (
    Draggable,
    Slider,
    alignment
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer


class SliderElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self['min'] = 0
        self['max'] = 100
        self['step'] = 10
        self['label'] = "{value}"
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._slider_ = Slider(label="{value}", divisions= 100)
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._slider_),
                alignment=alignment.center_left
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(self._slider_, alignment=alignment.center_left)

    def set_width(self, value):
        self._obj_.width = value
        self._slider_.width = value

    def set_height(self, value):
        self._obj_.height = value
        self._slider_.height = value

    def set_min(self, value):
        self._slider_.min = value

    def set_max(self, value):
        self._slider_.max = value
    
    def set_value(self, value):
        self._slider_.value = float(value)

    def set_divisions(self, value):
        self._slider_.divisions = value

    def set_label(self, value):
        self._slider_.label = "{value}"
    
    def set_slider_indic_color(self, value):
        pass
    
    def set_slider_knob_color(self, value):
        pass
    
    def set_onValueChanged(self, func):
        def on_change(e):
            self.value = e.control.value
            func(self)
        self._slider_.on_change = on_change

    @classmethod
    def default_events(cls, id):
        ret = FletBaseElement.default_events(id)
        ret['onValueChanged'] = {
            "code": "pass",
            "name": "on_%s_valueChanged" % id
        }
        return ret

    @property
    def style(self):
        ret = super().style
        ret.update({
            "slider-indic-color": self['slider_indic_color'],
            "slider-knob-color": self['slider_knob_color']
        })
        return ret

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "min": self._slider_.min,
            "max": self._slider_.max,
            "value": int(self._slider_.value),
            "divisions": self._slider_.divisions,
            "label": self._slider_.label
        })
        return attributes

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        style = attributes['style']
        self.slider_indic_color = style['slider-indic-color']
        self.slider_knob_color = style['slider-knob-color']
        # attr
        self.min = attributes["min"]
        self.max = attributes["max"]
        self.value = attributes["value"]
        self.divisions = attributes["divisions"]
        self.label = attributes["label"]

    def set_tiny_attributes(self, data):
        style = data['style']
        self.slider_indic_color = style['slider-indic-color']
        self.slider_knob_color = style['slider-knob-color']
        # attr
        self.percent = data["min"]
        self.max = data["max"]
        self.value = data["value"]
        self.divisions = data["divisions"]
        self.label = data["label"]

    @classmethod
    def defaut_style(cls):
        return {
            "width": 200,
            "height": 32,
            "border-width": 0,
            "border-radius": 100,
            "border-color": "transparent",
            "background-color": "transparent",
            "slider-indic-color": "red",
            "slider-knob-color": "yellow"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "min": 0,
            "max": 100,
            "value": 70,
            "divisions": 100,
            "label": "{value}",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "slider", left, top)
