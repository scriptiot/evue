# -*- coding: utf-8 -*-
from .fletbaseelement import FletBaseElement
from flet import (
    Draggable,
    GridView,
    alignment
)
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer


class GridElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._grid_ = GridView([], expand=True)
        self._controls_ = self._grid_.controls
        if draggable:
            self._obj_ = BaseContainer(
                Draggable(content=self._grid_), 
                alignment = alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(
                self._grid_
            )

    @property
    def isContainer(self):
        return True
    
    @property
    def isLayout(self):
        return True

    def set_width(self, value):
        self._obj_.width = value

    def set_height(self, value):
        self._obj_.height = value

    def set_horizontal(self, value):
        self._grid_.horizontal = FletBaseElement.bool(value)

    def set_runs_count(self, value):
        self._grid_.runs_count = value

    def set_max_extent(self, value):
        self._grid_.max_extent = value

    def set_child_aspect_ratio(self, value):
        self._grid_.child_aspect_ratio = value

    def set_spacing(self, value):
        self._grid_.spacing = value
        self._grid_.run_spacing = value

    def set_padding(self, value):
        self._grid_.padding = value

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        style = attributes['style']
        # attr
        self.horizontal = attributes["horizontal"]
        self.runs_count = attributes["runs_count"]
        self.max_extent = attributes["max_extent"]
        self.spacing = attributes["spacing"]
        self.run_spacing = attributes["run_spacing"]
        self.child_aspect_ratio = attributes["child_aspect_ratio"]
        self.padding = attributes["padding"]

    def set_tiny_attributes(self, data):
        # attr
        self.horizontal = data["horizontal"]
        self.runs_count = data["runs_count"]
        self.max_extent = data["max_extent"]
        self.spacing = data["spacing"]
        self.run_spacing = data["run_spacing"]
        self.child_aspect_ratio = data["child_aspect_ratio"]
        self.padding = data["padding"]

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "horizontal": self._grid_.horizontal,
            "runs_count": self._grid_.runs_count,
            "max_extent": self._grid_.max_extent,
            "spacing": self._grid_.spacing,
            "run_spacing": self._grid_.run_spacing,
            "child_aspect_ratio": self._grid_.child_aspect_ratio,
            "padding": self._grid_.padding
        })
        return attributes

    @classmethod
    def defaut_style(cls):
        return {
            "left": 0,
            "top": 0,
            "width": 200,
            "height": 200,
            "border-width": 0,
            "border-radius": 0,
            "border-color": "transparent",
            "background-color": "white"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "horizontal": False,
            "runs_count": 5,
            "max_extent": 150,
            "spacing": 5,
            "run_spacing": 5,
            "child_aspect_ratio": 1,
            "padding": 5,
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "grid", left, top)
