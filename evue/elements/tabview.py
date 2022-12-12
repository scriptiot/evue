# -*- coding: utf-8 -*-
from flet import (
    Draggable,
    alignment,
    Tabs
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer


class TabViewElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._tabview_ = Tabs(expand=True)
        self._controls_ = self._tabview_.tabs
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._tabview_), 
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(
                self._tabview_
            )
        
        def onValueChanged(e):
            pass
        
        self.onValueChanged = onValueChanged

    @property
    def isContainer(self):
        return True

    @property
    def isLayout(self):
        return False

    def set_expand(self, value):
        self.obj.expend = FletBaseElement.bool(value)
        self._tabview_.expend = FletBaseElement.bool(value)

    def set_currentIndex(self, value):
        self._tabview_.selected_index = value
    
    def set_animation_duration(self, value):
        self._tabview_.animation_duration = value

    def set_onValueChanged(self, func):
        def on_change(e):
            index = e.control.selected_index
            self.currentIndex = index
            func(self)
        self._tabview_.on_change = on_change
    
    
    @classmethod
    def default_events(cls, id):
        ret = FletBaseElement.default_events(id)
        ret['onValueChanged'] = {
            "code": "pass",
            "name": "on_%s_valueChanged" % id
        }
        return ret

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        style = attributes['style']
        # attr
        self.expand = attributes["expand"]
        self.currentIndex = attributes["currentIndex"]
        self.animation_duration = attributes["animation_duration"]

    def set_tiny_attributes(self, attributes):
        # attr
        self.expand = attributes["expand"]
        self.currentIndex = attributes["currentIndex"]
        self.animation_duration = attributes["animation_duration"]

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "expand": self._tabview_.expand,
            "currentIndex": self._tabview_.selected_index,
            "animation_duration": self._tabview_.animation_duration,
        })
        return attributes

    @classmethod
    def defaut_style(cls):
        return {
            "left": 0,
            "top": 0,
            "width": 400,
            "height": 400,
            "border-width": 0,
            "border-radius": 0,
            "border-color": "transparent",
            "background-color": "white"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "expand": True,
            "currentIndex": 0,
            "animation_duration": 300,
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "tabview", left, top)
