# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from flet import (
    Draggable,
    alignment
)
from .widgets import Collapsible
from .widgets import BaseContainer
from threading import Timer


class CollapsibleElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)
        self._timer = None

    def create(self, parent, draggable=False):
        self._collapsible_ = Collapsible()
        self._collapsible_.scroll = "adaptive"
        self._text_ = self._collapsible_._text_
        self._controls_ = self._collapsible_.content.controls
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._collapsible_),
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(
                self._collapsible_
            )
    
    def toggle(self, timeout=1):
        if self._timer is None:
            self._timer = Timer(timeout, self._collapsible_.header_click)
            if self._timer:
                self._timer.start()
        else:
            self._timer.cancel()
            self._timer = None

    @property
    def isContainer(self):
        return True
    
    def set_open(self, value):
        self._collapsible_.set_open(FletBaseElement.bool(value))

    def set_width(self, value):
        self._obj_.width = value
        self._collapsible_.width = value

    def set_height(self, value):
        self._obj_.height = value
        self._collapsible_.height = value

    def set_title(self, value):
        self._text_.value = str(value)
    
    def set_spacing(self, value):
        self._collapsible_.spacingContainer.height = value

    def set_font_size(self, value):
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

    def set_value(self, value):
        self._text_.value = str(value)
    
    def set_switch(self, value):
        if value == "true":
            self._collapsible_.set_switch(True)
        else:
            self._collapsible_.set_switch(False)
