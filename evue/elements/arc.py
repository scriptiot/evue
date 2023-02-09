# -*- coding: utf-8 -*-
from flet import (
    Draggable,
    ProgressRing,
    alignment,
    Stack
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer
import math


class ArcElement(FletBaseElement):

    startRotateAngle = 2 * math.pi * 90 / 360
    
    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self['rotation'] = 0
        self['arc_indic_width'] = 10
        self['arc_indic_color'] = "#ff0000"
        self['arc_bg_width'] = 10
        self['arc_bg_color'] = "transparent"
        self['bg_start_angle'] = 0
        self['bg_end_angle'] = 360
        self['start_angle'] = 0
        self['end_angle'] = 0
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._arc_ = ProgressRing(rotate=self['rotation'])
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._arc_),
                alignment=alignment.center_left
            )
            self._obj_.content.element = self
        else:
            self._bg_ = ProgressRing(rotate=self['rotation'])
            self._obj_ = BaseContainer(Stack([self._bg_, self._arc_]), alignment=alignment.center)

    def set_width(self, value):
        self._obj_.width = value
        self._arc_.width = value
        self._bg_.width = value

    def set_height(self, value):
        self._obj_.height = value
        self._arc_.height = value
        self._bg_.height = value

    def set_value(self, value):
        self._arc_.value = float(int(value) / 100)
        self._bg_.value = 1

    def set_rotation(self, value):
        self['rotation'] = value
        self._arc_.rotate = 2 * math.pi * (90 + value) / 360 

    def set_arc_indic_width(self, value):
        if isinstance(value, str):
            if value.endswith("px"):
                value = int(value[0:-2])
            else:
                value = value
        self._arc_.stroke_width = value
        self['arc_indic_width'] = "%spx" % value

    def set_arc_indic_color(self, value):
        self._arc_.color = value
    
    def set_arc_bg_color(self, value):
        self._bg_.color = value
        self['arc_bg_color'] = value

    def set_arc_bg_width(self, value):
        if isinstance(value, str):
            if value.endswith("px"):
                value = int(value[0:-2])
            else:
                value = value
        self._bg_.stroke_width = value
        self['arc_bg_width'] = "%spx" % value

    def set_bg_start_angle(self, value):
        self['bg_start_angle'] = value

    def set_bg_end_angle(self, value):
        self['bg_end_angle'] = value

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
            "arc-indic-width": self['arc_indic_width'],
            "arc-indic-color": self['arc_indic_color'],
            "arc-bg-width": self['arc_bg_width'],
            "arc-bg-color": self['arc_bg_color']
        })
        return ret

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "start-angle": self['start_angle'],
            "rotation": self['rotation'],
            "end-angle": self['end_angle'],
            "bg-start-angle": self['bg_start_angle'],
            "bg-end-angle": self['bg_end_angle'],
            "start-angle": self['start_angle'],
            "end-angle": self['end_angle'],
            "value": int(self._arc_.value * 100),
        })
        return attributes

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        style = attributes['style']
        self.arc_indic_color = style['arc-indic-color']
        self.arc_indic_width = style['arc-indic-width']
        self.arc_bg_color = style['arc-bg-color']
        self.arc_bg_width = style['arc-bg-width']
        # attr
        self.rotation = attributes["rotation"]
        self.value = int(attributes["value"])

    def set_tiny_attributes(self, data):
        style = data['style']
        self.arc_indic_color = style['arc-indic-color']
        self.arc_indic_width = style['arc-indic-width']
        self.arc_bg_color = style['arc-bg-color']
        self.arc_bg_width = style['arc-bg-width']
        # attr
        self.rotation = data["rotation"]
        self.value = int(data["value"])

    @classmethod
    def defaut_style(cls):
        return {
            "width": 140,
            "height": 140,
            "border-width": 0,
            "border-radius": 0,
            "border-color": "transparent",
            "background-color": "transparent",
            "arc-indic-color": "#ff0000",
            "arc-indic-width": "10px",
            'arc-bg-width': "0px",
            'arc-bg-color': 'transparent',
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "value": 83,
            "rotation": 120,
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "arc", left, top)
