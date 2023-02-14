# -*- coding: utf-8 -*-
import os
from flet import (
    Draggable,
    Image,
    Stack,
    alignment
)
from .fletbaseelement import FletBaseElement
from PIL import Image as PILImage
from .widgets import BaseContainer
from loguru import logger
from ..globalthis import globalThis
import traceback


def getSize(src):
    if src.endswith(".svg"):
        with open(src, "r", encoding="utf-8") as f:
            content = f.read()

        def getValue(key):
            wIndex = content.index("%s=" % key)
            i = wIndex
            while content[i:i+4] != "px\" ":
                i += 1
            value = int(content[wIndex+len(key)+2:i])
            return value

        width = getValue("width")
        height = getValue("height")
    else:
        path = src
        img = PILImage.open(path)
        size = img.size
        width = size[0]
        height = size[1]
    return width, height

class ImageElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._image_ = Image(gapless_playback=True)
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._image_),
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(
                self._image_,
                alignment = alignment.center
            )
    @property
    def isContainer(self):
        return False

    @property
    def isLayout(self):
        return False

    def set_width(self, value):
        self._obj_.width = value
        self._image_.width = value

    def set_height(self, value):
        self._obj_.height = value
        self._image_.height = value
    
    def set_tooltip(self, value):
        self._image_.tooltip = value

    def set_src(self, value):
        if value in self.resources:
            logger.warning(value)
            self.src_base64 = self.resources[value]
            return

        if value.startswith("http"):
            self._obj_.image_src = f"%s" % value
        else:
            if globalThis.isWeb():
                value = "http://%s:%d/%s" % (globalThis.server_ip, globalThis.port, value)
            elif "</svg>" in value:
                self._image_.src = f"%s" % value
            else:
                try:
                    size = getSize(value)
                    self.width = size[0]
                    self.height = size[1]
                except:
                    logger.error(traceback.format_exc())
            self._image_.src = f"%s" % value
            self._image_.src_base64 = None

    def set_src_base64(self, value):
        self._image_.src_base64 = value

    def set_repeat(self, value):
        self._image_.repeat = value

    def set_fit(self, value):
        self._image_.fit = value

    def set_image_opacity(self, value):
        self._image_.opacity = value

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "src": self['src']
        })
        return attributes

    def set_attributes(self, node):
        super().set_attributes(node)
        # attr
        attributes = node['attributes']
        if 'src' in attributes:
            self.src = attributes["src"]

    @classmethod
    def defaut_style(cls):
        style = FletBaseElement.defaut_style()
        style.update({
            "background-color": "transparent"
        })
        return style

    @classmethod
    def defaut_attributes(cls):
        return {
            "src": "image/logo.png",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "image", left, top)
