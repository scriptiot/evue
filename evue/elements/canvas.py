# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from .div import DivElement


class CanvasElement(DivElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)

    @classmethod
    def defaut_style(cls):
        ret = DivElement.defaut_style()
        ret.update({
            "width": 128,
            "height": 128,
            "background-color": "white",
        })
        return ret

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "canvas", left, top)
