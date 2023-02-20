# -*- coding: utf-8 -*-
import os
from .fletbaseelement import FletBaseElement
from .image import ImageElement
from .widgets import BaseContainer
from ..router import globalThis
from io import BytesIO
import qrcode
import base64
import hashlib

def qrcode_make(s):
    qr = qrcode.make(s)
    buffered = BytesIO()
    qr.save(buffered, format="JPEG")
    s1 = base64.b64encode(buffered.getvalue())
    b64_string = s1.decode('utf-8')
    return b64_string

def qrcode_make_png(s):
    md5 = hashlib.md5(s.encode("utf-8")).hexdigest()
    path = "image/qrcode_%s.png" % (md5)
    if not os.path.exists(path):
        qr = qrcode.make(s)
        buffered = BytesIO()
        qr.save(buffered, format="png")
        with open(path, "wb") as f:
            f.write(buffered.getvalue())
    return path

class QRCodeElement(ImageElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)


    def set_value(self, value):
        value = str(value)
        self._image_.src_base64 = qrcode_make(value)

    def set_src(self, value):
        value = str(value)
        self.set_value(value)

    def set_src_base64(self, value):
        self.set_value(value)

    def set_image_src_base64(self, value):
        self.set_value(value)

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "value": self.value,
            "tooltip": self.tooltip
        })
        return attributes

    def set_attributes(self, node):
        super().set_attributes(node)
        # attr
        attributes = node['attributes']
        self.value = attributes["value"]
        self.tooltip = attributes["tooltip"]
    
    def set_tiny_attributes(self, attributes):
        self.value = attributes["value"]
        self.tooltip = attributes["tooltip"]

    @classmethod
    def defaut_style(cls):
        return {
            "width": 128,
            "height": 128,
            "background-color": "transparent"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "value": "https://www.yuque.com/bytecode/eu1sci/bgb7ho",
            "tooltip": "EVUE 小程序开发文档 2.0",
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "qrcode", left, top)
