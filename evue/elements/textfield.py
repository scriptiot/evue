# -*- coding: utf-8 -*-
from sre_parse import expand_template
from flet import (
    Stack,
    Draggable,
    TextField,
    alignment,
    Control,
    TextStyle
)
from flet_core.textfield import KeyboardTypeString
from loguru import logger
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer
from ..globalthis import globalThis


class TextFieldElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._text_ = TextField(content_padding=0)
        self._text_.multiline = False
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._text_),
                alignment=alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(self._text_, alignment=alignment.center)
            self._text_.border_width = 0

        def on_change(e):
            self.value = e.control.value

        self._text_.on_change = on_change

    def set_width(self, value):
        self._obj_.width = value
        self._text_.width = value

    def set_height(self, value):
        self._obj_.height = value
        self._text_.height = value
    
    def set_border(self, value):
        if isinstance(value, str):
            self._text_.border = value
        else:
            return super().set_border(value)
    
    def set_label(self, value):
        self._text_.label = value
    
    def set_password(self, value):
        self._text_.password = FletBaseElement.bool(value)

    def set_can_reveal_password(self, value):
        self._text_.can_reveal_password = FletBaseElement.bool(value)

    def set_font_size(self, value):
        self._text_.text_size = value

    def set_color(self, value):
        self._text_.color = value

    def set_text_align(self, value):
        if value == "None":
            self._text_.text_align = "center"
        else:
            self._text_.text_align = value

    def set_value(self, value):
        self._text_.value = value
    
    def set_keyboard_type(self, value:KeyboardTypeString):
        self._text_.keyboard_type = value

    def set_multiline(self, value:bool):
        self._text_.multiline = value
    
    def set_min_lines(self, value:int):
        self._text_.min_lines = value
    
    def set_max_lines(self, value:int):
        self._text_.max_lines = value
    
    def set_max_length(self, value:int):
        self._text_.max_length = value

    def set_tooltip(self, value):
        self._text_.tooltip = value
    
    def set_read_only(self, value):
        self._text_.read_only = FletBaseElement.bool(value)
    
    def set_icon(self, value):
        self._text_.icon = FletBaseElement.ficon(value)

    def set_focused_color(self, value):
        self._text_.focused_color = value
    
    def set_focused_bgcolor(self, value):
        self._text_.focused_bgcolor = value
    
    def set_focused_border_width(self, value):
        self._text_.focused_border_width = value
    
    def set_focused_border_color(self, value):
        self._text_.focused_border_color = value
    
    def set_content_padding(self, value):
        self._text_.content_padding = value 
    
    def set_filled(self, value):
        self._text_.filled = value
    
    def set_place_holder(self, value:str):
        self._text_.hint_text = value

    def set_hint_text(self, value:str):
        self._text_.hint_text = value
    
    def set_hint_style(self, value:TextStyle):
        self._text_.hint_style = value
    
    def set_helper_text(self, value:str):
        self._text_.helper_text = value
    
    def set_helper_style(self, value:TextStyle):
        self._text_.helper_style = value
    
    def set_counter_text(self, value:str):
        self._text_.counter_text = value
    
    def set_counter_style(self, value:TextStyle):
        self._text_.counter_style = value

    def set_error_text(self, value:str):
        self._text_.error_text = value
    
    def set_error_style(self, value:TextStyle):
        self._text_.error_style = value
    
    def set_prefix(self, value:Control):
        self._text_.prefix = value

    def set_prefix_icon(self, value):
        self._text_.prefix_icon = FletBaseElement.ficon(value)
    
    def set_prefix_text(self, value):
        self._text_.prefix_text = value
    
    def set_prefix_style(self, value):
        self._text_.prefix_style = value
    
    def set_suffix(self, value:Control):
        self._text_.suffix = value

    def set_suffix_icon(self, value):
        self._text_.suffix_icon = FletBaseElement.ficon(value)

    def set_suffix_text(self, value):
        self._text_.suffix_text = value
    
    def set_suffix_style(self, value):
        self._text_.suffix_style = value

    def set_onValueChanged(self, func):
        def on_change(e):
            if self.value != e.control.value:
                self.value = e.control.value
                func(self)
        self._text_.on_change = on_change

    def set_attributes(self, node):
        super().set_attributes(node)
        style = node["attributes"]['style']
        self.font_size = style['font-size']
        self.color = style['color']
        self.text_align = style['text-align']
        # attr
        attributes = node['attributes']
        self.value = attributes["value"]

    def set_tiny_attributes(self, data):
        style = data['style']
        self.font_size = style['font-size']
        self.color = style['color']
        self.text_align = style['text-align']
        # attr
        self.value = data["value"]

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "value": self._text_.value
        })
        return attributes

    @property
    def style(self):
        style = super().style
        style.update({
            "color": self._text_.color,
            "font-size": self._text_.text_size,
            "text-align": FletBaseElement.textAlign(self._text_.text_align)
        })
        return style
    
    @classmethod
    def defaut_style(cls):
        return {
            "width": 200,
            "height": 40,
            "border-width": 0,
            "border-color": "transparent",
            "background-color": "#282828",
            "color": "white",
            "font-size": 14,
            "text-align": "center"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "value": "textfiled",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "textfield", left, top)
