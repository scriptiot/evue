# -*- coding: utf-8 -*-
from flet import (
    Draggable,
    alignment,
    border_radius
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer


class ProgressElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)
        self['percent'] = 0

    def create(self, parent, draggable=False):
        self._progressbar_ = BaseContainer()
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._progressbar_),
                alignment=alignment.center_left
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(self._progressbar_, alignment=alignment.center_left)

    def set_width(self, value):
        self._obj_.width = float(value)
        self._progressbar_.width = self._obj_.width  * (float(self['percent']) / 100)

    def set_height(self, value):
        self._obj_.height = value
        self._progressbar_.height = value

    def set_border_radius(self, value):
        self.obj.border_radius = border_radius.all(value)
        self._progressbar_.border_radius = border_radius.all(value)

    def set_value(self, value):
        self.set_percent(value)

    def set_percent(self, value):
        if self._obj_.width:
            self._progressbar_.width = self._obj_.width  * (value / 100)

    def set_background_color(self, value):
        self._obj_.bgcolor = value

    def set_progress_indic_color(self, value):
        self._progressbar_.bgcolor = value

    @property
    def style(self):
        ret = super().style
        ret.update({
            "progress-indic-color": self._progressbar_.bgcolor
        })
        return ret

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "percent": self['percent']
        })
        return attributes

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        style = attributes['style']
        self.progress_indic_color = style['progress-indic-color']
        # attr
        self.percent = attributes["percent"]

    def set_tiny_attributes(self, data):
        style = data['style']
        self.progress_indic_color = style['progress-indic-color']
        # attr
        self.percent = data["percent"]

    @classmethod
    def defaut_style(cls):
        return {
            "width": 200,
            "height": 32,
            "border-width": 0,
            "border-radius": 100,
            "border-color": "transparent",
            "background-color": "white",
            "progress-indic-color": "green",
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "percent": 30,
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "progress", left, top)
