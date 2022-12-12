# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from flet import (
    Draggable,
    Dropdown,
    dropdown,
    alignment,
)

from .widgets import BaseContainer
from loguru import logger


class ComboboxElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._dropdown_ = Dropdown(content_padding=5, expand=True)
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._dropdown_),
                alignment=alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(self._dropdown_, alignment=alignment.center)

        def on_change(e):
            self.value = e.control.value

        self._dropdown_.on_change = on_change

    def set_width(self, value):
        self._obj_.width = value

    def set_height(self, value):
        self._obj_.height = value

    def set_border_width(self, value):
        self._obj_.border_width = value
        self._dropdown_.border_width = value

    def set_border_radius(self, value):
        self._obj_.border_radius = value
        self._dropdown_.border_radius = value

    def set_border_color(self, value):
        self._obj_.border_color = value
        self._dropdown_.border_color = value

    def set_color(self, value):
        self._dropdown_.color = value

    def set_font_size(self, value):
        if value == "None":
            self._dropdown_.text_size = 20
        else:
            self._dropdown_.text_size = int(value)

    def set_padding(self, value):
        self._dropdown_.content_padding = int(value)

    def set_options(self, value):
        options = [dropdown.Option(item) for item in value]
        self._dropdown_.options = options

    def set_value(self, value):
        self._dropdown_.value = value

    def set_disabled(self, value):
        self._dropdown_.disabled = FletBaseElement.bool(value)

    def set_onValueChanged(self, func):
        def on_change(e):
            self.value = e.control.value
            func(self)
        self._dropdown_.on_change = on_change

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
            "options": self.options,
            "value": self._dropdown_.value
        })
        return attributes

    def set_attributes(self, node):
        super().set_attributes(node)
        style = node["attributes"]['style']
        self.font_size = style['font-size']
        self.padding = style['padding']
        if 'color' in style:
            self.color = style['color']
        # attr
        attributes = node['attributes']
        self.options = attributes["options"]
        self.value = attributes["value"]

    def set_tiny_attributes(self, data):
        style = data['style']
        self.font_size = style['font-size']
        self.color = style['color']
        # attr
        self.options = data["options"]
        self.value = data["value"]

    @classmethod
    def defaut_style(cls):
        return {
            "width": 120,
            "height": 42,
            "padding": 2,
            "border-width": 0,
            "border-radius": 5,
            "border-color": "transparent",
            "background-color": "white",
            "font-size": 20,
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "options": ['a', 'b', 'c'],
            "value": 'a',
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "combobox", left, top)
