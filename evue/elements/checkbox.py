# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from flet import (
    Checkbox,
    Row,
    Text,
    alignment,
    Draggable
)

from .text import TextElement
from .widgets import BaseContainer
from loguru import logger


class CheckboxElement(TextElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)

    def create(self, parent, draggable=False):
        self._checkbox_ = Checkbox()
        self._text_ = Text(expand=True)
        self._row_ = Row([self._checkbox_, self._text_], expand=True)
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._row_),
                alignment=alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(self._row_, alignment=alignment.center)

        def on_change(e):
            self.value = e.control.value
            logger.warning(self.value)
        self._checkbox_.on_change = on_change

    def set_width(self, value):
        self._obj_.width = value

    def set_height(self, value):
        self._obj_.height = value
    
    def set_value(self, value):
        self._checkbox_.value = FletBaseElement.bool(value)

    def set_text(self, value):
        width, height = self.measureText(value, self._text_.size)
        if width is not None and width > self.width:
            self.width = width + 48
        if height is not None and height > self.height:
            self.height = height
        self._text_.value = value

    def set_disabled(self, value):
        self._checkbox_.disabled = FletBaseElement.bool(value)
    
    def set_checkbox_checked_color(self, value):
        self._checkbox_.check_color = value
        
    def set_checkbox_unchecked_color(self, value):
        self._checkbox_.fill_color = value

    def set_onValueChanged(self, func):
        def on_change(e):
            self.value = e.control.value
            logger.warning(self.value)
            func(self)
        self._checkbox_.on_change = on_change

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
            "value": self._checkbox_.value
        })
        return attributes

    @property
    def style(self):
        ret = super().style
        ret.update({
            "checkbox-checked-color": self._checkbox_.check_color,
            "checkbox-unchecked-color": self._checkbox_.fill_color
        })
        return ret

    def set_attributes(self, node):
        super().set_attributes(node)
        style = node['attributes']['style']
        if 'checkbox-checked-color' in style:
            self.checkbox_checked_color = style['checkbox-checked-color']
        if 'checkbox-unchecked-color' in style:
            self.checkbox_unchecked_color = style['checkbox-unchecked-color']
        # attr
        attributes = node['attributes']
        self.text = attributes["text"]
        self.value = attributes["value"]

    def set_tiny_attributes(self, data):
        style = data['style']
        self.font_size = style['font-size']
        self.color = style['color']
        self.text_align = style['text-align']
        if 'checkbox-checked-color' in style:
            self.checkbox_checked_color = style['checkbox-checked-color']
        if 'checkbox-unchecked-color' in style:
            self.checkbox_unchecked_color = style['checkbox-unchecked-color']

        # attr
        if 'value' in data:
            self.value = data["value"]
        if 'text' in data:
            self.text = data["text"]

    @classmethod
    def defaut_style(cls):
        return {
            "width": 42,
            "height": 42,
            "border-width": 0,
            "border-color": "transparent",
            "background-color": "#282828",
            "color": "white",
            "font-size": 20,
            "text-align": "left",
            "checkbox-checked-color": "green",
            "checkbox-unchecked-color": "red"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "text": "checkbox",
            "value": True,
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "checkbox", left, top)
