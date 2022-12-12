# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from flet import (
    Draggable,
    alignment,
    Markdown,
    TextStyle
)
from .widgets import BaseContainer
from loguru import logger


class MarkdownElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._markdown_ = Markdown(
            selectable=True,
            extension_set="gitHubWeb",
            code_theme="atom-one-dark",
            code_style=TextStyle(font_family="Roboto Mono"),
            on_tap_link=lambda e: self.page.launch_url(e.data),
        )
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._markdown_), 
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(
                self._markdown_,
                alignment = alignment.top_left,
                expand=True
            )

    def set_width(self, value):
        self._obj_.width = value
        self._markdown_.width = value

    def set_height(self, value):
        self._obj_.height = value
        self._markdown_.height = value

    def set_content(self, value):
        self._markdown_.value = value

    def set_selectable(self, value):
        self._markdown_.selectable = FletBaseElement.bool(value)

    def set_code_theme(self, value):
        self._markdown_.code_theme = value

    def set_code_style(self, value):
        self._markdown_.code_theme = TextStyle(font_family="Roboto Mono")

    def set_extension_set(self, value):
        self._markdown_.extension_set = value

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "content": self._markdown_.value,
            "selectable": self._markdown_.selectable,
            "code_theme": self._markdown_.code_theme,
            "extension_set": self._markdown_.extension_set
        })
        return attributes

    @property
    def style(self):
        style = super().style
        style.update({
            "color": self.color,
            "font-size": self.font_size,
            "text-align": self.text_align
        })
        return style

    def set_attributes(self, node):
        super().set_attributes(node)
        # attr
        attributes = node['attributes']
        self.content = attributes["content"]
        self.selectable = attributes["selectable"]
        self.code_theme = attributes["code_theme"]
        self.extension_set = attributes["extension_set"]

    def set_attributes(self, node):
        super().set_attributes(node)
        style = node["attributes"]['style']
        self.font_size = style['font-size']
        self.color = style['color']
        self.text_align = style['text-align']
        # attr
        attributes = node['attributes']
        self.content = attributes["content"]
        self.selectable = attributes["selectable"]
        self.code_theme = attributes["code_theme"]
        self.extension_set = attributes["extension_set"]

    def set_tiny_attributes(self, attributes):
        style = attributes['style']
        self.font_size = style['font-size']
        self.color = style['color']
        self.text_align = style['text-align']
        # attr
        self.content = attributes["content"]
        self.selectable = attributes["selectable"]
        self.code_theme = attributes["code_theme"]
        self.extension_set = attributes["extension_set"]

    @classmethod
    def defaut_style(cls):
        return {
            "left": 0,
            "top": 0,
            "border-width": 0,
            "border-color": "#282828",
            "background-color": "#282828",
            "color": "white",
            "font-size": 20,
            "text-align": "center"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "content": "#1111",
            "selectable": True,
            "code_theme": "atom-one-dark",
            "extension_set": "gitHubWeb",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "markdown", left, top)
