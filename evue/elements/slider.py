# -*- coding: utf-8 -*-
from flet import (
    Slider,
    Container,
    DragUpdateEvent,
    GestureDetector,
    MouseCursor,
    Page,
    Stack,
    colors,
    alignment,
    ContainerTapEvent
)

from ..debounce import debounce
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer
from loguru import logger
import traceback


class SliderElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self['value'] = 0
        self['min'] = 0
        self['max'] = 100
        self['step'] = 10
        self['label'] = "{value}"
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._knob_ = BaseContainer()
        self._knob_.border_radius = 10000
        
        self._active_ = BaseContainer()
        self._active_.left = 5
        self._inactive_ = BaseContainer()

        def on_pan_update2(e: DragUpdateEvent):
            if self._gd_.left <= (self._obj_.width - self._knob_.width - e.delta_x):
                self._gd_.left = max(0, self._gd_.left + e.delta_x)
                self._gd_.update()
                self.updateSlider()
                self.value = 100 * self._gd_.left / (self._obj_.width - self._knob_.width)

        self._gd_ = GestureDetector(
            drag_interval=10,
            on_pan_update=on_pan_update2,
            left=0,
            top=0,
            content=Container(Stack([self._knob_])),
        )

        self._slider_ = Slider(label="{value}", divisions= 100)
        self._obj_ = BaseContainer(Stack([self._active_, self._inactive_, self._gd_]), alignment=alignment.center)

        def on_click(e:ContainerTapEvent):
            self.updateSliderByValue(100 * e.local_x / self._obj_.width)
            self.update()

        self._obj_.on_click = on_click
        
    def updateSlider(self):
        self._active_.left = 5
        self._active_.width = self._gd_.left + self._knob_.width / 2
        self._inactive_.left = self._active_.width
        self._inactive_.width = self._obj_.width - self._inactive_.left - 5

    def updateSliderByValue(self, value):
        try:
            self._gd_.left = min(self._obj_.width * value / 100, self._obj_.width - self._knob_.width)
            self.updateSlider()
        except:
            pass

    def set_width(self, value):
        self._obj_.width = value
        self.updateSliderByValue(self['value'])

    def set_height(self, value):
        value = value + 10
        
        self._obj_.height = value

        self._active_.top = 5
        self._active_.height = value - self._active_.top * 2
        
        self._inactive_.top = 5
        self._inactive_.height = value - self._inactive_.top * 2
        
        
        self._knob_.height = value 
        self._knob_.width = value
        
        self.updateSliderByValue(self['value'])

    def set_min(self, value):
        self['min'] = value

    def set_max(self, value):
        self['max'] = value

    def set_value(self, value):
        self['value'] = value
        if 'onValueChanged' in self and self['onValueChanged']:
            self['onValueChanged'](value)

    def set_divisions(self, value):
        self._slider_.divisions = value

    def set_label(self, value):
        self._slider_.label = "{value}"
    
    def set_slider_indic_color(self, value):
        self._active_.bgcolor = value
    
    def set_slider_knob_color(self, value):
        self._knob_.bgcolor = value

    def set_background_color(self, value):
        self._inactive_.bgcolor = value

    def set_border_radius(self, value):
        self._active_.border_radius = value
        self._inactive_.border_radius = value

    def set_onValueChanged(self, func):
        self['onValueChanged'] = func

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
            "min": self['min'],
            "max": self['max'],
            "value": int(self['value']),
        })
        return attributes

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        style = attributes['style']
        self.background_color = style['background-color']
        self.slider_indic_color = style['slider-indic-color']
        self.slider_knob_color = style['slider-knob-color']
        # attr
        self.min = attributes["min"]
        self.max = attributes["max"]
        self.value = attributes["value"]
        self.divisions = attributes["divisions"]
        self.updateSliderByValue(self['value'])

    def set_tiny_attributes(self, data):
        style = data['style']
        self.slider_indic_color = style['slider-indic-color']
        self.slider_knob_color = style['slider-knob-color']
        # attr
        self.percent = data["min"]
        self.max = data["max"]
        self.value = data["value"]
        self.divisions = data["divisions"]

    @classmethod
    def defaut_style(cls):
        return {
            "width": 200,
            "height": 32,
            "border-width": 0,
            "border-radius": 100,
            "border-color": "transparent",
            "background-color": "#808080",
            "slider-indic-color": "#ff0000",
            "slider-knob-color": "yellow"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "min": 0,
            "max": 100,
            "value": 70,
            "divisions": 100,
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "slider", left, top)
