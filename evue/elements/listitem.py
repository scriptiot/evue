# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from .div import DivElement


class ListItemElement(DivElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)

    @classmethod
    def defaut_style(cls):
        return {
            "left": 0,
            "top": 0,
            "width": 150,
            "height": 40,
            "border-width": 0,
            "border-color": "transparent",
            "border-radius": 0,
            "background-color": "#282828",
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "listitem", left, top)
