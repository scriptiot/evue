# -*- coding: utf-8 -*-
from itertools import cycle
from flet import (
    Stack,
    Draggable,
    alignment,
    border,
    border_radius,
    DataTable,
    DataColumn,
    Text
)
import flet as ft
from .fletbaseelement import FletBaseElement
from .widgets import BaseContainer
from loguru import logger


class TableElement(FletBaseElement):

    def __init__(self, node, parent, draggable=False, sessionID=None):
        super().__init__(node, parent, draggable, sessionID=sessionID)
        self.create(parent, draggable)
        self.setParent(parent)

    def create(self, parent, draggable=False):
        self._table_ = DataTable()
        if draggable:
            self._obj_ = BaseContainer(Draggable(content=self._table_),
                alignment=alignment.center
            )
            self._obj_.content.element = self
        else:
            self._obj_ = BaseContainer(self._table_, alignment=alignment.center)

    @property
    def isContainer(self):
        return False
    
    def set_width(self, value):
        self._obj_.width = value
        self._table_.width = value
    
    def set_data_row_height(self, value):
        self._table_.data_row_height = value
    
    def set_column_spacing(self, value):
        self._table_.column_spacing = value

    def set_hover_color(self, color):
        self._table_.data_row_color = {"hovered": color},

    def set_columns(self, columns):
        logger.info(columns)
        self._table_.columns=[ft.DataColumn(ft.Text(f'{item}')) for item in columns]
    
    def set_rows(self, rows):
        def on_select_changed(e):
            index = self._table_.rows.index(e.control)
            if 'onSelectChanged' in self:
                self['onSelectChanged'](index)
        self._table_.rows= [ft.DataRow([ft.DataCell(ft.Text(f'{item}')) for item in row], on_select_changed=on_select_changed) for row in rows]

    def set_onSelectChanged(self, func):
        self['onSelectChanged'] = func

    def set_attributes(self, node):
        super().set_attributes(node)
        attributes = node['attributes']
        style = node["attributes"]['style']

        # attr
        self.columns = attributes["columns"]
        self.rows = attributes["rows"]

    def set_tiny_attributes(self, attributes):
        # attr
        self.columns = attributes["columns"]
        self.rows = attributes["rows"]

    @property
    def attributes(self):
        attributes = super().attributes
        attributes.update({
            "columns": self.columns,
            "rows": self.rows,
        })
        return attributes

    @property
    def style(self):
        style = super().style
        return style

    @classmethod
    def defaut_style(cls):
        color = next(cls.colors)
        return {
            "left": 0,
            "top": 0,
            "width": 400,
            "height": 400,
            "border-width": 0,
            "border-radius": 0,
            "border-color": "transparent",
            "hover-color": "red"
        }

    @classmethod
    def defaut_attributes(cls):
        return {
            "columns": ['a', 'b'],
            "rows": [['1', '2'], ['3', '4']],
            "style": cls.defaut_style()
        }

    @classmethod
    def defaut_json(cls, left=0, top=0):
        return FletBaseElement.defaut_json(cls, "table", left, top)
