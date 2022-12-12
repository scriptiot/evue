# -*- coding: utf-8 -*-
from flet import (
    alignment
)
from .fletbaseelement import FletBaseElement
from .textfield import TextFieldElement


class TextareaElement(TextFieldElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self._text_.multiline = True
        self._text_.filled = True
        self._text_.expand = True
        self._obj_.set_padding(5)
        self._obj_.alignment = alignment.top_left

    def set_width(self, value):
        self._obj_.width = value
        self._text_.width = value

    def set_height(self, value):
        self._obj_.height = value
        self._text_.height = value
    
    def set_font_size(self, value):
        self._text_.text_size = value

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
            "text-align": self._text_.text_align
        })
        return style
    
    @classmethod
    def defaut_style(cls):
        return {
            "width": 240,
            "height": 160,
            "border-width": 0,
            "border-color": "transparent",
            "background-color": "#282828",
            "color": "white",
            "font-size": 16,
            "text-align": "left"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "value": "Evue是面向iot的小程序应用框架, 开箱即用, 超轻量、原生支持MVVM, 丰富的组件和完整支持HTML5 Canvas 2D接口, 纯C开发, 跨平台, 一次适配, 多端运行!",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "textarea", left, top)
